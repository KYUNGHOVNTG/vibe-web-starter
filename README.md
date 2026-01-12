# AI 데이터 분석 웹 서비스 템플릿

FastAPI + React 기반의 풀스택 웹 애플리케이션

## 프로젝트 개요

이 프로젝트는 AI 데이터 분석 웹 서비스를 위한 재사용 가능한 풀스택 템플릿입니다.
- **백엔드**: FastAPI + SQLAlchemy 기반의 확장 가능한 API 서버
- **프론트엔드**: React + Vite + TypeScript 기반의 모던 웹 인터페이스

도메인 플러그인 구조를 통해 새로운 기능을 쉽게 추가할 수 있도록 설계되었습니다.

### 주요 특징

- **계층화된 아키텍처**: Router → Service → Provider/Calculator/Formatter
- **도메인 플러그인 구조**: 새로운 도메인을 독립적으로 추가 가능
- **모든 비즈니스 로직은 클래스 기반**: 절차지향 함수 사용 금지
- **타입 안전성**: Pydantic v2 + SQLAlchemy 2.0
- **비동기 처리**: async/await 기반
- **확장 가능**: 명확한 패턴과 추상 클래스 제공

## 기술 스택

### 백엔드
- **Python**: 3.12
- **Web Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL (asyncpg)
- **Validation**: Pydantic v2
- **Testing**: pytest + pytest-asyncio
- **Code Quality**: black, isort, ruff, mypy

### 프론트엔드
- **Framework**: React 19
- **Build Tool**: Vite 7
- **Language**: TypeScript 5.9
- **Styling**: Tailwind CSS 4
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Animation**: Framer Motion
- **Routing**: React Router DOM

## 프로젝트 구조

```
ai-worker-project/
├── server/                     # 백엔드 (FastAPI)
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   └── app/
│       ├── core/               # 핵심 인프라
│       │   ├── config.py       # 설정 관리
│       │   ├── database.py     # DB 연결 및 세션
│       │   └── dependencies.py # FastAPI 의존성
│       ├── shared/             # 공유 컴포넌트
│       │   ├── base/           # 추상 베이스 클래스
│       │   ├── exceptions/     # 커스텀 예외
│       │   └── types/          # 공통 타입
│       ├── domain/             # 비즈니스 도메인
│       ├── examples/           # 예제 도메인
│       │   └── sample_domain/  # 샘플 도메인 구현
│       └── api/
│           └── v1/
│               ├── endpoints/  # API 엔드포인트
│               └── router.py   # 라우터 통합
├── client/                     # 프론트엔드 (React + Vite)
│   ├── src/
│   │   ├── components/         # React 컴포넌트
│   │   ├── pages/              # 페이지 컴포넌트
│   │   ├── store/              # Zustand 상태 관리
│   │   ├── api/                # API 호출 함수
│   │   ├── types/              # TypeScript 타입
│   │   └── App.tsx             # 메인 App 컴포넌트
│   ├── public/                 # 정적 파일
│   ├── package.json            # npm 의존성
│   ├── vite.config.ts          # Vite 설정
│   └── tsconfig.json           # TypeScript 설정
├── tests/                      # 테스트
│   ├── unit/
│   └── integration/
├── requirements.txt            # Python 의존성
├── pyproject.toml              # Python 프로젝트 설정
└── .env.example                # 환경 변수 예제
```

## 아키텍처

```
┌─────────────────────────────────────────────┐
│            FastAPI Router (API)             │
│         /api/v1/sample/analyze              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│          Service (비즈니스 로직 조율)          │
│       SampleDomainService.execute()         │
└─────┬───────────┬──────────────┬────────────┘
      │           │              │
      ▼           ▼              ▼
┌─────────┐ ┌────────────┐ ┌────────────┐
│Provider │ │Calculator  │ │Formatter   │
│데이터조회│ │계산/분석    │ │응답포맷팅   │
└─────────┘ └────────────┘ └────────────┘
```

### 각 계층의 역할

1. **Router** (API Layer)
   - HTTP 요청 수신
   - 입력 검증 (Pydantic)
   - Service 호출
   - HTTP 응답 반환

2. **Service** (Business Logic Layer)
   - Provider, Calculator, Formatter 조율
   - 트랜잭션 관리
   - 권한 검증
   - 에러 핸들링

3. **Provider** (Data Access Layer)
   - 데이터베이스 쿼리
   - 외부 API 호출
   - 파일 시스템 접근
   - 캐시 조회

4. **Calculator** (Computation Layer)
   - 순수한 계산 로직
   - 데이터 분석
   - 통계 처리
   - 알고리즘 적용

5. **Formatter** (Presentation Layer)
   - API 응답 형식 변환
   - 데이터 직렬화
   - 민감정보 마스킹

