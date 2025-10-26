// UserModeContext that provides if the current state is business or individual
import { createContext, useState, useContext} from 'react';
import type { ReactNode } from 'react';

type UserMode = 'business' | 'individual';

interface UserModeContextType {
    userMode: UserMode;
    setUserMode: (mode: UserMode) => void;
}

const UserModeContext = createContext<UserModeContextType | undefined>(undefined);

export const UserModeContextProvider = ({ children }: { children: ReactNode }) => {
    const [userMode, setUserMode] = useState<UserMode>('individual');

    return (
        <UserModeContext.Provider value={{ userMode, setUserMode }}>
            {children}
        </UserModeContext.Provider>
    );
}

export const useUserMode = () => {
    const context = useContext(UserModeContext);
    if (!context) {
        throw new Error('useUserMode must be used within a UserModeContextProvider');
    }
    return context;
}
