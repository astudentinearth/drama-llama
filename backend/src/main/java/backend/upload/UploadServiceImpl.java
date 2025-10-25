package backend.upload;

import backend.auth.AuthContext;
import backend.upload.dto.PresignCvResponseDTO;
import backend.upload.dto.UploadAvatarResponseDTO;
import backend.upload.dto.UploadCvResponseDTO;
import backend.upload.exception.UploadFailedException;
import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

@Service
@Primary
@AllArgsConstructor
public class UploadServiceImpl implements UploadService {

    private final String AVATAR_UPLOAD_URL = "/files/avatar/presign";
    private final String CV_UPLOAD_URL = "/files/cv/presign";
    private final String CV_PRESIGN_URL = "/files/cv/{{key}}/presign";

    private S3Service s3Service;
    private AuthContext authContext;

    private String getCvKey(UUID userId) {
        return "users/" + userId.toString() + "/cv-" + UUID.randomUUID();
    }

    private String getCvPresignUrl(String key) {
        var encoded = URLEncoder.encode(key, StandardCharsets.UTF_8);
        return CV_PRESIGN_URL.replace("{{key}}", encoded);
    }

    @Override
    public UploadAvatarResponseDTO uploadAvatar(MultipartFile file) {
        return null;
    }

    @Override
    public UploadCvResponseDTO uploadCv(MultipartFile file) {
        var uid = authContext.getCurrentUser().getId();
        try {
            var key = getCvKey(uid);
            s3Service.uploadPrivateObject(key, file.getInputStream(), file.getContentType());
            return new UploadCvResponseDTO(s3Service.getPrivatePresignedUrl(key), key);
        } catch (IOException e) {
            throw new UploadFailedException();
        }
    }

    @Override
    public PresignCvResponseDTO presignCv(MultipartFile file) {
        return null;
    }
}
