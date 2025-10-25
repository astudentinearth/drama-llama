package backend.company;

import backend.auth.AuthContext;
import backend.auth.exception.UnauthorizedException;
import backend.exception.NotFoundException;
import backend.jobs.entity.JobListing;
import backend.jobs.repository.JobListingRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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

    @Transactional
    public Company updateCompany(UUID id, String name, String description) {
        var currentUser = authContext.getCurrentUser();
        var company = companyRepository.findById(id).orElseThrow(() -> new NotFoundException(Company.class));
        if (!company.getUser().is(currentUser)) throw new UnauthorizedException();

        if (name != null) company.setName(name);
        if (description != null) company.setDescription(description);
        return companyRepository.save(company);
    }
}
