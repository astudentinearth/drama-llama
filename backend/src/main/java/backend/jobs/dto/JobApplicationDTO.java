package backend.jobs.dto;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class JobApplicationDTO {
    private UUID id;
    private UUID jobListingId;
    private UUID userId;
    private String message;
}
