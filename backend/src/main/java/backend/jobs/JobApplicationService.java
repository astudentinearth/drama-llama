package backend.jobs;

import backend.auth.AuthContext;
import backend.auth.User;
import backend.auth.exception.UnauthorizedException;
import backend.auth.user.UserRole;
import backend.exception.NotFoundException;
import backend.jobs.entity.JobApplication;
import backend.jobs.entity.JobListing;
import backend.jobs.repository.JobApplicationRepository;
import backend.jobs.repository.JobListingRepository;
import lombok.AllArgsConstructor;
import org.springframework.security.access.annotation.Secured;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class JobApplicationService {

    private final JobApplicationRepository jobApplicationRepository;
    private final JobListingRepository jobListingRepository;
    private final AuthContext authContext;

    @Secured("ROLE_MEMBER")
    @Transactional
    public JobApplication upsertApplication(UUID jobId, String message) {
        User user = authContext.getCurrentUser();
        if (user.getRoles() != null && user.getRoles().contains(UserRole.RECRUITER)) {
            throw new UnauthorizedException();
        }
        JobListing listing = jobListingRepository.findById(jobId).orElseThrow(() -> new NotFoundException(JobListing.class));

        return jobApplicationRepository
                .findByJobListingIdAndUserId(jobId, user.getId())
                .map(existing -> {
                    existing.setMessage(message);
                    return jobApplicationRepository.save(existing);
                })
                .orElseGet(() -> {
                    JobApplication application = JobApplication.builder()
                            .jobListing(listing)
                            .user(user)
                            .message(message)
                            .build();
                    return jobApplicationRepository.save(application);
                });
    }

    @Secured("ROLE_RECRUITER")
    @Transactional(readOnly = true)
    public List<JobApplication> listApplications(UUID jobId) {
        User user = authContext.getCurrentUser();
        JobListing listing = jobListingRepository.findById(jobId).orElseThrow(() -> new NotFoundException(JobListing.class));
        if (!listing.getUser().is(user)) throw new UnauthorizedException();
        return jobApplicationRepository.findAllByJobListingId(jobId);
    }

    @Transactional(readOnly = true)
    public long countApplications(UUID jobId) {
        if (!jobListingRepository.existsById(jobId)) throw new NotFoundException(JobListing.class);
        return jobApplicationRepository.countByJobListingId(jobId);
    }
}
