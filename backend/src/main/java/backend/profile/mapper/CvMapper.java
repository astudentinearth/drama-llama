package backend.profile.mapper;

import backend.profile.dto.CvDTO;
import backend.profile.entity.UserCv;
import backend.upload.S3Service;
import lombok.AllArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class CvMapper {
    private S3Service s3Service;
    private ModelMapper modelMapper;

    public CvDTO toDTO(UserCv cv) {
        CvDTO dto = new CvDTO();
        modelMapper.map(cv, dto);
        String url = s3Service.getPrivatePresignedUrl(cv.getObjectKey());
        dto.setUrl(url);
        return dto;
    }
}
