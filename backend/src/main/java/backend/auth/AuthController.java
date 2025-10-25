package backend.auth;

import backend.auth.dto.RegisterRequestDTO;
import backend.auth.dto.UserDTO;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@AllArgsConstructor
public class AuthController {

    private AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<UserDTO> register(@RequestBody @Valid RegisterRequestDTO dto) {
        var user = authService.register(dto);
        return ResponseEntity.ok(UserDTO.from(user));
    }

    @GetMapping("/me")
    public ResponseEntity<UserDTO> getCurrentUser() {
        var user = authService.getAuthenticatedUser();
        return ResponseEntity.ok(UserDTO.from(user));
    }
}
