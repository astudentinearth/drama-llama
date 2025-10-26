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
public class CreateQuizDTO {
    @JsonProperty("goal_id")
    private Long goal_id;

    @JsonProperty("time_limit_minutes")
    private Integer time_limit_minutes;

    @JsonProperty("passing_score_percentage")
    private Integer passing_score_percentage;

    @JsonProperty("max_attempts")
    private Integer max_attempts;
}

