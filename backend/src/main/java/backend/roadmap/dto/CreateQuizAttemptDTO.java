package backend.roadmap.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class CreateQuizAttemptDTO {
    @JsonProperty("quiz_id")
    private Long quiz_id;

    @JsonProperty("user_id")
    private String user_id;
}

