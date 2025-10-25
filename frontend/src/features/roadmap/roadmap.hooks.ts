import { useState, useCallback } from "react";
import { useQueryClient } from "@tanstack/react-query";
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
  
  const queryClient = useQueryClient();

  const sendMessage = useCallback(
    async (message: string) => {
      setState({
        isStreaming: true,
        error: null,
        currentMessage: "",
      });

      const session = Session(sessionId);
      let hasInvalidatedQueries = false;

      await session.chat(
        message,
        // onMessage callback - receives each chunk of the stream
        (data: string) => {
          setState((prev) => ({
            ...prev,
            currentMessage: prev.currentMessage + data,
          }));

          // Parse the data to detect tool calls that should invalidate queries
          if (!hasInvalidatedQueries) {
            try {
              // Parse SSE format
              const lines = data.split('\n').filter(line => line.trim());
              
              for (const line of lines) {
                if (line.startsWith('data:')) {
                  const dataContent = line.substring(5).trim();
                  const parsed = JSON.parse(dataContent);
                  
                  // Check for tool calls that affect materials/goals
                  if (parsed.tool_calls) {
                    const shouldInvalidate = parsed.tool_calls.some((call: any) => 
                      call.tool_name === 'createLearningMaterials' || 
                      call.tool_name === 'createRoadmapSkeleton'
                    );
                    
                    if (shouldInvalidate) {
                      // Invalidate relevant queries
                      queryClient.invalidateQueries({ 
                        queryKey: ["roadmap", "session", sessionId, "full"] 
                      });
                      queryClient.invalidateQueries({ 
                        queryKey: ["roadmap", "session", sessionId] 
                      });
                      hasInvalidatedQueries = true;
                    }
                  }
                  
                  // Also check for successful learning materials operations
                  if (parsed.operation === 'createLearningMaterials' && parsed.success) {
                    queryClient.invalidateQueries({ 
                      queryKey: ["roadmap", "session", sessionId, "full"] 
                    });
                    queryClient.invalidateQueries({ 
                      queryKey: ["roadmap", "session", sessionId] 
                    });
                    hasInvalidatedQueries = true;
                  }
                }
              }
            } catch (e) {
              // Ignore parsing errors, continue with normal flow
            }
          }
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
          
          // Final invalidation on completion if we detected relevant operations
          if (hasInvalidatedQueries) {
            // Also invalidate messages to refresh the chat history
            queryClient.invalidateQueries({ 
              queryKey: ["roadmap", "session", sessionId, "messages"] 
            });
          }
        }
      );
    },
    [sessionId, queryClient]
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
