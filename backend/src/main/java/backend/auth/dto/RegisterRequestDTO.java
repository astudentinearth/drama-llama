package backend.auth.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class RegisterRequestDTO {
    @Length(min = 3 , max = 100)
    @NotBlank
    private String username;

    @Length(min = 8, max = 240)
    @NotBlank
    private String password;

    @Length(min = 3, max = 255)
    @NotBlank
    private String email;
}
