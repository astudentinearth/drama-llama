package backend.auth.user;

import org.springframework.security.core.GrantedAuthority;

import java.io.Serializable;

public enum UserRole implements GrantedAuthority, Serializable {
    MEMBER,
    RECRUITER;

    @Override
    public String getAuthority() {
        return "ROLE_" + name();
    }
}
