package backend.jobs.dto;


import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class CreateJobListingDTO {
    @Length(min = 4, max = 440)
    @NotBlank
    private String title;

    @Length(min = 4, max = 32768)
    @NotBlank
    private String content;

    private List<String> tags;

    private boolean active;
}
