package backend.profile.dto;

import backend.profile.entity.UserProfile;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.modelmapper.ModelMapper;

import java.util.List;
import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserProfileDTO {
    private UUID userId;
    private String fullName;
    private String jobTitle;
    private List<String> skills;

    public static UserProfileDTO from(UserProfile userProfile) {
        var mapper = new ModelMapper();
        return mapper.map(userProfile, UserProfileDTO.class);
    }
}