자세한 내용은 [ARCHITECTURE.md](ARCHITECTURE.md)를 참조하세요.

## 🚀 로컬 환경에서 실행하기

이 가이드는 Docker 없이 로컬 환경에서 백엔드와 프론트엔드를 실행하는 방법을 설명합니다.

### 📋 사전 준비사항

시작하기 전에 다음 프로그램들이 설치되어 있어야 합니다:

1. **Python 3.12 이상**
   - 설치 확인: 터미널에서 `python3 --version` 또는 `python --version` 실행
   - 다운로드: https://www.python.org/downloads/

2. **Node.js 18 이상 및 npm**
   - 설치 확인: 터미널에서 `node --version` 및 `npm --version` 실행
   - 다운로드: https://nodejs.org/

3. **PostgreSQL 데이터베이스**
   - 설치 확인: 터미널에서 `psql --version` 실행
   - 다운로드: https://www.postgresql.org/download/
   - 설치 후 PostgreSQL 서비스가 실행 중이어야 합니다

---

## 1️⃣ 백엔드 (FastAPI) 실행하기

### 1-1. 프로젝트 루트 디렉토리로 이동
```bash
cd ai-worker-project
```
> 💡 **왜 하는가?**: 백엔드 설정을 시작하기 위해 프로젝트의 최상위 폴더로 이동합니다.

### 1-2. Python 가상환경 생성
```bash
python3 -m venv .venv
```
> 💡 **왜 하는가?**: 프로젝트 전용 독립적인 Python 환경을 만듭니다. 시스템 전역 Python과 충돌을 방지합니다.

### 1-3. 가상환경 활성화
```bash
# macOS/Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```
> 💡 **왜 하는가?**: 가상환경을 활성화해야 이후 설치하는 패키지들이 이 프로젝트 전용으로 설치됩니다.
>
> ✅ **확인**: 터미널 앞에 `(.venv)`가 표시되면 성공입니다.

### 1-4. Python 의존성 패키지 설치
```bash
pip install -r requirements.txt
```
> 💡 **왜 하는가?**: FastAPI, SQLAlchemy 등 백엔드 실행에 필요한 모든 라이브러리를 설치합니다.
>
> ⏱️ **소요시간**: 약 1-3분 (인터넷 속도에 따라 다름)

### 1-5. 환경 변수 파일 생성
```bash
# .env.example을 복사해서 .env 파일 생성
cp .env.example .env
```
> 💡 **왜 하는가?**: 데이터베이스 접속 정보, 보안 키 등 환경별 설정을 담는 파일입니다.

### 1-6. 환경 변수 파일 수정 (중요!)
텍스트 에디터로 `.env` 파일을 열어 다음 내용을 확인/수정합니다:


```bash
# ====================
# Database Settings (Supabase)
# ====================
POSTGRES_HOST=db.cafquolsrqkhpqejgojd.supabase.co
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=chl0795chl0795!
POSTGRES_DB=postgres

# SQLAlchemy 연결 URL (asyncpg 사용)
DATABASE_URL=postgresql+asyncpg://postgres:chl0795chl0795%21@db.cafquolsrqkhpqejgojd.supabase.co:5432/postgres

# ====================
# Security Settings
# ====================
# 터미널에서 python -c "import secrets; print(secrets.token_hex(32))" 실행 결과 입력
SECRET_KEY=your-generated-random-string

```

### 1-7. Supabase 테이블 생성 (SQL Editor 사용)

로컬에 DB를 설치할 필요 없이 Supabase 대시보드에서 직접 실행합니다.

1. **Supabase Dashboard**에 접속합니다.
2. 왼쪽 메뉴에서 **SQL Editor** 아이콘을 클릭합니다.
3. **New Query**를 선택하고, 프로젝트의 테이블 생성 SQL(예: `schema.sql`) 내용을 붙여넣습니다.
4. 오른쪽 하단의 **Run** 버튼을 클릭하여 테이블을 생성합니다.

### 1-8. 백엔드 서버 실행

```bash
python -m server.main

```

---

## 2️⃣ 프론트엔드 (React) 실행하기

백엔드를 실행한 터미널은 그대로 두고, **새로운 터미널 창을 열어서** 진행합니다.

### 2-1. 프론트엔드 디렉토리로 이동
```bash
cd ai-worker-project/client
```
> 💡 **왜 하는가?**: 프론트엔드 코드와 설정 파일이 있는 `client` 폴더로 이동합니다.

### 2-2. Node.js 의존성 패키지 설치
```bash
npm install
```
> 💡 **왜 하는가?**: React, Vite, TypeScript 등 프론트엔드 실행에 필요한 모든 JavaScript 라이브러리를 설치합니다.
>
> ⏱️ **소요시간**: 약 1-5분 (인터넷 속도에 따라 다름)
>
> ✅ **확인**: `node_modules` 폴더가 생성되고, 수백 개의 패키지가 설치됩니다.

