# ⚛️ 프론트엔드 (React 19 + Vite + TypeScript) 개발 가이드

> React 19 + Vite + TypeScript + Tailwind CSS 4 + Zustand 기반의 모던 웹 애플리케이션

---

## 📖 목차

- [아키텍처 개요](#-아키텍처-개요)
- [프로젝트 구조](#-프로젝트-구조)
- [React 19 컴포넌트 설계 원칙](#-react-19-컴포넌트-설계-원칙)
- [Zustand 상태 관리 전략](#-zustand-상태-관리-전략)
- [Tailwind CSS 4 스타일 규칙](#-tailwind-css-4-스타일-규칙)
- [API 통신 모듈 사용법](#-api-통신-모듈-사용법)
- [커스텀 훅 활용](#-커스텀-훅-활용)
- [도메인 기능 추가 가이드](#-도메인-기능-추가-가이드)
- [라우팅 & 네비게이션](#-라우팅--네비게이션)
- [빌드 & 배포](#-빌드--배포)

---

## 🏗️ 아키텍처 개요

### 핵심 설계 원칙

1. **도메인 기반 구조**: 백엔드 도메인과 1:1 대응되는 프론트엔드 도메인 구조
2. **컴포넌트 재사용성**: `core/ui/` 에 재사용 가능한 기본 UI 컴포넌트 분리
3. **상태 관리 분산**: 전역 상태(Auth) + 도메인별 상태(Zustand) 분리
4. **타입 안전성**: TypeScript로 컴파일 타임 에러 방지
5. **API 레이어 추상화**: Axios 싱글톤 + 도메인별 API 모듈로 분리
6. **전역 에러/로딩 처리**: ErrorBoundary + LoadingManager로 사용자 경험 향상

### 기술 스택

- **UI Framework**: React 19.2.0 (Concurrent Features, Automatic Batching)
- **Build Tool**: Vite 7.2.4 (빠른 HMR, 최적화된 프로덕션 빌드)
- **Language**: TypeScript 5.9.3
- **Styling**: Tailwind CSS 4.1.18 (유틸리티 우선 CSS)
- **State Management**: Zustand 5.0.9 (경량 상태 관리)
- **HTTP Client**: Axios 1.13.2
- **Animation**: Framer Motion 12.25.0
- **Icons**: Lucide React 0.562.0
- **Routing**: React Router DOM 7.12.0

---

## 📂 프로젝트 구조

```
client/
├── src/
│   ├── main.tsx                     # React 진입점 (ReactDOM.render)
│   ├── App.tsx                      # 메인 앱 컴포넌트 (랜딩 페이지)
│   ├── index.css                    # 전역 스타일 + Tailwind 지시자
│   │
│   ├── 📁 core/                     # 🔧 핵심 인프라
│   │   ├── 📁 api/                  # API 클라이언트
│   │   │   ├── client.ts            # Axios 싱글톤 (ApiClient)
│   │   │   ├── types.ts             # API 응답 타입
│   │   │   └── index.ts             # 내보내기
│   │   ├── 📁 errors/               # 에러 처리
│   │   │   ├── ErrorBoundary.tsx    # React Error Boundary
│   │   │   ├── ErrorFallback.tsx    # 에러 Fallback UI
│   │   │   ├── ApiErrorHandler.ts   # API 에러 핸들러
│   │   │   └── index.ts
│   │   ├── 📁 loading/              # 로딩 처리
│   │   │   ├── LoadingOverlay.tsx   # 전역 로딩 오버레이
│   │   │   ├── LoadingManager.ts    # 로딩 상태 관리
│   │   │   └── index.ts
│   │   ├── 📁 hooks/                # 커스텀 훅
│   │   │   ├── useApi.ts            # API 호출 훅 (로딩, 에러 처리)
│   │   │   ├── useDebounce.ts       # 디바운스 훅
│   │   │   └── index.ts
│   │   ├── 📁 layout/               # 레이아웃 컴포넌트
│   │   │   ├── MainLayout.tsx       # 메인 레이아웃 (Header + Sidebar + Content)
│   │   │   ├── Header.tsx           # 헤더 (네비게이션, 사용자 메뉴)
│   │   │   ├── Sidebar.tsx          # 사이드바 (메뉴)
│   │   │   └── index.ts
│   │   ├── 📁 store/                # 전역 상태 (Zustand)
│   │   │   ├── useAuthStore.ts      # 인증 상태 (사용자, 토큰)
│   │   │   └── index.ts
│   │   ├── 📁 ui/                   # 재사용 UI 컴포넌트
│   │   │   ├── Button.tsx           # 버튼 (primary, secondary, danger)
│   │   │   ├── Card.tsx             # 카드 컨테이너
│   │   │   ├── Input.tsx            # 입력 필드
│   │   │   ├── Modal.tsx            # 모달 다이얼로그
│   │   │   └── index.ts
│   │   └── index.ts                 # core 모듈 통합 내보내기
│   │
│   ├── 📁 domains/                  # 🎯 도메인별 기능 (백엔드 미러링)
│   │   └── sample/                  # 샘플 도메인 (예시)
│   │       ├── api.ts               # API 호출 함수 (fetchSampleItems, createSampleItem)
│   │       ├── store.ts             # Zustand 스토어 (useSampleStore)
│   │       ├── types.ts             # TypeScript 타입 (SampleItem, SampleRequest)
│   │       ├── 📁 components/       # 도메인 전용 컴포넌트
│   │       │   ├── SampleForm.tsx   # 샘플 폼
│   │       │   ├── SampleList.tsx   # 샘플 리스트
│   │       │   └── index.ts
│   │       ├── 📁 pages/            # 도메인 페이지 (라우팅 대상)
│   │       │   ├── SamplePage.tsx   # 샘플 메인 페이지
│   │       │   └── index.ts
│   │       ├── README.md            # 도메인 문서 (선택)
│   │       └── index.ts
│   │
│   ├── 📁 types/                    # 전역 TypeScript 타입
│   │   └── index.ts
│   │
│   └── 📁 assets/                   # 정적 자산 (이미지, 아이콘)
│
├── 📁 public/                       # 정적 파일 (favicon, robots.txt)
│
├── package.json                     # npm 의존성
├── package-lock.json
├── vite.config.ts                   # Vite 설정 (프록시, 플러그인)
├── tsconfig.json                    # TypeScript 베이스 설정
├── tsconfig.app.json                # 앱 TypeScript 설정
├── tsconfig.node.json               # Node 도구 TypeScript 설정
├── tailwind.config.js               # Tailwind CSS 설정
├── postcss.config.js                # PostCSS 설정
├── eslint.config.mjs                # ESLint 설정
└── .env.example                     # 환경 변수 예시
```

---

## 🛡️ 에러 & 로딩 처리

### 1. 전역 에러 처리 (ErrorBoundary)

**파일**: `client/src/core/errors/ErrorBoundary.tsx`

```tsx
/**
 * React Error Boundary로 컴포넌트 에러 포착
 *
 * main.tsx에서 사용:
 *    <ErrorBoundary>
 *      <App />
 *    </ErrorBoundary>
 *
 * 기능:
 *    - 컴포넌트 렌더링 중 에러 포착
 *    - 에러 Fallback UI 표시
 *    - 에러 로깅 (Sentry 등 연동 가능)
 *    - "다시 시도" 기능 제공
 *
 * 주의사항:
 *    Error Boundary는 다음 에러를 포착하지 못합니다:
 *    - 이벤트 핸들러 내부 에러 (try-catch 사용)
 *    - 비동기 코드 (setTimeout, Promise)
 *    - SSR 에러
 */
```

### 2. 전역 로딩 상태 (LoadingOverlay)

**파일**: `client/src/core/loading/LoadingOverlay.tsx`

```tsx
/**
 * 전역 로딩 오버레이 컴포넌트
 *
 * App.tsx에서 사용:
 *    <LoadingOverlay />
 *
 * 사용 예시:
 *    import { LoadingManager } from '@/core/loading';
 *
 *    const handleSubmit = async () => {
 *      LoadingManager.show('데이터를 저장하는 중...');
 *      try {
 *        await api.saveData(data);
 *      } finally {
 *        LoadingManager.hide();
 *      }
 *    };
 *
 * 기능:
 *    - API 요청 중 사용자 피드백 제공
 *    - 스피너 + 커스텀 메시지 표시
 *    - LoadingManager로 show/hide 제어
 *    - 전체 화면 오버레이
 */
```

### 3. API 에러 처리

**파일**: `client/src/core/errors/ApiErrorHandler.ts`

```typescript
/**
 * API 에러를 사용자 친화적인 메시지로 변환
 *
 * HTTP 상태 코드별 처리:
 *    - 400: 잘못된 요청 (입력 검증 실패)
 *    - 401: 인증 필요 (로그인 필요)
 *    - 403: 권한 없음 (접근 거부)
 *    - 404: 리소스 없음
 *    - 500: 서버 오류
 *
 * 사용 예시:
 *    try {
 *      await api.fetchData();
 *    } catch (error) {
 *      const message = handleApiError(error);
 *      toast.error(message);
 *    }
 */
```

### 4. 사용 패턴 비교

```tsx
// ✅ 권장: LoadingManager 사용 (전역 로딩)
import { LoadingManager } from '@/core/loading';

const handleSubmit = async () => {
  LoadingManager.show('저장 중...');
  try {
    await api.saveData(data);
  } finally {
    LoadingManager.hide();
  }
};

// ✅ 권장: useApi 훅 사용 (컴포넌트 레벨)
const { loading, execute } = useApi(api.fetchData);

useEffect(() => {
  execute();
}, []);

if (loading) return <Spinner />;

// ❌ 금지: 컴포넌트별 로딩 상태 남발
const [loading, setLoading] = useState(false);  // 여러 곳에서 중복
```

---

## ⚛️ React 19 컴포넌트 설계 원칙

### 1. 컴포넌트 분류

#### a) 재사용 가능한 UI 컴포넌트 (`core/ui/`)

**목적**: 프로젝트 전체에서 재사용 가능한 기본 UI 요소

**예시**: `Button.tsx`

```tsx
import React from 'react';
import { cn } from '@/utils/cn'; // Tailwind 클래스 병합 유틸리티

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        (disabled || isLoading) && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      )}
      {children}
    </button>
  );
};
```

**핵심 규칙**:
- ✅ **완전히 재사용 가능**: 어떤 도메인에도 의존하지 않음
- ✅ **TypeScript Props 정의**: 명시적 인터페이스
- ✅ **Tailwind CSS 사용**: 일관된 스타일 시스템
- ✅ **접근성(Accessibility)**: ARIA 속성, 키보드 네비게이션
- ❌ **비즈니스 로직 금지**: 오직 UI 표현만

#### b) 레이아웃 컴포넌트 (`core/layout/`)

**목적**: 페이지의 공통 구조 (헤더, 사이드바, 푸터)

**예시**: `MainLayout.tsx`

```tsx
import React from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
};
```

#### c) 도메인 전용 컴포넌트 (`domains/{domain}/components/`)

**목적**: 특정 도메인의 비즈니스 로직을 포함한 컴포넌트

**예시**: `SampleForm.tsx`

```tsx
import React from 'react';
import { Button, Input, Card } from '@/core/ui';
import { useSampleStore } from '../store';
import { createSampleItem } from '../api';

export const SampleForm: React.FC = () => {
  const [name, setName] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const { addItem } = useSampleStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const newItem = await createSampleItem({ name, description: '' });
      addItem(newItem);
      setName(''); // 폼 초기화
    } catch (error) {
      console.error('Failed to create item:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="이름"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="샘플 이름 입력"
          required
        />
        <Button type="submit" isLoading={loading}>
          생성
        </Button>
      </form>
    </Card>
  );
};
```

**핵심 규칙**:
- ✅ **도메인 스토어 사용**: `useSampleStore()` 훅 활용
- ✅ **도메인 API 호출**: `createSampleItem()` 호출
- ✅ **재사용 UI 컴포넌트 조합**: `Button`, `Input`, `Card` 사용
- ❌ **다른 도메인 의존 금지**: 도메인 간 독립성 유지

#### d) 페이지 컴포넌트 (`domains/{domain}/pages/`)

**목적**: 라우팅 대상이 되는 최상위 컴포넌트

**예시**: `SamplePage.tsx`

```tsx
import React, { useEffect } from 'react';
import { MainLayout } from '@/core/layout';
import { SampleForm } from '../components/SampleForm';
import { SampleList } from '../components/SampleList';
import { useSampleStore } from '../store';
import { fetchSampleItems } from '../api';

export const SamplePage: React.FC = () => {
  const { setItems, setLoading, setError } = useSampleStore();

  useEffect(() => {
    const loadItems = async () => {
      setLoading(true);
      try {
        const items = await fetchSampleItems();
        setItems(items);
      } catch (error) {
        setError(error instanceof Error ? error.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    loadItems();
  }, [setItems, setLoading, setError]);

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">샘플 관리</h1>
        <SampleForm />
        <SampleList />
      </div>
    </MainLayout>
  );
};
```

**핵심 규칙**:
- ✅ **데이터 로딩**: `useEffect`로 초기 데이터 로드
- ✅ **레이아웃 적용**: `MainLayout`으로 감싸기
- ✅ **컴포넌트 조합**: 하위 컴포넌트 조합으로 구성
- ❌ **복잡한 비즈니스 로직 금지**: 하위 컴포넌트로 위임

---

## 🗃️ Zustand 상태 관리 전략

### 1. 전역 상태 vs 도메인 상태

| 상태 종류 | 위치 | 예시 |
|----------|------|------|
| **전역 상태** | `core/store/` | 인증(Auth), 테마, 언어 설정 |
| **도메인 상태** | `domains/{domain}/store.ts` | 도메인별 데이터, 로딩, 에러 |

### 2. 전역 상태: `useAuthStore`

**위치**: `core/store/useAuthStore.ts`

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  email: string;
  username: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;

  // Actions
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (user, token) =>
        set({
          user,
          token,
          isAuthenticated: true,
        }),

      logout: () =>
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        }),

      updateUser: (updatedUser) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...updatedUser } : null,
        })),
    }),
    {
      name: 'auth-storage', // localStorage 키
    }
  )
);
```

**사용 예시**:

```tsx
import { useAuthStore } from '@/core/store';

