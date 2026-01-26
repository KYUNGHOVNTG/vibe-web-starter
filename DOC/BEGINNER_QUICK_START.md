# 🚀 빠른 시작 가이드 (Quick Start)

이 가이드는 웹 개발 입문자를 위해 작성되었습니다. 차근차근 따라 하시면 로컬 개발 환경을 완벽하게 구축할 수 있습니다.

## 📋 사전 준비사항

시작하기 전에 아래 도구들이 설치되어 있어야 합니다.
드라이브 링크 : https://drive.google.com/drive/folders/0AKGyePA4UPjQUk9PVA

* **Git**: [다운로드](https://git-scm.com/downloads)
* **Python 3.12**: [다운로드](https://www.python.org/downloads/) (설치 시 'Add Python to PATH' 체크 필수)
* **Node.js 18+**: [다운로드](https://nodejs.org/)
* **Cursor AI**: [다운로드](https://www.cursor.com/)

---

## 1️⃣ 프로젝트 열기 및 터미널 준비

가장 먼저 프로젝트 폴더를 **Cursor**에서 열고 터미널을 실행해야 합니다.

1. **프로젝트 폴더 열기**: Cursor 실행 후 `File` > `Open Folder`를 눌러 다운로드한 프로젝트 폴더를 선택합니다.
2. **터미널 열기**:
* 상단 메뉴바에서 **Terminal** > **New Terminal**을 클릭합니다.
* 화면 하단에 검은색 입력창(터미널)이 나타납니다. 앞으로 모든 명령어는 이곳에 입력합니다.



---

## 2️⃣ 백엔드(Backend) 설정

### 1. 가상환경 생성 및 활성화

터미널에 아래 명령어를 한 줄씩 복사해서 붙여넣고 Enter를 누르세요.

```bash
# 프로젝트 루트 폴더로 이동 (이미 폴더 안이라면 생략 가능)
cd project-name

# 1. Python 가상환경 생성
py -3.12 -m venv .venv

# 2. 가상환경 활성화 (Windows 기준)
.venv\Scripts\activate

```

> **⚠️ 여기서 '보안 오류'가 발생한다면?**
> 만약 `이 시스템에서 스크립트를 실행할 수 없으므로...` 라는 빨간색 오류가 뜬다면 아래 명령어를 입력한 후 다시 활성화를 시도하세요.
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 2. 의존성 설치 및 환경 변수 설정

```bash
# 3. 필요한 라이브러리 설치
pip install -r requirements.txt

# 4. 설정 파일 복사
cp .env.example .env

```

### 3. Supabase 데이터베이스 연결 (중요)

1. **프로젝트 생성**: [Supabase](https://supabase.com) 로그인 후 `New Project`를 생성합니다. (비밀번호는 꼭 메모해두세요!)
2. **테이블 생성**:
* 왼쪽 메뉴 `SQL Editor` > `New query` 클릭
* 프로젝트 폴더 내 `supabase_schema.sql` 파일의 내용을 전체 복사해서 붙여넣고 **Run** 클릭


3. **연결 문자열 복사**:
* `Settings` > `Database` > `Connection string` 메뉴 이동
* **Type**: `URI`, **Method**: `Transaction pooler` 선택 후 주소 복사


4. **.env 파일 수정**: Cursor에서 `.env` 파일을 열어 복사한 주소를 붙여넣습니다.
* **주의**: `postgresql://` 부분을 `postgresql+asyncpg://`로 바꿔야 합니다.
* **주의**: 비밀번호에 `@`, `#` 등 특수문자가 있다면 [Encoding](https://www.urlencoder.io/)을 해서 넣어야 합니다. (예: `! -> %21`)



---

## 3️⃣ 프론트엔드(Frontend) 설정

백엔드 터미널은 그대로 두고, **새 터미널**을 하나 더 엽니다 (Terminal > New Terminal).

```bash
# 1. client 폴더로 이동
cd client

# 2. 패키지 설치
npm install

```

---

## 4️⃣ 서버 실행하기 (평소 개발할 때)

세팅이 끝난 후, 나중에 다시 코딩을 시작할 때는 아래 명령어로 서버를 켭니다.

### **방법 A. 백엔드 서버 실행 (첫 번째 터미널)**

```bash
# 가상환경이 꺼져있다면 다시 활성화
.venv\Scripts\activate

# 서버 실행
python -m server.main

```

* 성공 시: `http://localhost:8000`에서 작동 중

### **방법 B. 프론트엔드 서버 실행 (두 번째 터미널)**

```bash
cd client
npm run dev

```

* 성공 시: `http://localhost:3000`에서 화면 확인 가능

---

## ✅ 최종 확인 리스트

설정이 완료되었다면 아래 주소들이 정상적으로 접속되는지 확인하세요.

| 서비스 | 주소 | 비고 |
| --- | --- | --- |
| **프론트엔드** | [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000) | 실제 화면 |
| **API 문서** | [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) | Swagger (백엔드 테스트) |
| **상태 점검** | [http://localhost:8000/core/health](https://www.google.com/search?q=http://localhost:8000/core/health) | "ok"가 나오면 정상 |

---

### 💡 팁

* **터미널 종료**: 터미널 창에서 `Ctrl + C`를 누르면 서버가 중단됩니다.
* **가상환경**: 백엔드 작업 시 터미널 줄 맨 앞에 `(.venv)`라는 표시가 있는지 항상 확인하세요.

---

**수정된 내용의 주요 포인트:**

1. **시각화 유도**: Cursor 메뉴 위치를 설명하고 이미지 태그를 추가해 시각적 이해를 돕도록 했습니다.
2. **보안 오류 해결**: PowerShell 정책 변경 명령어를 실제 상황에 맞게 배치했습니다.
3. **재실행 가이드**: 처음 세팅(Setup)과 일상적인 실행(Daily Run)을 구분하여 사용자가 혼란을 느끼지 않게 했습니다.
4. **Supabase 단계 구체화**: 초보자가 가장 많이 실수하는 `asyncpg` 드라이버 명시와 `URL 인코딩` 부분을 강조했습니다.

이 내용으로 `QUICKSTART.md`를 업데이트하시면 처음 프로젝트를 접하는 분들도 훨씬 수월하게 세팅하실 수 있을 거예요. 추가로 더 보완하고 싶은 부분이 있으신가요?