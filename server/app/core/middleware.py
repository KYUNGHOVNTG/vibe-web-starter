"""
Core Middleware

Request ID 추적, 로깅 등 애플리케이션 전역에 적용되는 미들웨어들을 정의합니다.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .logging import get_logger

logger = get_logger(__name__)


# ====================
# Request ID Middleware
# ====================

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    모든 요청에 대해 고유한 Request ID를 생성하거나 수신합니다.

    - X-Request-ID 헤더가 있으면 그것을 사용
    - 없으면 새로운 UUID 생성
    - Request ID를 응답 헤더에 포함
    - Request ID를 로그 컨텍스트에 저장
    """

    REQUEST_ID_HEADER = "X-Request-ID"

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Request ID 가져오기 또는 생성
        request_id = request.headers.get(self.REQUEST_ID_HEADER)
        if not request_id:
            request_id = str(uuid.uuid4())

        # Request state에 저장 (다른 코드에서 접근 가능)
        request.state.request_id = request_id

        # 시작 시간 기록
        start_time = time.time()

        # 요청 로깅
        logger.info(
            f"[req_id={request_id}] {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
            }
        )

        try:
            # 다음 미들웨어/핸들러 실행
            response = await call_next(request)

            # 처리 시간 계산
            process_time = time.time() - start_time

            # Response 헤더에 Request ID 추가
            response.headers[self.REQUEST_ID_HEADER] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            # 응답 로깅
            logger.info(
                f"[req_id={request_id}] {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time": process_time,
                }
            )

            return response

        except Exception as e:
            # 에러 발생 시에도 Request ID 포함하여 로깅
            process_time = time.time() - start_time
            logger.error(
                f"[req_id={request_id}] {request.method} {request.url.path} - ERROR: {str(e)} ({process_time:.3f}s)",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "process_time": process_time,
                },
                exc_info=True
            )
            raise


# ====================
# Logging Middleware (Stub)
# ====================

class ExternalLoggingMiddleware(BaseHTTPMiddleware):
    """
    외부 로깅 서비스 연동을 위한 Stub 미들웨어

    실제 구현 시 여기에 다음 서비스들을 연동할 수 있습니다:
    - Sentry
    - DataDog
    - CloudWatch
    - ELK Stack
    등등
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # TODO: 외부 로깅 서비스 연동
        # 현재는 stub으로만 존재

        response = await call_next(request)

        # 여기에 외부 로깅 서비스로 전송하는 코드 추가
        # await send_to_external_logging_service(...)

        return response