export const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <header>
      {isAuthenticated ? (
        <>
          <span>환영합니다, {user?.username}님</span>
          <button onClick={logout}>로그아웃</button>
        </>
      ) : (
        <a href="/login">로그인</a>
      )}
    </header>
  );
};
```

### 3. 도메인 상태: `useSampleStore`

**위치**: `domains/sample/store.ts`

```typescript
import { create } from 'zustand';
import { SampleItem } from './types';

interface SampleState {
  items: SampleItem[];
  selectedItem: SampleItem | null;
  loading: boolean;
  error: string | null;

  // Actions
  setItems: (items: SampleItem[]) => void;
  addItem: (item: SampleItem) => void;
  updateItem: (id: number, updates: Partial<SampleItem>) => void;
  deleteItem: (id: number) => void;
  selectItem: (item: SampleItem | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useSampleStore = create<SampleState>((set) => ({
  items: [],
  selectedItem: null,
  loading: false,
  error: null,

  setItems: (items) => set({ items }),

  addItem: (item) =>
    set((state) => ({
      items: [...state.items, item],
    })),

  updateItem: (id, updates) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.id === id ? { ...item, ...updates } : item
      ),
    })),

  deleteItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),

  selectItem: (item) => set({ selectedItem: item }),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),
}));
```

**핵심 규칙**:
- ✅ **도메인별 독립 스토어**: 각 도메인은 자체 스토어 사용
- ✅ **불변성 유지**: `set((state) => ({ ...state, ... }))` 패턴
- ✅ **명시적 액션**: getter/setter 명확히 분리
- ❌ **전역 상태 남용 금지**: 필요한 경우에만 전역 상태 사용

---

## 🎨 Tailwind CSS 4 스타일 규칙

### 1. 기본 설정

**파일**: `tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          // ... (커스텀 색상)
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

