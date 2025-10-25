package backend.roadmap;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.core.ParameterizedTypeReference;

import lombok.RequiredArgsConstructor;

import java.util.Map;

import backend.roadmap.dto.CreateSessionDTO;
import backend.roadmap.dto.ChatMessageDTO;

@RestController
@RequestMapping("/api/roadmap")
@RequiredArgsConstructor
public class RoadmapProxyController {

    private final WebClient webClient;

    @Value("${ai.service.url}")
    private String aiServiceUrl;

    @Value("${ai.service.api-key}")
    private String aiServiceApiKey;

    private String buildUrl(String pathTemplate, Map<String, ?> uriVars) {
        String base = aiServiceUrl != null ? aiServiceUrl : "";
        if (base.endsWith("/")) base = base.substring(0, base.length() - 1);
        if (!pathTemplate.startsWith("/")) pathTemplate = "/" + pathTemplate;
        String template = base + pathTemplate;
        return UriComponentsBuilder.fromUriString(template).buildAndExpand(uriVars).toUriString();
    }

    private Mono<ResponseEntity<byte[]>> proxyGet(String pathTemplate, Map<String, ?> uriVars) {
        String url = buildUrl(pathTemplate, uriVars);
        return webClient.get()
                .uri(url)
                .header("X-Api-Key", aiServiceApiKey == null ? "" : aiServiceApiKey)
                .exchangeToMono(this::toResponseEntity);
    }

    private Mono<ResponseEntity<byte[]>> proxyPost(String pathTemplate,
                                                   Map<String, ?> uriVars,
                                                   byte[] body,
                                                   HttpHeaders incomingHeaders) {
        String url = buildUrl(pathTemplate, uriVars);
        var spec = webClient.post().uri(url).header("X-Api-Key", aiServiceApiKey == null ? "" : aiServiceApiKey);
        MediaType contentType = incomingHeaders != null ? incomingHeaders.getContentType() : null;
        if (contentType != null) spec = spec.contentType(contentType);
        byte[] safeBody = body != null ? body : new byte[0];
        return spec.bodyValue(safeBody).exchangeToMono(this::toResponseEntity);
    }

    private Mono<ResponseEntity<byte[]>> toResponseEntity(ClientResponse resp) {
        Mono<byte[]> bodyMono = resp.bodyToMono(byte[].class).defaultIfEmpty(new byte[0]);
        return bodyMono.map(body -> {
            ResponseEntity.BodyBuilder builder = ResponseEntity.status(resp.statusCode());
            resp.headers().contentType().ifPresent(ct -> builder.header(HttpHeaders.CONTENT_TYPE, ct.toString()));
            return builder.body(body);
        });
    }

    @GetMapping("/sessions/{sessionId}")
    public Mono<ResponseEntity<byte[]>> getSession(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/sessions/{session_id}", Map.of("session_id", sessionId));
    }

    @GetMapping("/sessions/user/{userId}")
    public Mono<ResponseEntity<byte[]>> getUserSessions(@PathVariable("userId") String userId) {
        return proxyGet("/sessions/user/{user_id}", Map.of("user_id", userId));
    }

    @GetMapping("/sessions/{sessionId}/full")
    public Mono<ResponseEntity<byte[]>> getSessionFull(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/sessions/{session_id}/full", Map.of("session_id", sessionId));
    }

    @GetMapping("/sessions/{sessionId}/progress")
    public Mono<ResponseEntity<byte[]>> getSessionProgress(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/sessions/{session_id}/progress", Map.of("session_id", sessionId));
    }

    @GetMapping("/sessions/user/{userId}/stats")
    public Mono<ResponseEntity<byte[]>> getUserStats(@PathVariable("userId") String userId) {
        return proxyGet("/sessions/user/{user_id}/stats", Map.of("user_id", userId));
    }

    @GetMapping("/sessions/{sessionId}/messages")
    public Mono<ResponseEntity<byte[]>> getSessionMessages(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/sessions/{session_id}/messages", Map.of("session_id", sessionId));
    }

    @GetMapping("/sessions/{sessionId}/messages/recent")
    public Mono<ResponseEntity<byte[]>> getSessionMessagesRecent(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/sessions/{session_id}/messages/recent", Map.of("session_id", sessionId));
    }

    @GetMapping("/sessions/{sessionId}/messages/count")
    public Mono<ResponseEntity<byte[]>> getSessionMessagesCount(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/sessions/{session_id}/messages/count", Map.of("session_id", sessionId));
    }

    @GetMapping("/ai/sessions/{sessionId}/roadmap")
    public Mono<ResponseEntity<byte[]>> getSessionRoadmap(@PathVariable("sessionId") String sessionId) {
        return proxyGet("/ai/sessions/{session_id}/roadmap", Map.of("session_id", sessionId));
    }

    @PostMapping("/sessions/complete")
    public Mono<ResponseEntity<byte[]>> completeSession(@RequestParam("sessionId") Long sessionId,
                                                        @RequestHeader HttpHeaders headers,
                                                        @RequestBody(required = false) byte[] body) {
        return proxyPost("/sessions/{session_id}/complete", Map.of("session_id", String.valueOf(sessionId)), body, headers);
    }

    @PostMapping("/sessions/archive")
    public Mono<ResponseEntity<byte[]>> archiveSession(@RequestParam("sessionId") Long sessionId,
                                                       @RequestHeader HttpHeaders headers,
                                                       @RequestBody(required = false) byte[] body) {
        return proxyPost("/sessions/{session_id}/archive", Map.of("session_id", String.valueOf(sessionId)), body, headers);
    }

    @PostMapping("/sessions")
    public Mono<ResponseEntity<byte[]>> createSession(@RequestBody CreateSessionDTO dto) {
        if (dto.getStatus() == null || dto.getStatus().isBlank()) dto.setStatus("active");
        String url = buildUrl("/sessions/", Map.of());
        return webClient.post()
                .uri(url)
                .header("X-Api-Key", aiServiceApiKey == null ? "" : aiServiceApiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(dto)
                .exchangeToMono(this::toResponseEntity);
    }

    @PostMapping(value = "/ai/sessions/{sessionId}/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> postChatStream(@PathVariable("sessionId") String sessionId,
                                                        @RequestBody ChatMessageDTO body) {
        String url = buildUrl("/ai/sessions/{session_id}/chat", Map.of("session_id", sessionId));
        return webClient.post()
                .uri(url)
                .header("X-Api-Key", aiServiceApiKey == null ? "" : aiServiceApiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(body)
                .retrieve()
                .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {});
    }
}
