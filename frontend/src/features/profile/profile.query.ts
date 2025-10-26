import { useQuery } from "@tanstack/react-query";
import { profileApi } from "./profile.api";

export const useUserProfile = (userId: string) => {
  return useQuery({
    queryKey: ["profile", userId],
    queryFn: () => profileApi.getUserProfile(userId),
    enabled: !!userId,
  });
};