package backend.company;

import backend.auth.Authorize;
import lombok.AllArgsConstructor;
import org.springframework.security.access.annotation.Secured;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class CompanyService {

    @Secured("ROLE_RECRUITER")
    public String createCompany() {
        return "Company created";
    }
}
