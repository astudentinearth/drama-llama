package backend.auth;

import backend.auth.user.UserRole;
import backend.company.Company;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "users")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(length = 100)
    private String username;

    @Column
    private String passwordHash;

    @Column
    private String email;

    @Column
    @CreationTimestamp
    private Instant createdAt;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "user_roles", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "role_name")
    @Enumerated(EnumType.STRING)
    private Set<UserRole> roles;

    public boolean is(User user) {
        return this.id.equals(user.getId());
    }

    public boolean is(UUID userId) {
        return this.id.equals(userId);
    }
}
