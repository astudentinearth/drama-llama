package backend.profile;

import backend.profile.dto.GetCVsResponseDTO;
import backend.profile.dto.UpdateProfileDTO;
import backend.profile.dto.UserProfileDTO;
import backend.profile.dto.UserProfileResponseDTO;
import backend.profile.mapper.CvMapper;
import lombok.AllArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/profile")
@AllArgsConstructor
public class UserProfileController {

    private UserProfileService userProfileService;
    private CvMapper cvMapper;

    @GetMapping("/{userId}")
    public ResponseEntity<UserProfileResponseDTO> getUserProfile(@PathVariable UUID userId) {
        var profile = userProfileService.getUserProfileById(userId);
        return ResponseEntity.ok(new UserProfileResponseDTO(UserProfileDTO.from(profile)));
    }

    @PostMapping("/{userId}")
    public ResponseEntity<UserProfileResponseDTO> createOrUpdateUserProfile(@PathVariable UUID userId, @RequestBody UpdateProfileDTO dto) {
        var profile = userProfileService.createOrUpdateUserProfile(userId, dto);
        return ResponseEntity.ok(new UserProfileResponseDTO(UserProfileDTO.from(profile)));
    }

    @GetMapping("/{userId}/cv")
    public ResponseEntity<GetCVsResponseDTO> getUserCvs(@PathVariable UUID userId) {
        var cvs = userProfileService.getUserCvs(userId);
        var dtos = cvs.stream().map(cvMapper::toDTO).toList();
        return ResponseEntity.ok(new GetCVsResponseDTO(dtos));
    }
}
