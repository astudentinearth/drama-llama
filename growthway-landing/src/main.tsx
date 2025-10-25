import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { UserModeContextProvider } from './contexts/user-mode-context.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UserModeContextProvider>
      <App />
    </UserModeContextProvider>
  </StrictMode>,
)
