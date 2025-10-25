package backend.jobs.dto;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class JobListingDTO {
    private UUID id;
    private String title;
    private String content;
    private List<String> tags;
    private UUID userId;
    private boolean active;
}
