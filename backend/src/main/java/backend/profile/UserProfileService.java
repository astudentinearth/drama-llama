package backend.profile;

import backend.auth.AuthContext;
import backend.auth.exception.UnauthorizedException;
import backend.profile.dto.UpdateProfileDTO;
import backend.profile.dto.UserProfileDTO;
import backend.profile.entity.UserProfile;
import backend.profile.exception.ProfileNotFoundException;
import lombok.AllArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@AllArgsConstructor
public class UserProfileService {

    private UserProfileRepository userProfileRepository;
    private AuthContext authContext;

    public UserProfile getUserProfileById(UUID userId) {
        return userProfileRepository.findById(userId).orElseThrow(ProfileNotFoundException::new);
    }

    @Transactional
    public UserProfile createOrUpdateUserProfile(UUID userId, UpdateProfileDTO dto) {
        var currentUser = authContext.getCurrentUser();
        var mapper = new ModelMapper();
        if(!currentUser.is(userId)) throw new UnauthorizedException();
        var profile = userProfileRepository.findById(userId).orElse(new UserProfile());
        mapper.getConfiguration().setSkipNullEnabled(true);
        mapper.getConfiguration().setCollectionsMergeEnabled(false);
        mapper.map(dto, profile);
        profile.setUser(currentUser);
        return userProfileRepository.save(profile);
    }
}
