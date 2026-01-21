"""
FastAPI 애플리케이션 진입점

AI 데이터 분석 웹 서비스의 메인 애플리케이션입니다.
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from rich.logging import RichHandler

from server.app.core.config import settings
from server.app.core.database import DatabaseManager
from server.app.core.routers import router as core_router
from server.app.core.middleware import RequestIDMiddleware, ExternalLoggingMiddleware
from server.app.api.v1.router import api_router
from server.app.shared.exceptions import ApplicationException

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

logging.basicConfig(
    level="INFO",  # 보고 싶은 로그 레벨 (DEBUG, INFO 등)
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            rich_tracebacks=True,          # 예외 발생 시 Rich 스타일 Traceback 출력
            tracebacks_show_locals=False,   # 로컬 변수 값 표시 (상세 디버깅용)
            markup=True
        )
    ]
)

# Uvicorn 로그 제거 및 Rich 적용
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.handlers = [
    RichHandler(rich_tracebacks=True, tracebacks_show_locals=False, markup=True)
]
uvicorn_error.propagate = False

uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.handlers = [
    RichHandler(rich_tracebacks=True, tracebacks_show_locals=False, markup=True)
]
uvicorn_access.propagate = False

logger = logging.getLogger("uvicorn")


# ====================
# Lifespan Events
# ====================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    애플리케이션 생명주기 관리

    시작 시:
        - 데이터베이스 연결 확인
        - 필요한 초기화 작업 수행

    종료 시:
        - 데이터베이스 연결 종료
        - 리소스 정리
    """

    print_vibe_signature()

    # 시작 시 실행
    logger.info("🚀 Starting application...")
    logger.info(f"📦 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🗄️  Database: {settings.POSTGRES_DB}")

    # TODO: 필요한 초기화 작업
    # - 데이터베이스 마이그레이션 확인
    # - 캐시 워밍업
    # - 외부 서비스 연결 확인

    # 개발 환경에서는 테이블 자동 생성 (운영에서는 사용 금지!)
    if settings.ENVIRONMENT == "development" and settings.DEBUG:
        print("⚠️  Development mode: Creating database tables...")
        # await DatabaseManager.create_tables()

    yield

    # 종료 시 실행
    logger.info("👋 Shutting down application...")
    await DatabaseManager.close_connections()
    logger.info("✅ Application shutdown complete")


# ====================
# FastAPI Application
# ====================


