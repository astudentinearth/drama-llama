package backend.upload;

import backend.upload.dto.UploadCvResponseDTO;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/upload")
@AllArgsConstructor
public class UploadController {

    private UploadService uploadService;

    @PostMapping("/cv")
    public ResponseEntity<UploadCvResponseDTO> uploadCv(@RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(uploadService.uploadCv(file));
    }
}
