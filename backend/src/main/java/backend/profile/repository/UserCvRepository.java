package backend.profile.repository;

import backend.profile.entity.UserCv;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface UserCvRepository extends JpaRepository<UserCv, UUID> {
    List<UserCv> findByUserId(UUID userId);
}
