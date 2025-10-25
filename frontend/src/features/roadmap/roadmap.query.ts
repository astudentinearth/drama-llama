import { useQuery } from "@tanstack/react-query";
import { getSessions, Session } from "./roadmap.api";

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