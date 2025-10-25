package backend.upload.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UploadAvatarResponseDTO {
    private String uploadUrl;
    private String publicUrl;
    private String key;
}
