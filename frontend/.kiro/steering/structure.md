# Project Structure & Architecture

## Folder Organization

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components (Button, Card, Dialog, etc.)
│   └── *.tsx           # App-specific components (Logo, PageRoot, etc.)
├── features/           # Feature-based modules
│   ├── auth/           # Authentication (login, register, API, queries)
│   ├── jobs/           # Job listings (CRUD, types, components)
│   ├── company/        # Company information
│   ├── profile/        # User profiles
│   ├── layout/         # Layout components (Nav, etc.)
│   └── roadmap/        # Career roadmaps
├── lib/                # Shared utilities and configuration
│   ├── api-util.ts     # API response helpers
│   ├── query-client.tsx # TanStack Query setup
│   ├── router.tsx      # React Router configuration
│   └── utils.ts        # General utilities
└── main.tsx            # Application entry point
```

## Feature Module Pattern

Each feature follows a consistent structure:
- `*.api.ts` - API functions using Axios
- `*.query.ts` - TanStack Query hooks
- `*.mutation.ts` - TanStack Query mutations
- `*.types.ts` - TypeScript interfaces
- `*.page.tsx` - Page components
- `*-card.tsx` - Card/list item components
- `*-dialog.tsx` - Modal/dialog components

## Component Conventions

- Use `@/` path alias for imports from `src/`
- UI components use CVA for variants and styling
- All components are functional with TypeScript
- Props interfaces defined inline or in separate types files
- Consistent naming: PascalCase for components, kebab-case for files

## API Layer

- Centralized API functions in `*.api.ts` files
- Consistent error handling using `success()` helper
- Type-safe responses with TypeScript interfaces
- RESTful endpoint patterns (`/api/resource`)

## State Management

- Server state: TanStack Query for caching and synchronization
- Client state: Zustand for global application state
- Component state: React hooks for local state