### 2. 스타일 가이드라인

#### a) 반응형 디자인

```tsx
<div className="
  w-full              /* 모바일: 전체 너비 */
  md:w-1/2            /* 태블릿: 50% 너비 */
  lg:w-1/3            /* 데스크톱: 33% 너비 */
  px-4                /* 수평 패딩 */
  py-2                /* 수직 패딩 */
">
  {/* 콘텐츠 */}
</div>
```

#### b) 다크 모드 대응 (추후 구현)

```tsx
<div className="
  bg-white            /* 라이트 모드 */
  dark:bg-gray-900    /* 다크 모드 */
  text-gray-900
  dark:text-gray-100
">
  {/* 콘텐츠 */}
</div>
```

#### c) 호버 & 포커스 상태

```tsx
<button className="
  bg-blue-600
  hover:bg-blue-700          /* 마우스 오버 */
  active:bg-blue-800         /* 클릭 중 */
  focus:outline-none         /* 기본 아웃라인 제거 */
  focus:ring-2               /* 커스텀 링 */
  focus:ring-blue-500        /* 링 색상 */
  focus:ring-offset-2        /* 링 오프셋 */
  transition-colors          /* 부드러운 전환 */
  duration-200               /* 전환 시간 */
">
  클릭하세요
</button>
```

