package backend.upload;

import backend.upload.dto.PresignCvResponseDTO;
import backend.upload.dto.UploadAvatarResponseDTO;
import backend.upload.dto.UploadCvResponseDTO;
import org.springframework.web.multipart.MultipartFile;

public interface UploadService {
    UploadAvatarResponseDTO uploadAvatar(MultipartFile file);
    UploadCvResponseDTO uploadCv(MultipartFile file);
    PresignCvResponseDTO presignCv(MultipartFile file);
}
