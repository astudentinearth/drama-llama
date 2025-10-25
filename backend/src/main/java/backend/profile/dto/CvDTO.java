package backend.profile.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CvDTO {
    private UUID id;
    private UUID userId;
    private String url;
    private Instant createdAt;
}
