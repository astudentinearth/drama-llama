package backend.upload.service;

import backend.profile.dto.CvDTO;
import backend.upload.dto.UploadAvatarResponseDTO;
import backend.upload.dto.UploadCvResponseDTO;
import org.springframework.web.multipart.MultipartFile;

import java.util.UUID;

public interface UploadService {
    UploadAvatarResponseDTO uploadAvatar(MultipartFile file);
    UploadCvResponseDTO uploadCv(MultipartFile file);
    String presignCv(UUID cvId);
}
