package backend.profile.entity;

import backend.auth.User;
import jakarta.persistence.*;
import lombok.*;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "user_profile")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserProfile {

    @Id
    private UUID id;

    @MapsId
    @OneToOne
    @JoinColumn(name = "user_id", referencedColumnName = "id")
    private User user;

    @Column
    private String fullName;

    @Column
    private String jobTitle;

    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(
            name = "user_profile_skills",
            joinColumns = @JoinColumn(name = "user_id")
    )
    @Column(name = "skill_name")
    private List<String> skills;

    @Column(columnDefinition = "text")
    private String cvSummary;
}
