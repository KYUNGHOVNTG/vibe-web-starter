# 📘 Alembic 데이터베이스 마이그레이션 가이드

이 문서는 Alembic을 사용한 데이터베이스 스키마 관리 방법을 설명합니다.

---

## 🎯 핵심 원칙

### ✅ 반드시 지켜야 할 규칙

1. **모든 DB 스키마 변경은 Alembic 마이그레이션으로 관리**
   - 테이블 생성/수정/삭제
   - 컬럼 추가/수정/삭제
   - 인덱스, 제약조건 변경
   - 초기 데이터(seed data) 삽입

2. **DB 콘솔에서 직접 스키마 변경 금지**
   - Supabase SQL Editor 직접 사용 금지
   - pgAdmin, DBeaver 등에서 직접 ALTER TABLE 금지

3. **마이그레이션 파일은 Append-Only**
   - 기존 마이그레이션 파일 수정 금지
   - 변경이 필요하면 새 마이그레이션 생성

4. **모델과 마이그레이션 동기화 필수**
   - SQLAlchemy 모델 변경 시 반드시 마이그레이션 생성
   - 마이그레이션 적용 후 모델 코드도 업데이트

---

## 🚀 빠른 시작

### 초기 설정 (프로젝트 최초 1회)

```bash
# 1. Alembic 설치 확인 (requirements.txt에 포함됨)
pip install alembic

# 2. 현재 DB 상태를 초기 마이그레이션으로 생성
alembic revision --autogenerate -m "Initial schema"

# 3. 마이그레이션 적용
alembic upgrade head
```

### 일반적인 워크플로우

```bash
# 1. SQLAlchemy 모델 수정
# server/app/domain/{domain}/models/__init__.py 편집

# 2. 마이그레이션 생성
alembic revision --autogenerate -m "Add email column to user"

# 3. 생성된 마이그레이션 파일 검토
# alembic/versions/YYYYMMDD_HHMM_add_email_column_to_user.py

# 4. 마이그레이션 적용
alembic upgrade head

# 5. 롤백이 필요한 경우
alembic downgrade -1  # 1단계 롤백
```

---

## 📝 주요 명령어

### 마이그레이션 생성

```bash
# 자동 생성 (권장)
alembic revision --autogenerate -m "설명"

# 수동 생성 (빈 템플릿)
alembic revision -m "설명"
```

**파일명 예시:**
```
20260126_1430_add_email_column_to_user.py
```

### 마이그레이션 적용

```bash
# 최신 버전으로 업그레이드
alembic upgrade head

# 특정 버전으로 업그레이드
alembic upgrade <revision_id>

# 1단계씩 업그레이드
alembic upgrade +1
```

### 마이그레이션 롤백

```bash
# 1단계 롤백
alembic downgrade -1

# 특정 버전으로 롤백
alembic downgrade <revision_id>

# 전체 롤백 (주의!)
alembic downgrade base
```

### 상태 확인

```bash
# 현재 적용된 마이그레이션 확인
alembic current

# 마이그레이션 히스토리 확인
alembic history

# 적용 예정인 마이그레이션 확인
alembic show head
```

---

## 🔧 실전 예제

### 예제 1: 새 테이블 생성

**1단계: SQLAlchemy 모델 작성**

```python
# server/app/domain/product/models/__init__.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from server.app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default="now()")
```

**2단계: 마이그레이션 생성**

```bash
alembic revision --autogenerate -m "Create product table"
```

**3단계: 생성된 파일 검토**

```python
# alembic/versions/20260126_1430_create_product_table.py
def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
```

**4단계: 적용**

```bash
alembic upgrade head
```

---

### 예제 2: 컬럼 추가

**1단계: 모델 수정**

```python
# server/app/domain/user/models/__init__.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)  # 새로 추가
```

**2단계: 마이그레이션 생성 및 적용**

```bash
alembic revision --autogenerate -m "Add email to user"
alembic upgrade head
```

---

### 예제 3: 초기 데이터 삽입

**1단계: 마이그레이션 생성**

```bash
alembic revision -m "Seed initial roles"
```

**2단계: 수동으로 데이터 삽입 코드 작성**

```python
# alembic/versions/20260126_1500_seed_initial_roles.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

def upgrade() -> None:
    # Define table structure for data insertion
    roles_table = table(
        'roles',
        column('id', sa.Integer),
        column('name', sa.String),
        column('description', sa.String)
    )
    
    # Insert initial data
    op.bulk_insert(
        roles_table,
        [
            {'id': 1, 'name': 'admin', 'description': 'Administrator'},
            {'id': 2, 'name': 'user', 'description': 'Regular User'},
            {'id': 3, 'name': 'guest', 'description': 'Guest User'},
        ]
    )

def downgrade() -> None:
    # Delete seeded data
    op.execute("DELETE FROM roles WHERE id IN (1, 2, 3)")
```

