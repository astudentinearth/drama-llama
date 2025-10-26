# Drama Llama Frontend

This is the frontend for the Drama Llama project, a web application built with React, Vite, and TypeScript.

## Installation

To install the project's dependencies, run the following command:

```bash
bun install
```

## Running the Project

To run the project in development mode, run the following command:

```bash
bun run dev
```

This will start the development server at `http://localhost:5173`.

## Building the Project

To build the project for production, run the following command:

```bash
bun run build
```

This will create a `dist` directory with the production-ready files.

## Linting

To lint the project's code, run the following command:

```bash
bun run lint
```

## Project Structure

The project's directory structure is as follows:

```
├───.gitignore
├───bun.lock
├───components.json
├───eslint.config.js
├───index.html
├───package.json
├───README.md
├───tsconfig.app.json
├───tsconfig.json
├───tsconfig.node.json
├───vite.config.ts
├───.kiro/
├───.vscode/
├───dist/
├───node_modules/
├───public/
└───src/
    ├───App.tsx
    ├───index.css
    ├───main.tsx
    ├───assets/
    ├───components/
    ├───features/
    └───lib/
```

## Dependencies

- **@radix-ui/react-dialog**: For creating accessible dialogs.
- **@radix-ui/react-label**: For creating accessible labels.
- **@radix-ui/react-progress**: For creating accessible progress bars.
- **@radix-ui/react-slot**: For creating accessible slots.
- **@tanstack/react-query**: For data fetching and caching.
- **axios**: For making HTTP requests.
- **class-variance-authority**: For creating class variants.
- **clsx**: For constructing `className` strings conditionally.
- **lucide-react**: For using Lucide icons.
- **react**: For building user interfaces.
- **react-dom**: For rendering React components.
- **react-markdown**: For rendering Markdown.
- **react-router-dom**: For routing.
- **remark-gfm**: For GitHub Flavored Markdown support.
- **tailwind-merge**: For merging Tailwind CSS classes.
- **zustand**: For state management.

## Dev Dependencies

- **@eslint/js**: For ESLint.
- **@tailwindcss/vite**: For using Tailwind CSS with Vite.
- **@types/node**: For Node.js types.
- **@types/react**: For React types.
- **@types/react-dom**: For React DOM types.
- **@vitejs/plugin-react**: For using React with Vite.
- **eslint**: For linting.
- **eslint-plugin-react-hooks**: For ESLint React Hooks plugin.
- **eslint-plugin-react-refresh**: For ESLint React Refresh plugin.
- **globals**: For ESLint globals.
- **tailwindcss**: For Tailwind CSS.
- **tw-animate-css**: For Tailwind CSS animations.
- **typescript**: For TypeScript.
- **typescript-eslint**: For TypeScript ESLint.
- **vite**: For building and running the project.