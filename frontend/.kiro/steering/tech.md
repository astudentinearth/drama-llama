# Tech Stack & Build System

## Core Technologies
- **React 19** with TypeScript
- **Vite** as build tool and dev server
- **TailwindCSS 4** for styling
- **React Router DOM 7** for client-side routing
- **TanStack Query 5** for server state management
- **Zustand** for client state management
- **Axios** for HTTP requests

## UI Components
- **Radix UI** primitives for accessible components
- **Lucide React** for icons
- **Class Variance Authority (CVA)** for component variants
- **clsx** and **tailwind-merge** for conditional styling

## Development Tools
- **ESLint** with TypeScript support
- **Bun** as package manager (bun.lock present)
- Path aliases configured (`@/` maps to `src/`)

## Common Commands
```bash
# Development
bun run dev          # Start development server
bun run build        # Build for production (TypeScript check + Vite build)
bun run lint         # Run ESLint
bun run preview      # Preview production build

# Package management
bun install          # Install dependencies
bun add <package>    # Add new dependency
```

## Build Configuration
- Vite with React plugin and TailwindCSS integration
- TypeScript with strict configuration
- Path aliases for clean imports
- ESM modules throughout