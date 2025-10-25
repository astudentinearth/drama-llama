package backend.profile.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UpdateProfileDTO {
    @Length(max = 120)
    private String fullName;

    @Length(max = 120)
    private String jobTitle;

    private List<String> skills;
}
