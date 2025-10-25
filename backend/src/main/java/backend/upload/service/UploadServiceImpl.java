package backend.upload.service;

import backend.auth.AuthContext;
import backend.exception.NotFoundException;
import backend.profile.entity.UserCv;
import backend.profile.mapper.CvMapper;
import backend.profile.repository.UserCvRepository;
import backend.upload.S3Service;
import backend.profile.dto.CvDTO;
import backend.upload.dto.UploadAvatarResponseDTO;
import backend.upload.dto.UploadCvResponseDTO;
import backend.upload.exception.UploadFailedException;
import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.UUID;

@Service
@Primary
@AllArgsConstructor
public class UploadServiceImpl implements UploadService {

    private S3Service s3Service;
    private AuthContext authContext;
    private UserCvRepository cvRepository;

    private String getCvKey(UUID userId) {
        return "users/" + userId.toString() + "/cv-" + UUID.randomUUID();
    }

    @Override
    public UploadAvatarResponseDTO uploadAvatar(MultipartFile file) {
        return null;
    }

    @Override
    @Transactional
    public UploadCvResponseDTO uploadCv(MultipartFile file) {
        var user = authContext.getCurrentUser();
        var uid = user.getId();
        try {
            var key = getCvKey(uid);
            s3Service.uploadPrivateObject(key, file.getInputStream(), file.getContentType());
            UserCv cv = UserCv.builder().objectKey(key).user(user).build();
            cv = cvRepository.save(cv);
            return new UploadCvResponseDTO(cv.getId(), s3Service.getPrivatePresignedUrl(key), key);
        } catch (IOException e) {
            throw new UploadFailedException();
        }
    }

    @Override
    public String presignCv(UUID cvId) {
        var cv = cvRepository.findById(cvId).orElseThrow(() -> new NotFoundException(UserCv.class));
        return s3Service.getPrivatePresignedUrl(cv.getObjectKey());
    }
}
