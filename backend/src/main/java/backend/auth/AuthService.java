package backend.auth;

import backend.auth.dto.RegisterRequestDTO;
import backend.auth.exception.EmailInUseException;
import backend.auth.exception.UsernameInUseException;
import backend.auth.user.UserRole;
import lombok.AllArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Set;

@Service
@AllArgsConstructor
public class AuthService {

    private UserRepository userRepository;
    private PasswordEncoder passwordEncoder;
    private AuthContext authContext;

    @Transactional
    public User register(RegisterRequestDTO dto) {
        if(userRepository.existsByUsername(dto.getUsername())) throw new UsernameInUseException();
        if(userRepository.existsByEmail(dto.getEmail())) throw new EmailInUseException();

        User user = User.builder()
                .username(dto.getUsername())
                .email(dto.getEmail())
                .passwordHash(passwordEncoder.encode(dto.getPassword()))
                .build();

        if(dto.isRecruiter()) user.setRoles(Set.of(UserRole.RECRUITER));
        else user.setRoles(Set.of(UserRole.MEMBER));

        return userRepository.save(user);

    }

    public User getAuthenticatedUser() {
        return authContext.getCurrentUser();
    }
}
