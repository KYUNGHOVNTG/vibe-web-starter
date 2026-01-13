"""
Core Logging Configuration

애플리케이션 전역 로깅 설정을 관리합니다.
- Request ID 자동 포함
- 구조화된 로그 형식
- 레벨별 로그 필터링
"""

import logging
import sys
from typing import Any, Dict

from .config import get_settings

settings = get_settings()


# ====================
# Custom Log Formatter
# ====================

class RequestIDFormatter(logging.Formatter):
    """
    Request ID를 자동으로 포함하는 로그 포맷터

    로그 형태: [req_id=xxxx] LEVEL - MESSAGE
    """

    def format(self, record: logging.LogRecord) -> str:
        # extra에 request_id가 있으면 사용, 없으면 '-'
        request_id = getattr(record, 'request_id', '-')

        # 기존 로그 레코드에 request_id 추가
        if request_id != '-':
            prefix = f"[req_id={request_id}] "
        else:
            prefix = ""

        # 원래 메시지 포맷
        original_format = super().format(record)

        # prefix 추가
        return f"{prefix}{original_format}"


# ====================
# Logger Setup
# ====================

def setup_logging() -> None:
    """
    애플리케이션 로깅 설정을 초기화합니다.

    - 콘솔 핸들러 설정
    - Request ID 포맷터 적용
    - 로그 레벨 설정
    """

    # 루트 로거 가져오기
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL.upper())

    # 기존 핸들러 제거 (중복 방지)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 콘솔 핸들러 생성
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL.upper())

    # Request ID 포맷터 적용
    formatter = RequestIDFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # 루트 로거에 핸들러 추가
    root_logger.addHandler(console_handler)

    # uvicorn 로거 설정
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(settings.LOG_LEVEL.upper())

    # FastAPI 로거 설정
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(settings.LOG_LEVEL.upper())

    logging.info("Logging configuration initialized")


def get_logger(name: str) -> logging.Logger:
    """
    모듈별 로거를 가져옵니다.

    Args:
        name: 로거 이름 (보통 __name__ 사용)

    Returns:
        설정된 로거 인스턴스
    """
    return logging.getLogger(name)


# ====================
# Logging Utilities
# ====================

def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    request_id: str | None = None,
    **kwargs: Any
) -> None:
    """
    Request ID를 포함한 로그를 기록합니다.

    Args:
        logger: 로거 인스턴스
        level: 로그 레벨 (INFO, WARNING, ERROR, etc.)
        message: 로그 메시지
        request_id: Request ID (optional)
        **kwargs: 추가 로그 컨텍스트
    """
    extra: Dict[str, Any] = kwargs.copy()
    if request_id:
        extra['request_id'] = request_id

    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message, extra=extra)


# ====================
# External Logging Service Stub
# ====================

class ExternalLoggingService:
    """
    외부 로깅 서비스 연동을 위한 Stub 클래스

    실제 구현 시 여기에 다음 서비스들을 연동할 수 있습니다:
    - Sentry
    - DataDog
    - CloudWatch
    - ELK Stack
    등등
    """

    def __init__(self):
        self.enabled = False  # 현재는 비활성화

    async def send_log(self, log_data: Dict[str, Any]) -> None:
        """
        외부 로깅 서비스로 로그를 전송합니다. (Stub)

        Args:
            log_data: 전송할 로그 데이터
        """
        if not self.enabled:
            return

        # TODO: 외부 로깅 서비스 연동
        # 예: await sentry_sdk.capture_message(...)
        pass

    async def send_error(
        self,
        error: Exception,
        context: Dict[str, Any] | None = None
    ) -> None:
        """
        외부 로깅 서비스로 에러를 전송합니다. (Stub)

        Args:
            error: 발생한 예외
            context: 추가 컨텍스트 정보
        """
        if not self.enabled:
            return

        # TODO: 외부 로깅 서비스 연동
        # 예: await sentry_sdk.capture_exception(...)
        pass


# 싱글톤 인스턴스
external_logging_service = ExternalLoggingService()
