"""
Sample Domain API 엔드포인트

샘플 도메인의 REST API 엔드포인트를 정의합니다.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.core.dependencies import (
    get_database_session,
    get_optional_current_user,
    get_pagination,
    PaginationParams,
)
from server.app.examples.sample_domain.service import (
    SampleDomainService,
    SimpleGetService,
)
from server.app.examples.sample_domain.schemas import (
    SampleAnalysisRequest,
    SampleAnalysisResponse,
    SampleListResponse,
)

# 라우터 생성
router = APIRouter(
    prefix="/sample",
    tags=["sample"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


# ====================
# GET 엔드포인트 (교과서 예제)
# ====================


@router.get(
    "",
    response_model=SampleListResponse,
    status_code=status.HTTP_200_OK,
    summary="샘플 데이터 목록 조회",
    description="""
    샘플 데이터 목록을 조회합니다.

    이 엔드포인트는 **Router → Service → Provider → Calculator → Formatter** 흐름을
    보여주는 교과서 예제입니다.

    **각 레이어의 책임:**
    - **Router**: HTTP 요청 수신, 응답 반환
    - **Service**: 비즈니스 로직 조율 (Provider, Calculator, Formatter 조합)
    - **Provider**: 데이터 제공 (DB, API, 파일 등)
    - **Calculator**: 데이터 가공 및 계산 (순수 함수)
    - **Formatter**: API 응답 형식으로 변환

    **Response:**
    - `items`: 샘플 아이템 목록 (status가 'active'인 것만)
    - `total_count`: 아이템 개수
    - `message`: 응답 메시지

    **NOTE:**
    - 실제 비즈니스 로직 없음 (mock 데이터 사용)
    - 새로운 도메인 API를 만들 때 이 구조를 참고하세요
    """,
)
async def get_sample_list(
    db: AsyncSession = Depends(get_database_session),
    current_user: Optional[dict] = Depends(get_optional_current_user),
) -> SampleListResponse:
    """
    샘플 데이터 목록을 조회합니다.

    Args:
        db: 데이터베이스 세션
        current_user: 현재 사용자 정보 (선택)

    Returns:
        SampleListResponse: 샘플 데이터 목록

    Raises:
        HTTPException: 처리 중 오류 발생 시
    """
    # Service 인스턴스 생성
    service = SimpleGetService(db)

    # Service 실행
    result = await service.execute(
        None,
        user_id=current_user.get("id") if current_user else None
    )

    # 결과 처리
    if result.success:
        return result.data
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error
        )


# ====================
# POST 엔드포인트 (기존)
# ====================


@router.post(
    "/analyze",
    response_model=SampleAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="데이터 분석 실행",
    description="""
    샘플 데이터에 대한 분석을 수행합니다.

    이 엔드포인트는 새로운 도메인 엔드포인트를 만들 때 참고할 수 있는 예제입니다.

    **분석 유형:**
    - `statistical`: 통계 분석 (평균, 중앙값, 표준편차 등)
    - `trend`: 트렌드 분석 (상승/하락 추세)
    - `anomaly`: 이상치 탐지

    **사용 예시:**
    ```json
    {
        "data_id": 1,
        "analysis_type": "statistical",
        "threshold": 0.5,
        "include_details": true
    }
    ```
    """,
)
async def analyze_data(
    request: SampleAnalysisRequest,
    db: AsyncSession = Depends(get_database_session),
    current_user: Optional[dict] = Depends(get_optional_current_user),
) -> SampleAnalysisResponse:
    """
    데이터 분석을 수행합니다.

    Args:
        request: 분석 요청 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자 정보 (선택)

    Returns:
        SampleAnalysisResponse: 분석 결과

    Raises:
        HTTPException: 요청 실패 시
    """
    # 서비스 인스턴스 생성
    service = SampleDomainService(db)

    # 사용자 ID 추출 (있는 경우)
    user_id = current_user.get("user_id") if current_user else None

    # 서비스 실행
    result = await service.execute(request, user_id=user_id)

    # 결과 처리
    if result.success:
        return result.data
    else:
        # 에러 응답
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.error,
        )


@router.get(
    "/health",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="헬스체크",
    description="샘플 도메인 API의 상태를 확인합니다.",
)
async def health_check() -> dict:
    """
    헬스체크 엔드포인트

    Returns:
        dict: 상태 정보
    """
    return {
        "status": "healthy",
        "domain": "sample",
        "version": "1.0.0",
    }


# TODO: 추가 엔드포인트 구현 예시


@router.get(
    "/data/{data_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="데이터 조회",
    description="ID로 샘플 데이터를 조회합니다.",
)
async def get_data(
    data_id: int,
    db: AsyncSession = Depends(get_database_session),
) -> dict:
    """
    데이터를 조회합니다.

    Args:
        data_id: 데이터 ID
        db: 데이터베이스 세션

    Returns:
        dict: 데이터 정보

    TODO: 실제 구현
        - Service 메서드 추가
        - 에러 처리
        - 권한 확인
    """
    # 스텁
    return {
        "id": data_id,
        "name": f"Sample Data {data_id}",
        "value": 42.5,
        "score": 0.85,
    }


@router.get(
    "/data",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="데이터 목록 조회",
    description="샘플 데이터 목록을 페이지네이션과 함께 조회합니다.",
)
async def list_data(
    pagination: PaginationParams = Depends(get_pagination),
    db: AsyncSession = Depends(get_database_session),
) -> dict:
    """
    데이터 목록을 조회합니다.

    Args:
        pagination: 페이지네이션 파라미터
        db: 데이터베이스 세션

    Returns:
        dict: 페이지네이션된 데이터 목록

    TODO: 실제 구현
        - Service list 메서드 추가
        - 필터링 파라미터 추가
        - 정렬 기능 추가
    """
    # 스텁
    return {
        "items": [
            {"id": i, "name": f"Sample Data {i}", "value": 42.5}
            for i in range(pagination.skip, pagination.skip + min(10, pagination.limit))
        ],
        "total": 100,
        "page": (pagination.skip // pagination.limit) + 1,
        "page_size": pagination.limit,
    }


@router.post(
    "/data",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="데이터 생성",
    description="새로운 샘플 데이터를 생성합니다.",
)
async def create_data(
    request: dict,
    db: AsyncSession = Depends(get_database_session),
    current_user: Optional[dict] = Depends(get_optional_current_user),
) -> dict:
    """
    새로운 데이터를 생성합니다.

    Args:
        request: 생성 요청 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자 정보

    Returns:
        dict: 생성된 데이터

    TODO: 실제 구현
        - SampleDataCreateRequest 스키마 사용
        - CRUDService 구현
        - 트랜잭션 처리
    """
    # 스텁
    return {
        "id": 999,
        "name": request.get("name", "New Sample Data"),
        "value": request.get("value", 0.0),
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.put(
    "/data/{data_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="데이터 수정",
    description="기존 샘플 데이터를 수정합니다.",
)
async def update_data(
    data_id: int,
    request: dict,
    db: AsyncSession = Depends(get_database_session),
    current_user: Optional[dict] = Depends(get_optional_current_user),
) -> dict:
    """
    데이터를 수정합니다.

    Args:
        data_id: 데이터 ID
        request: 수정 요청 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자 정보

    Returns:
        dict: 수정된 데이터

    TODO: 실제 구현
        - CRUDService update 메서드
        - 낙관적 잠금 처리
        - 권한 확인
    """
    # 스텁
    return {
        "id": data_id,
        "name": request.get("name", "Updated Sample Data"),
        "value": request.get("value", 0.0),
        "updated_at": "2024-01-01T00:00:00Z",
    }


@router.delete(
    "/data/{data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="데이터 삭제",
    description="샘플 데이터를 삭제합니다.",
)
async def delete_data(
    data_id: int,
    db: AsyncSession = Depends(get_database_session),
    current_user: Optional[dict] = Depends(get_optional_current_user),
) -> None:
    """
    데이터를 삭제합니다.

    Args:
        data_id: 데이터 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자 정보

    TODO: 실제 구현
        - CRUDService delete 메서드
        - 소프트 삭제 vs 하드 삭제
        - 연관 데이터 처리
    """
    # 스텁
    pass
