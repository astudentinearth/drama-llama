package backend.jobs.entity;

import backend.auth.User;
import io.hypersistence.utils.hibernate.type.array.ListArrayType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.Type;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "job_listing")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class JobListing {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "user_id", referencedColumnName = "id", nullable = false)
    private User user;

    @Column(columnDefinition = "text", nullable = false)
    private String title;

    @Column(columnDefinition = "text")
    private String content;

    @Type(ListArrayType.class)
    @Column(columnDefinition = "text[]", name = "tags")
    private List<String> tags;

    @Column(columnDefinition = "boolean default true", name = "is_active")
    private boolean isActive;
}
