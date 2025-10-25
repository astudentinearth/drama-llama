package backend.company;

import backend.auth.Authorize;
import backend.company.dto.CompanyDTO;
import backend.jobs.dto.JobListingsResponse;
import lombok.AllArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@AllArgsConstructor
@RequestMapping("/api/company")
public class CompanyController {

    private final CompanyService companyService;
    private final ModelMapper modelMapper;

    @GetMapping("/{id}")
    public ResponseEntity<CompanyDTO> getCompanyById(@PathVariable UUID id) {
        var company = companyService.getCompanyById(id);
        var dto = modelMapper.map(company, CompanyDTO.class);
        return ResponseEntity.ok(dto);
    }

    @GetMapping("/{id}/jobs")
    public ResponseEntity<JobListingsResponse> getCompanyJobs(@PathVariable UUID id) {
        var jobs = companyService.getCompanyJobs(id);
        var dtos = jobs.stream().map((element) -> modelMapper.map(element, backend.jobs.dto.JobListingDTO.class));
        return ResponseEntity.ok(new JobListingsResponse(dtos.toList()));
    }

    @GetMapping("/my")
    @PreAuthorize("hasRole('RECRUITER')")
    public ResponseEntity<CompanyDTO> getMyCompany() {
        var company = companyService.getMyCompany();
        var dto = modelMapper.map(company, CompanyDTO.class);
        return ResponseEntity.ok(dto);
    }
}
