package backend.jobs.dto;


import backend.jobs.JobListing;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class JobListingsResponse {
    private List<JobListingDTO> jobs;
}
