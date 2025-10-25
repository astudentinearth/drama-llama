package backend.jobs.repository;

import backend.jobs.entity.JobListing;
import backend.jobs.entity.JobWishlist;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface JobWishlistRepository extends JpaRepository<JobWishlist, UUID> {
    @EntityGraph(attributePaths = {"jobListing"})
    List<JobListing> findAllByUserId(UUID userId);
}