#### d) 레이아웃 유틸리티

```tsx
{/* Flexbox */}
<div className="flex items-center justify-between gap-4">
  {/* 아이템들 */}
</div>

{/* Grid */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* 아이템들 */}
</div>

{/* 중앙 정렬 */}
<div className="flex items-center justify-center min-h-screen">
  {/* 중앙 콘텐츠 */}
</div>
```

**핵심 규칙**:
- ✅ **Tailwind 유틸리티 우선**: 커스텀 CSS 최소화
- ✅ **일관된 네이밍**: 색상, 간격, 폰트 크기는 Tailwind 기본값 사용
- ✅ **반응형 디자인**: `sm:`, `md:`, `lg:`, `xl:` 접두사 활용
- ❌ **인라인 스타일 금지**: `style={{ ... }}` 대신 Tailwind 클래스 사용
- ❌ **임의 값 남용 금지**: `w-[347px]` 대신 `w-80` 같은 표준 값 사용

---

## 🌐 API 통신 모듈 사용법

### 1. Axios 싱글톤 클라이언트

**위치**: `core/api/client.ts`

```typescript
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 요청 인터셉터 (토큰 자동 첨부)
    this.client.interceptors.request.use(
      (config) => {
        // TODO: Zustand에서 토큰 가져오기
        // const token = useAuthStore.getState().token;
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`;
        // }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 응답 인터셉터 (에러 핸들링)
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // TODO: 로그아웃 처리
          // useAuthStore.getState().logout();
          // window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config);
    return response.data;
  }
}

