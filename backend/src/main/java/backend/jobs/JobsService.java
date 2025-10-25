package backend.jobs;

import backend.auth.AuthContext;
import backend.auth.User;
import backend.auth.exception.UnauthorizedException;
import backend.exception.NotFoundException;
import backend.jobs.dto.CreateJobListingDTO;
import backend.jobs.entity.JobListing;
import backend.jobs.repository.JobListingRepository;
import lombok.AllArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.security.access.annotation.Secured;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class JobsService {

    private final JobListingRepository jobListingRepository;
    private final ModelMapper modelMapper;
    private final AuthContext authContext;

    public List<JobListing> getJobListings() {
        return jobListingRepository.findAllByIsActive(true);
    }

    public JobListing getJobListingById(UUID id) {
        var jobOptional = jobListingRepository.findById(id);
        if(jobOptional.isEmpty()) throw new NotFoundException(JobListing.class);
        return jobOptional.get();
    }

    @Secured("ROLE_RECRUITER")
    @Transactional
    public JobListing createJobListing(CreateJobListingDTO dto) {
        User user = authContext.getCurrentUser();
        JobListing listing = new JobListing();
        modelMapper.map(dto, listing);
        listing.setUser(user);
        return jobListingRepository.save(listing);
    }

    @Secured("ROLE_RECRUITER")
    @Transactional
    public JobListing updateJobListing(UUID id, CreateJobListingDTO dto) {
        User user = authContext.getCurrentUser();
        var jobOptional = jobListingRepository.findById(id);
        if(jobOptional.isEmpty()) throw new NotFoundException(JobListing.class);
        JobListing listing = jobOptional.get();
        if(!listing.getUser().is(user)) throw new UnauthorizedException();

        modelMapper.map(dto, listing);
        return jobListingRepository.save(listing);
    }
}
