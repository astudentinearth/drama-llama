package backend.jobs;

import backend.jobs.dto.CreateJobApplicationDTO;
import backend.jobs.dto.JobApplicationDTO;
import backend.jobs.dto.JobApplicationsResponse;
import backend.jobs.dto.CreateJobListingDTO;
import backend.jobs.dto.JobListingDTO;
import backend.jobs.dto.JobListingsResponse;
import backend.jobs.dto.ApplicationsCountDTO;
import backend.jobs.entity.JobApplication;
import backend.jobs.entity.JobListing;
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

    private final JobsService jobsService;
    private final JobApplicationService jobApplicationService;
    private final ModelMapper modelMapper;

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

    @PostMapping("/{jobId}/applications")
    public ResponseEntity<JobApplicationDTO> upsertApplication(@PathVariable UUID jobId,
                                                               @RequestBody CreateJobApplicationDTO dto) {
        JobApplication application = jobApplicationService.upsertApplication(jobId, dto.getMessage());
        return ResponseEntity.ok(toJobApplicationDTO(application));
    }

    @GetMapping("/{jobId}/applications")
    public ResponseEntity<JobApplicationsResponse> listApplications(@PathVariable UUID jobId) {
        List<JobApplication> applications = jobApplicationService.listApplications(jobId);
        var dtos = applications.stream().map(this::toJobApplicationDTO).toList();
        return ResponseEntity.ok(new JobApplicationsResponse(dtos));
    }

    @GetMapping("/{jobId}/count")
    public ResponseEntity<ApplicationsCountDTO> countApplications(@PathVariable UUID jobId) {
        long count = jobApplicationService.countApplications(jobId);
        return ResponseEntity.ok(new ApplicationsCountDTO(count));
    }

    private JobApplicationDTO toJobApplicationDTO(JobApplication application) {
        return JobApplicationDTO.builder()
                .id(application.getId())
                .jobListingId(application.getJobListing().getId())
                .userId(application.getUser().getId())
                .message(application.getMessage())
                .build();
    }
}