### 2-3. 프론트엔드 개발 서버 실행
```bash
npm run dev
```
> 💡 **왜 하는가?**: Vite 개발 서버를 시작합니다. 코드 변경 시 자동으로 브라우저를 새로고침합니다.
>
> ✅ **성공 확인**:
> - 터미널에 `Local: http://localhost:5173/` 같은 메시지 표시
> - 웹 브라우저에서 http://localhost:5173 열기
> - React 앱이 화면에 표시됨

> ⚠️ **주의**: 이 터미널 창도 프론트엔드가 실행되는 동안 계속 열어두어야 합니다!

---

## ✅ 실행 확인

모든 것이 정상적으로 실행되면:

1. **백엔드 API**: http://localhost:8000
   - API 문서: http://localhost:8000/docs

2. **프론트엔드 웹**: http://localhost:5173

두 개의 터미널 창이 열려 있어야 합니다:
- 터미널 1: 백엔드 서버 실행 중 (`python -m server.main`)
- 터미널 2: 프론트엔드 개발 서버 실행 중 (`npm run dev`)

---

## 🛑 실행 중지하기

각 터미널에서 `Ctrl + C`를 눌러 서버를 중지할 수 있습니다.

다시 실행하려면:
- 백엔드: `python -m server.main` (프로젝트 루트에서)
- 프론트엔드: `npm run dev` (client 폴더에서)

---

## ❓ 문제 해결

### 백엔드 실행 시 에러
- `ModuleNotFoundError`: 가상환경이 활성화되었는지 확인 (`(.venv)` 표시 확인)
- `Database connection error`: PostgreSQL이 실행 중인지, `.env` 설정이 올바른지 확인
- `Port 8000 already in use`: 다른 프로그램이 8000 포트를 사용 중입니다. 종료하거나 다른 포트 사용

### 프론트엔드 실행 시 에러
- `command not found: npm`: Node.js가 설치되지 않았습니다
- `Port 5173 already in use`: 다른 Vite 서버가 실행 중입니다. 종료 후 재시도
- `Module not found`: `npm install`을 다시 실행해보세요

## 새 도메인 추가하기

### 1. 도메인 디렉토리 생성

```bash
mkdir -p server/app/domain/my_domain/{models,schemas,providers,calculators,formatters}
```

### 2. 각 컴포넌트 구현

```python
# server/app/domain/my_domain/providers/__init__.py
from server.app.shared.base import BaseProvider

class MyDataProvider(BaseProvider[MyInput, MyOutput]):
    async def provide(self, input_data: MyInput) -> MyOutput:
        # 데이터 조회 로직
        pass

# server/app/domain/my_domain/calculators/__init__.py
from server.app.shared.base import BaseCalculator

class MyCalculator(BaseCalculator[MyInput, MyOutput]):
    async def calculate(self, input_data: MyInput) -> MyOutput:
        # 계산 로직
        pass

# server/app/domain/my_domain/formatters/__init__.py
from server.app.shared.base import BaseFormatter

class MyFormatter(BaseFormatter[MyInput, MyOutput]):
    async def format(self, input_data: MyInput) -> MyOutput:
        # 포맷팅 로직
        pass

# server/app/domain/my_domain/service.py
from server.app.shared.base import BaseService

class MyDomainService(BaseService[MyRequest, MyResponse]):
    async def execute(self, request: MyRequest) -> ServiceResult[MyResponse]:
        # Provider, Calculator, Formatter 조율
        pass
```

### 3. API 엔드포인트 추가

```python
# server/app/api/v1/endpoints/my_domain.py
from fastapi import APIRouter

router = APIRouter(prefix="/my-domain", tags=["my-domain"])

@router.post("/action")
async def my_action(...):
    service = MyDomainService(db)
    result = await service.execute(request)
    return result.data
```

### 4. 라우터 등록

```python
# server/app/api/v1/router.py
from server.app.api.v1.endpoints import my_domain

api_router.include_router(my_domain.router)
```

## 테스트

```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=server --cov-report=html

# 특정 테스트만 실행
pytest tests/unit/
pytest tests/integration/

# 마커 사용
pytest -m unit
pytest -m integration
```

## 코드 품질

```bash
# 코드 포맷팅
black server/
isort server/

# 린팅
ruff check server/

# 타입 체크
mypy server/
```

## 배포

TODO: 배포 가이드 작성
- Docker 이미지 빌드
- 환경별 설정
- CI/CD 파이프라인

## 라이센스

MIT

## 기여

이슈와 PR을 환영합니다!

## 문의

문제가 있거나 질문이 있으시면 이슈를 등록해주세요.
