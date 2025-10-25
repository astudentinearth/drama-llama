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
public class CreateSessionDTO {
    @JsonProperty("user_id")
    private String user_id;
    @JsonProperty("session_name")
    private String session_name;
    @JsonProperty("description")
    private String description;
    @JsonProperty("status")
    private String status = "active";
}
