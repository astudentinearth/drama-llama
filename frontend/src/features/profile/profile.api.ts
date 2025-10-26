import { success } from "@/lib/api-util";
import axios from "axios";
import type { UpdateProfileDTO, UserProfileResponseDTO } from "./profile.types";

export const profileApi = {
  getUserProfile: async (userId: string): Promise<UserProfileResponseDTO> => {
    const response = await axios.get(`/api/profile/${userId}`);
    if (success(response)) {
      return response.data;
    }
    throw new Error("Failed to fetch user profile");
  },

  updateUserProfile: async (
    userId: string,
    data: UpdateProfileDTO
  ): Promise<UserProfileResponseDTO> => {
    const response = await axios.post(`/api/profile/${userId}`, data);
    if (success(response)) {
      return response.data;
    }
    throw new Error("Failed to update user profile");
  },
};