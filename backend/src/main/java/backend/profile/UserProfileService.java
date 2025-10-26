package backend.profile;

import backend.auth.AuthContext;
import backend.auth.exception.UnauthorizedException;
import backend.profile.dto.UpdateProfileDTO;
import backend.profile.entity.UserCv;
import backend.profile.entity.UserProfile;
import backend.profile.exception.ProfileNotFoundException;
import backend.profile.repository.UserCvRepository;
import backend.profile.repository.UserProfileRepository;
import backend.roadmap.dto.SummarizeCvDTO;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserProfileService {

    private final UserProfileRepository userProfileRepository;
    private final UserCvRepository cvRepository;
    private final AuthContext authContext;
    private final WebClient webClient;

    @Value("${ai.service.url}")
    private String aiServiceUrl;

    @Value("${ai.service.api-key}")
    private String aiServiceApiKey;

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

    public List<UserCv> getUserCvs(UUID userId) {
        var currentUser = authContext.getCurrentUser();
        if(!currentUser.is(userId)) throw new UnauthorizedException();
        return cvRepository.findByUserId(userId);
    }

    public Mono<ResponseEntity<byte[]>> summarizeCv(UUID userId, String sessionId, SummarizeCvDTO dto) {
        var currentUser = authContext.getCurrentUser();
        if (!currentUser.is(userId)) throw new UnauthorizedException();
        String base = aiServiceUrl != null ? aiServiceUrl : "";
        if (base.endsWith("/")) base = base.substring(0, base.length() - 1);
        String url = UriComponentsBuilder.fromUriString(base + "/ai/sessions/{session_id}/summarize-cv")
                .buildAndExpand(Map.of("session_id", sessionId))
                .toUriString();
        return webClient.post()
                .uri(url)
                .header("X-Api-Key", aiServiceApiKey == null ? "" : aiServiceApiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(dto)
                .exchangeToMono(this::toResponseEntity);
    }

    private Mono<ResponseEntity<byte[]>> toResponseEntity(ClientResponse resp) {
        Mono<byte[]> bodyMono = resp.bodyToMono(byte[].class).defaultIfEmpty(new byte[0]);
        return bodyMono.map(body -> {
            ResponseEntity.BodyBuilder builder = ResponseEntity.status(resp.statusCode());
            resp.headers().contentType().ifPresent(ct -> builder.header(HttpHeaders.CONTENT_TYPE, ct.toString()));
            return builder.body(body);
        });
    }
}
