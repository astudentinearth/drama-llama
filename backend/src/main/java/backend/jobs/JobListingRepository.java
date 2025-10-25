package backend.jobs;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface JobListingRepository extends JpaRepository<JobListing, UUID> {
    List<JobListing> findAllByIsActive(boolean isActive);
}
