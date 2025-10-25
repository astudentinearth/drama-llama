package backend.jobs.repository;

import backend.jobs.entity.JobApplication;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface JobApplicationRepository extends JpaRepository<JobApplication, UUID> {
    @EntityGraph(attributePaths = {"jobListing"})
    List<JobApplication> findAllByUserId(UUID userId);

    @EntityGraph(attributePaths = {"jobListing"})
    List<JobApplication> findAllByJobListingId(UUID jobListingId);

    Optional<JobApplication> findByJobListingIdAndUserId(UUID jobListingId, UUID userId);

    long countByJobListingId(UUID jobListingId);
}