def create_application() -> FastAPI:
    """
    FastAPI 애플리케이션을 생성하고 설정합니다.

    Returns:
        FastAPI: 설정된 애플리케이션 인스턴스
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        # AI 데이터 분석 웹 서비스 템플릿

        FastAPI + SQLAlchemy 기반의 확장 가능한 백엔드 아키텍처

        ## 주요 기능

        - **도메인 플러그인 구조**: 새로운 도메인을 쉽게 추가 가능
        - **계층화된 아키텍처**: Router → Service → Provider/Calculator/Formatter
        - **타입 안전성**: Pydantic v2 + SQLAlchemy 2.0
        - **비동기 처리**: async/await 기반

        ## 아키텍처

        ```
        Router (FastAPI)
            ↓
        Service (비즈니스 로직 조율)
            ↓
        ├─ Provider (데이터 조회)
        ├─ Calculator (계산/분석)
        └─ Formatter (응답 포맷팅)
        ```

        ## 새 도메인 추가 방법

        1. `server/app/examples/` 또는 `server/app/domain/` 에 새 디렉토리 생성
        2. Provider, Calculator, Formatter, Service 구현
        3. `server/app/api/v1/endpoints/` 에 라우터 추가
        4. `server/app/api/v1/router.py` 에 라우터 등록
        """,
        debug=settings.DEBUG,
        lifespan=lifespan,
        # docs_url="/docs" if settings.DEBUG else None,  # 운영에서는 문서 비활성화 가능
        # redoc_url="/redoc" if settings.DEBUG else None,
    )

    # ====================
    # Middleware 설정
    # ====================

    # Request ID 추적 (가장 먼저 추가!)
    app.add_middleware(RequestIDMiddleware)

    # 외부 로깅 서비스 (stub)
    app.add_middleware(ExternalLoggingMiddleware)

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host 설정 (운영 환경)
    if settings.ENVIRONMENT == "production":
        # TODO: 운영 환경에서는 실제 호스트 목록으로 변경
        # app.add_middleware(
        #     TrustedHostMiddleware,
        #     allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
        # )
        pass

    # TODO: 추가 미들웨어
    # - 메트릭 수집
    # - Rate Limiting

    # ====================
    # Exception Handlers
    # ====================

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request,
        exc: ApplicationException
    ) -> JSONResponse:
        """
        애플리케이션 예외 핸들러

        비즈니스 로직에서 발생한 예외를 적절한 HTTP 응답으로 변환합니다.
        """
        # Request ID 가져오기
        request_id = getattr(request.state, 'request_id', None)

        # 로깅
        logger.warning(
            f"Application exception: {exc.message}",
            extra={
                "request_id": request_id,
                "exception_type": type(exc).__name__,
                "status_code": exc.status_code,
                "details": exc.details,
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """
        일반 예외 핸들러

        예상치 못한 예외를 처리합니다.
        """
        # Request ID 가져오기
        request_id = getattr(request.state, 'request_id', None)

        # 로깅 및 알림
        logger.error(
            f"Unexpected error: {str(exc)}",
            extra={
                "request_id": request_id,
                "exception_type": type(exc).__name__,
                "path": request.url.path,
                "method": request.method,
            },
            exc_info=True
        )

        # 개발 환경에서는 상세 에러 표시
        if settings.DEBUG:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "details": {
                        "type": type(exc).__name__,
                        "message": str(exc),
                    },
                },
            )

        # 운영 환경에서는 간단한 에러 메시지만
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
            },
        )

    # ====================
    # Router 등록
    # ====================

    # Core 라우터 (인프라 레벨)
    app.include_router(core_router)

    # API v1 라우터
    app.include_router(
        api_router,
        prefix=settings.API_V1_PREFIX,
    )

    # 루트 엔드포인트
    @app.get(
        "/",
        tags=["root"],
        summary="루트 엔드포인트",
    )
    async def root() -> dict:
        """
        루트 엔드포인트

        API 기본 정보를 반환합니다.
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs",
            "api_v1": settings.API_V1_PREFIX,
            "health": "/core/health",
            "version_info": "/core/version",
        }

    return app


# ====================
# Application Instance
# ====================

# 애플리케이션 인스턴스 생성
app = create_application()


# ====================
# CLI Entry Point
# ====================

if __name__ == "__main__":
    """
    개발 서버 실행

    사용법:
        python -m server.main
    """
    import uvicorn

    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )

# ==========================================
# VIBE WEB STARTER SIGNATURE
# ==========================================
def print_vibe_signature():

    console = Console()

    ascii_art = r"""
██╗   ██╗██╗██████╗ ███████╗    ██╗    ██╗███████╗██████╗ 
██║   ██║██║██╔══██╗██╔════╝    ██║    ██║██╔════╝██╔══██╗
██║   ██║██║██████╔╝█████╗      ██║ █╗ ██║█████╗  ██████╔╝
╚██╗ ██╔╝██║██╔══██╗██╔══╝      ██║███╗██║██╔══╝  ██╔══██╗
 ╚████╔╝ ██║██████╔╝███████╗    ╚███╔███╔╝███████╗██████╔╝
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝     ╚══╝╚══╝ ╚══════╝╚═════╝ 
███████╗████████╗ █████╗ ██████╗ ████████╗███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
███████╗   ██║   ███████║██████╔╝   ██║   █████╗  ██████╔╝
╚════██║   ██║   ██╔══██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
"""
    styled_art = Text(ascii_art)
    styled_art.stylize("bold bright_cyan", 0, len(ascii_art) // 2)
    styled_art.stylize("bold dodger_blue1", len(ascii_art) // 2, len(ascii_art))

    info_content = Text.from_markup(
        f"\n[gray30]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/gray30]\n"
        f" 🚀 [bold white]AI Vibe Web Starter[/bold white]  [green]v{settings.APP_VERSION}[/green]\n\n"
        f" 👨‍💻 Created by : [bold cyan]최경호[/bold cyan]\n"
        f" 📮 Contact    : [underline sky_blue2]cjhol2107@vntgcorp.com[/underline sky_blue2]\n"
        f" ✨ [italic gray70]Code with Vibe, Build with Speed.[/italic gray70]"
    )
    
    final_render = Group(
        styled_art,
        Align.center(info_content)
    )

    panel = Panel(
        final_render,
        border_style="bright_cyan",
        title="[bold white] Welcome Back [/bold white]",
        subtitle="[bold white] Server Ready [/bold white]",
        expand=False,
        padding=(1, 4)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")