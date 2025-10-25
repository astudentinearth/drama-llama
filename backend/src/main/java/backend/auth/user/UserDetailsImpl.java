package backend.auth.user;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.io.Serial;
import java.io.Serializable;
import java.util.Collection;
import java.util.Set;

@Getter
@Setter
@Builder
public class UserDetailsImpl implements UserDetails, Serializable {

    @Serial
    private static final long serialVersionUID = 2L;

    private String username;
    private String password;
    private Set<UserRole> roles;

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return roles;
    }

}
