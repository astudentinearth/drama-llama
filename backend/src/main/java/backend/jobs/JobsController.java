package backend.jobs;

import backend.jobs.dto.CreateJobListingDTO;
import backend.jobs.dto.JobListingDTO;
import backend.jobs.dto.JobListingsResponse;
import lombok.AllArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/jobs")
@AllArgsConstructor
public class JobsController {

    private JobsService jobsService;
    private ModelMapper modelMapper;

    @GetMapping
    public ResponseEntity<JobListingsResponse> getJobs() {
        List<JobListing> jobs = jobsService.getJobListings();
        var dtos = jobs.stream().map((element) -> modelMapper.map(element, JobListingDTO.class));
        return ResponseEntity.ok(new JobListingsResponse(dtos.toList()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<JobListingDTO> getJobById(@PathVariable UUID id) {
        JobListing job = jobsService.getJobListingById(id);
        var dto = modelMapper.map(job, JobListingDTO.class);
        return ResponseEntity.ok(dto);
    }

    @PostMapping
    public ResponseEntity<JobListingDTO> createJob(@RequestBody CreateJobListingDTO dto) {
        JobListing job = jobsService.createJobListing(dto);
        var responseDto = modelMapper.map(job, JobListingDTO.class);
        return ResponseEntity.ok(responseDto);
    }

    @PatchMapping("/{id}")
    public ResponseEntity<JobListingDTO> updateJob(@PathVariable UUID id, @RequestBody CreateJobListingDTO dto) {
        JobListing job = jobsService.updateJobListing(id, dto);
        var responseDto = modelMapper.map(job, JobListingDTO.class);
        return ResponseEntity.ok(responseDto);
    }
}
