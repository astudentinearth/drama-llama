import { useMutation, useQueryClient } from "@tanstack/react-query";
import { profileApi } from "./profile.api";
import type { UpdateProfileDTO } from "./profile.types";

export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, data }: { userId: string; data: UpdateProfileDTO }) =>
      profileApi.updateUserProfile(userId, data),
    onSuccess: (_, { userId }) => {
      queryClient.invalidateQueries({ queryKey: ["profile", userId] });
    },
  });
};