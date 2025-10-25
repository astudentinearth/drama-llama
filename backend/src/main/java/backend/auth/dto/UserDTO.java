package backend.auth.dto;

import backend.auth.User;
import backend.auth.user.UserRole;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.modelmapper.ModelMapper;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class UserDTO {
    private UUID id;
    private String username;
    private Instant createdAt;
    private List<UserRole> roles;

    public static UserDTO from(User user) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(user, UserDTO.class);
    }
}
