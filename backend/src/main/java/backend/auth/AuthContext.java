package backend.auth;

import backend.auth.exception.AuthenticationFailedException;
import lombok.AllArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class AuthContext {

    private UserRepository userRepository;

    public String getCurrentUsername() {
        var auth = SecurityContextHolder.getContext().getAuthentication();
        return auth.getName();
    }

    public User getCurrentUser() {
        String username = getCurrentUsername();
        return userRepository.findByUsername(username).orElseThrow(AuthenticationFailedException::new);
    }
}