**3단계: 적용**

```bash
alembic upgrade head
```

---

## 🏭 운영 환경 전략

### 배포 전 체크리스트

- [ ] 로컬 환경에서 마이그레이션 테스트 완료
- [ ] 롤백 테스트 완료 (`downgrade` 동작 확인)
- [ ] 마이그레이션 파일 코드 리뷰 완료
- [ ] 데이터 손실 가능성 검토 (DROP, ALTER 등)
- [ ] 대용량 테이블의 경우 실행 시간 예측

### 운영 배포 절차

```bash
# 1. 현재 DB 상태 백업
pg_dump -h <host> -U <user> -d <database> > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. 현재 마이그레이션 버전 확인
alembic current

# 3. 적용 예정 마이그레이션 확인
alembic history

# 4. 마이그레이션 적용
alembic upgrade head

# 5. 문제 발생 시 롤백
alembic downgrade -1
```

### 무중단 배포 전략

**대용량 테이블 변경 시:**

1. **컬럼 추가**: NULL 허용으로 먼저 추가 → 데이터 마이그레이션 → NOT NULL 제약조건 추가
2. **컬럼 삭제**: 애플리케이션에서 사용 중단 → 배포 → 일정 기간 후 컬럼 삭제
3. **인덱스 추가**: `CONCURRENTLY` 옵션 사용 (PostgreSQL)

```python
# 예: 동시성 인덱스 생성
def upgrade() -> None:
    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        postgresql_concurrently=True
    )
```

---

## ⚠️ 주의사항

### 하지 말아야 할 것

1. **운영 DB에서 직접 스키마 변경**
   ```sql
   -- ❌ 절대 금지
   ALTER TABLE users ADD COLUMN email VARCHAR(255);
   ```

2. **적용된 마이그레이션 파일 수정**
   ```python
   # ❌ 이미 적용된 파일은 수정 금지
   # alembic/versions/20260120_1000_create_user.py
   ```

3. **마이그레이션 파일 삭제**
   ```bash
   # ❌ 금지
   rm alembic/versions/20260120_1000_create_user.py
   ```

### 해야 할 것

1. **변경이 필요하면 새 마이그레이션 생성**
   ```bash
   # ✅ 권장
   alembic revision --autogenerate -m "Fix user table schema"
   ```

2. **마이그레이션 전 백업**
   ```bash
   # ✅ 필수
   pg_dump ... > backup.sql
   ```

3. **롤백 테스트**
   ```bash
   # ✅ 배포 전 반드시 테스트
   alembic upgrade head
   alembic downgrade -1
   alembic upgrade head
   ```

---

## 🐛 문제 해결

### 문제: "Target database is not up to date"

**원인:** 다른 개발자가 생성한 마이그레이션이 있음

**해결:**
```bash
git pull
alembic upgrade head
```

### 문제: "Can't locate revision identified by 'xxxxx'"

**원인:** 마이그레이션 파일이 누락됨

**해결:**
```bash
# 1. Git에서 누락된 파일 복구
git checkout main -- alembic/versions/

# 2. 마이그레이션 재적용
alembic upgrade head
```

### 문제: 자동 생성이 변경사항을 감지하지 못함

**원인:** 모델이 `env.py`에 import되지 않음

**해결:**
```python
# alembic/env.py
from server.app.domain.user.models import User  # 추가
from server.app.domain.product.models import Product  # 추가
```

---

## 📚 추가 참고 자료

- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [DOC/DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md) - 전체 개발 가이드

---

## 🤖 AI 에이전트 규칙

**Cursor/Claude AI가 DB 변경 시 따라야 할 규칙:**

1. **DB 스키마 변경이 필요한 경우:**
   - 사용자에게 마이그레이션 생성 안내
   - 마이그레이션 파일 내용 제시
   - 사용자 확인 후 파일 생성

2. **모델 변경 시:**
   - SQLAlchemy 모델 수정
   - Alembic 마이그레이션 생성 명령어 제시
   - Repository 코드 업데이트

3. **절대 하지 말 것:**
   - DB 콘솔 직접 실행 제안 금지
   - 기존 마이그레이션 파일 수정 금지
   - 마이그레이션 없이 모델만 변경 금지

---

**이 가이드를 따르면 안전하고 추적 가능한 데이터베이스 관리가 가능합니다! 🎉**
