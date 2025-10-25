package backend.profile.entity;

import backend.auth.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "user_cv")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class UserCv {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "user_id", referencedColumnName = "id", nullable = false)
    private User user;

    @Column(name = "object_key", nullable = false)
    private String objectKey;

    @CreationTimestamp
    @Column(nullable = false, name = "created_at")
    private Instant createdAt;
}
