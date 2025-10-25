import { useState, useCallback } from "react";
import { Session } from "./roadmap.api";

export interface ChatStreamState {
  isStreaming: boolean;
  error: string | null;
  currentMessage: string;
}

export function useChatStream(sessionId: number) {
  const [state, setState] = useState<ChatStreamState>({
    isStreaming: false,
    error: null,
    currentMessage: "",
  });

  const sendMessage = useCallback(
    async (message: string) => {
      setState({
        isStreaming: true,
        error: null,
        currentMessage: "",
      });

      const session = Session(sessionId);

      await session.chat(
        message,
        // onMessage callback - receives each chunk of the stream
        (data: string) => {
          setState((prev) => ({
            ...prev,
            currentMessage: prev.currentMessage + data,
          }));
        },
        // onError callback
        (error: Error) => {
          setState((prev) => ({
            ...prev,
            isStreaming: false,
            error: error.message,
          }));
        },
        // onComplete callback
        () => {
          setState((prev) => ({
            ...prev,
            isStreaming: false,
          }));
        }
      );
    },
    [sessionId]
  );

  const resetMessage = useCallback(() => {
    setState((prev) => ({
      ...prev,
      currentMessage: "",
      error: null,
    }));
  }, []);

  return {
    ...state,
    sendMessage,
    resetMessage,
  };
}
