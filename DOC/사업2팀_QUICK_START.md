# 사업2팀 Quick Start Guide

> **AntiGravity(안티그래비티)**를 활용한 바이브코딩 환경 설정 가이드

---

## 목차

- [사전 준비사항](#사전-준비사항)
- [Step 1: GitHub에서 템플릿 받기](#step-1-github에서-템플릿-받기)
- [Step 2: 안티그래비티에서 프로젝트 열기](#step-2-안티그래비티에서-프로젝트-열기)
- [Step 3: 백엔드 실행](#step-3-백엔드-실행)
- [Step 4: 데이터베이스 설정 (Supabase)](#step-4-데이터베이스-설정-supabase)
- [Step 5: 프론트엔드 실행](#step-5-프론트엔드-실행)
- [실행 확인](#실행-확인)
- [문제 해결](#문제-해결)

---

## 사전 준비사항

시작하기 전에 다음을 준비하세요:

| 필요한 것 | 설명 | 링크 |
|-----------|------|------|
| **GitHub 계정** | 템플릿을 복사하기 위해 필요 | [GitHub 가입](https://github.com) |
| **Git** | 코드 버전 관리 도구 | [다운로드](https://git-scm.com/downloads) |
| **AntiGravity** | AI 바이브코딩 에디터 | 회사에서 제공 |
| **Python 3.12** | 백엔드 실행용 | [다운로드](https://www.python.org/downloads/) |
| **Node.js 18+** | 프론트엔드 실행용 | [다운로드](https://nodejs.org/) |
| **Supabase 계정** | 데이터베이스 (무료) | [무료 가입](https://supabase.com) |

### 설치 확인 방법

설치 후 터미널(명령 프롬프트 또는 PowerShell)에서 다음 명령어로 확인:

```bash
# Git 설치 확인
git --version
# 예상 출력: git version 2.43.0 (버전 숫자는 다를 수 있음)

# Python 설치 확인
python --version
# 또는
python3 --version
# 예상 출력: Python 3.12.x

# Node.js 설치 확인
node --version
# 예상 출력: v18.x.x 또는 v20.x.x

# npm 설치 확인 (Node.js와 함께 자동 설치됨)
npm --version
# 예상 출력: 9.x.x 또는 10.x.x
```

> **"command not found" 에러가 나오면?**
> - 해당 프로그램이 설치되지 않았거나
> - 설치 후 터미널을 재시작하지 않았습니다
> - 터미널을 닫았다가 다시 열어보세요!

### 설치 팁

**Windows 사용자:**
- Python 설치 시 **"Add Python to PATH"** 체크박스 반드시 선택!
- Node.js 설치 시 기본 옵션 그대로 진행
---

## Step 1: GitHub에서 템플릿 받기

### 1-1. GitHub 로그인

1. [https://github.com](https://github.com) 에 접속
2. 우측 상단 `Sign in` 클릭하여 로그인

### 1-2. 템플릿 레포지토리로 이동

1. 다음 주소로 이동:
   **https://github.com/KYUNGHOVNTG/vibe-web-starter.git**

### 1-3. "Use this template"로 내 레포지토리 생성

1. 초록색 **`Use this template`** 버튼 클릭
2. **`Create a new repository`** 선택

   ![Use this template](https://docs.github.com/assets/cb-77734/mw-1440/images/help/repository/use-this-template-button.webp)

3. Repository 설정:
   - **Repository name**: 원하는 프로젝트 이름 입력 (예: `my-web-project`)
   - **Description**: 프로젝트 설명 (선택사항)
   - **Public/Private**: 원하는 공개 설정 선택

4. **`Create repository`** 버튼 클릭

5. 잠시 기다리면 내 계정에 새 레포지토리가 생성됩니다!

### 1-4. 내 레포지토리 URL 복사

1. 생성된 레포지토리 페이지에서 초록색 **`<> Code`** 버튼 클릭
2. **HTTPS** 탭에서 URL 복사 (예: `https://github.com/내아이디/my-web-project.git`)

---

## Step 2: 안티그래비티에서 프로젝트 열기

### 2-1. 안티그래비티 실행

1. 안티그래비티(AntiGravity) 프로그램 실행

### 2-2. Git Clone으로 프로젝트 가져오기

**방법 A: 메뉴에서 Clone**

1. 상단 메뉴에서 `File` > `Clone Repository...` 클릭
2. 또는 단축키: `Ctrl + Shift + G` (Windows) / `Cmd + Shift + G` (Mac)
3. 복사한 URL 붙여넣기
4. 저장할 폴더 선택 (예: `C:\Projects` 또는 `~/Projects`)
5. `Clone` 버튼 클릭

**방법 B: 터미널에서 Clone**

1. 안티그래비티 터미널 열기 (`` Ctrl + ` `` 또는 `View` > `Terminal`)
2. 다음 명령어 실행:

```bash
# 원하는 폴더로 이동
cd ~/Projects  # Mac/Linux
cd C:\Projects  # Windows

# Git Clone
git clone https://github.com/내아이디/my-web-project.git

# 프로젝트 폴더로 이동
cd my-web-project
```

### 2-3. 프로젝트 열기

Clone이 완료되면:

1. `File` > `Open Folder...` 클릭
2. Clone한 폴더 선택 (예: `my-web-project`)
3. 프로젝트가 열리면 좌측에 파일 목록이 표시됩니다

---

## Step 3: 백엔드 실행

### 3-1. 터미널 열기

안티그래비티에서 터미널을 엽니다:
- 단축키: `` Ctrl + ` `` (Windows) / `` Cmd + ` `` (Mac)
- 또는 메뉴: `View` > `Terminal`

### 3-2. Python 가상환경 설정

```bash
# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

> **Windows에서 보안 오류 발생 시**:
> PowerShell을 관리자 권한으로 실행 후:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### 3-3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3-4. 환경 변수 설정

```bash
# .env 파일 생성 (템플릿 복사)
cp .env.example .env
```

> `.env` 파일은 다음 단계(데이터베이스 설정)에서 수정합니다.

---

## Step 4: 데이터베이스 설정 (Supabase)

### 4-1. Supabase 프로젝트 생성

1. [https://supabase.com](https://supabase.com) 접속 및 로그인
2. `New Project` 클릭
3. 설정 입력:
   - **Name**: 프로젝트 이름
   - **Database Password**: 비밀번호 입력 (반드시 기억!)
   - **Region**: `Northeast Asia (Seoul)` 선택
4. `Create new project` 클릭
5. 2-3분 대기 (프로젝트 생성 중...)

### 4-2. Connection String 복사

1. 좌측 메뉴에서 `Settings` > `Database` 클릭
2. `Connection string` 섹션에서:
   - **Mode**: `Transaction` 선택
   - URI 형식의 문자열 복사

### 4-3. .env 파일 수정

안티그래비티에서 `.env` 파일을 열고 `DATABASE_URL`을 수정:

```bash
# 복사한 Connection String 붙여넣기
# 주의: postgresql:// → postgresql+asyncpg:// 로 변경!

DATABASE_URL=postgresql+asyncpg://postgres.xxxxx:비밀번호@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres
```

> **비밀번호에 특수문자가 있다면 URL 인코딩 필요!**
> - `!` → `%21`
> - `@` → `%40`
> - `#` → `%23`

### 4-4. 초기 테이블 생성

1. Supabase Dashboard > `SQL Editor` 클릭
2. `New query` 클릭
3. 프로젝트의 `supabase_schema.sql` 파일 내용 복사하여 붙여넣기
4. `Run` 버튼 클릭

---

## Step 5: 프론트엔드 실행

### 5-1. 새 터미널 열기

안티그래비티에서 새 터미널을 엽니다:
- 터미널 패널에서 `+` 버튼 클릭

### 5-2. 프론트엔드 폴더로 이동

```bash
cd client
```

### 5-3. 의존성 설치

```bash
npm install
```

### 5-4. 개발 서버 실행

```bash
npm run dev
```

---

## 실행 확인

모든 설정이 완료되면 다음 URL에서 확인:

| 서비스 | URL | 설명 |
|--------|-----|------|
| **프론트엔드** | http://localhost:3000 | 웹 애플리케이션 |
| **백엔드 API** | http://localhost:8000 | FastAPI 서버 |
| **API 문서** | http://localhost:8000/docs | Swagger UI |

### 백엔드 실행 명령어 (참고)

백엔드 터미널에서:
```bash
python -m server.main
```

---

## 문제 해결

### "command not found: python3"
→ Python이 설치되지 않았습니다. [Python 다운로드](https://www.python.org/downloads/)

### "command not found: npm"
→ Node.js가 설치되지 않았습니다. [Node.js 다운로드](https://nodejs.org/)

### "Database connection error"
→ `.env` 파일의 `DATABASE_URL` 확인:
1. `postgresql+asyncpg://` 로 시작하는지 확인
2. 비밀번호 특수문자 URL 인코딩 확인
3. Supabase 프로젝트가 활성화 상태인지 확인

### "Port already in use"
→ 이미 다른 프로그램이 해당 포트를 사용 중:
- 기존 터미널 종료 후 다시 실행
- 또는 다른 포트 사용

### 가상환경 활성화 안 됨 (Windows)
→ PowerShell 실행 정책 변경:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 다음 단계

설치가 완료되었다면:

1. **[사업2팀_개발팁.md](./사업2팀_개발팁.md)** - 바이브코딩 핵심 팁
2. **[../common/DEVELOPMENT_GUIDE.md](../common/DEVELOPMENT_GUIDE.md)** - 개발 가이드
3. **[../common/ARCHITECTURE.md](../common/ARCHITECTURE.md)** - 아키텍처 이해

---

**Happy Vibe Coding!**