// 싱글톤 인스턴스 내보내기
export const apiClient = new ApiClient();
```

### 2. 도메인별 API 모듈

**위치**: `domains/sample/api.ts`

```typescript
import { apiClient } from '@/core/api/client';
import { SampleItem, SampleItemRequest } from './types';

/**
 * 샘플 아이템 목록 조회
 */
export async function fetchSampleItems(): Promise<SampleItem[]> {
  return apiClient.get<SampleItem[]>('/v1/sample/items');
}

/**
 * 샘플 아이템 생성
 */
export async function createSampleItem(data: SampleItemRequest): Promise<SampleItem> {
  return apiClient.post<SampleItem>('/v1/sample/items', data);
}

/**
 * 샘플 아이템 수정
 */
export async function updateSampleItem(
  id: number,
  data: Partial<SampleItemRequest>
): Promise<SampleItem> {
  return apiClient.put<SampleItem>(`/v1/sample/items/${id}`, data);
}

/**
 * 샘플 아이템 삭제
 */
export async function deleteSampleItem(id: number): Promise<void> {
  return apiClient.delete<void>(`/v1/sample/items/${id}`);
}
```

**핵심 규칙**:
- ✅ **도메인별 API 파일 분리**: `domains/{domain}/api.ts`
- ✅ **타입 안전성**: 모든 API 함수에 TypeScript 타입 지정
- ✅ **에러 핸들링**: try/catch로 컴포넌트에서 처리
- ❌ **직접 axios 호출 금지**: 반드시 `apiClient` 사용

---

## 🪝 커스텀 훅 활용

### 1. `useApi` - API 호출 훅

**위치**: `core/hooks/useApi.ts`

```typescript
import { useState, useCallback } from 'react';

interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  execute: (...args: any[]) => Promise<T | undefined>;
  reset: () => void;
}

/**
 * API 호출을 위한 커스텀 훅
 * 로딩, 에러, 데이터 상태를 자동 관리
 */
export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<T>
): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (...args: any[]) => {
      setLoading(true);
      setError(null);

      try {
        const result = await apiFunction(...args);
        setData(result);
        return result;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : '알 수 없는 오류';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
  }, []);

  return { data, loading, error, execute, reset };
}
```

### 2. `useDebounce` - 디바운스 훅

**위치**: `core/hooks/useDebounce.ts`

```typescript
import { useEffect, useState } from 'react';

/**
 * 값 변경을 지연시키는 디바운스 훅
 * (검색창 등에서 API 호출 최적화)
 */
export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

---

## 🎯 도메인 기능 추가 가이드

새로운 도메인 기능을 추가하는 단계별 가이드입니다. 예시: `payment` 도메인 추가

### 단계별 체크리스트

- [ ] **1단계**: 디렉토리 생성
- [ ] **2단계**: 타입 정의 (`types.ts`)
- [ ] **3단계**: API 모듈 작성 (`api.ts`)
- [ ] **4단계**: 상태 관리 (`store.ts`)
- [ ] **5단계**: 컴포넌트 작성 (`components/`)
- [ ] **6단계**: 페이지 작성 (`pages/`)
- [ ] **7단계**: 라우팅 등록

자세한 내용은 [Root README](../README.md)의 "도메인 플러그인 추가하기" 섹션을 참조하세요.

---

## 🚦 라우팅 & 네비게이션

### React Router DOM 설정

**파일**: `App.tsx`

```tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { SamplePage } from '@/domains/sample/pages';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/sample" replace />} />
        <Route path="/sample" element={<SamplePage />} />
        {/* 추가 라우트 */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

## 📦 빌드 & 배포

### 개발 서버 실행

```bash
npm run dev
```

### 프로덕션 빌드

```bash
npm run build
```

**결과물**: `dist/` 폴더에 최적화된 정적 파일 생성

### 프로덕션 미리보기

```bash
npm run preview
```

### 환경 변수

**파일**: `.env`

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

**주의**: Vite에서는 `VITE_` 접두사가 필요합니다!

---

## 📚 추가 리소스

- **[ARCHITECTURE.md](../ARCHITECTURE.md)**: 전체 아키텍처 문서
- **[DEVELOPMENT_GUIDE.md](../DEVELOPMENT_GUIDE.md)**: 도메인 추가 체크리스트
- **React 19 공식 문서**: https://react.dev/
- **Vite 공식 문서**: https://vitejs.dev/
- **Tailwind CSS 공식 문서**: https://tailwindcss.com/
- **Zustand 공식 문서**: https://zustand-demo.pmnd.rs/

---

**Happy Coding! 🎉**
