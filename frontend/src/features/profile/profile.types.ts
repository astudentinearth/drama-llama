export interface UserProfileDTO {
  userId: string;
  fullName: string;
  jobTitle: string;
  skills: string[];
}

export interface UserProfileResponseDTO {
  profile: UserProfileDTO;
}

export interface UpdateProfileDTO {
  fullName: string;
  jobTitle: string;
  skills: string[];
}