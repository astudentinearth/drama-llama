package backend.company;

import backend.auth.AuthContext;
import backend.auth.Authorize;
import backend.exception.NotFoundException;
import backend.jobs.entity.JobListing;
import backend.jobs.repository.JobListingRepository;
import lombok.AllArgsConstructor;
import org.springframework.security.access.annotation.Secured;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class CompanyService {
    private final CompanyRepository companyRepository;
    private final JobListingRepository jobListingRepository;
    private final AuthContext authContext;

    public Company getCompanyById(UUID id) {
        return companyRepository.findById(id).orElseThrow(() -> new NotFoundException(Company.class));
    }

    public Company getMyCompany() {
        var currentUser = authContext.getCurrentUser();
        return companyRepository.findByUserId(currentUser.getId())
                .orElseThrow(() -> new NotFoundException(Company.class));
    }

    public List<JobListing> getCompanyJobs(UUID companyId) {
        return jobListingRepository.findAllByCompanyId(companyId);
    }
}
