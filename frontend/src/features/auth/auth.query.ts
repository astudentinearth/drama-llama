import { useQuery } from "@tanstack/react-query";
import { getCurrentUser } from "./auth.api";

export function useAuth() {
  return useQuery({
    queryKey: ["auth"],
    queryFn: getCurrentUser,
  });
}
