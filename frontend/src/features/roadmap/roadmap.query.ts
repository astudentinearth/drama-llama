import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getSessions, Session, createSession } from "./roadmap.api";

export function useSessionsQuery() {
  return useQuery({
    queryKey: ["roadmap", "sessions"],
    queryFn: getSessions,
  });
}

export function useSessionQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "session", sessionId],
    queryFn: () => Session(sessionId).get(),
    enabled: !!sessionId,
  });
}

export function useFullSessionQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "session", sessionId, "full"],
    queryFn: () => Session(sessionId).getFull(),
    enabled: !!sessionId,
  });
}

export function useSessionMessagesQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "session", sessionId, "messages"],
    queryFn: () => Session(sessionId).getMessages(),
    enabled: !!sessionId,
  });
}

export function useCreateSessionMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionName, description }: { sessionName: string; description: string }) =>
      createSession(sessionName, description),
    onSuccess: () => {
      // Invalidate and refetch sessions list
      queryClient.invalidateQueries({ queryKey: ["roadmap", "sessions"] });
    },
  });
}