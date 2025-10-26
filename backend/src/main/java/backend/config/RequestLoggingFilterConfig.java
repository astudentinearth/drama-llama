package backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.filter.CommonsRequestLoggingFilter;

@Configuration
public class RequestLoggingFilterConfig {
    @Bean
    public CommonsRequestLoggingFilter logFilter() {
        CommonsRequestLoggingFilter filter = new CommonsRequestLoggingFilter();
        filter.setIncludeQueryString(true); // Include query parameters
        filter.setIncludePayload(true);     // Include request body/payload
        filter.setMaxPayloadLength(10000); // Set max length of payload to log
        filter.setIncludeHeaders(false);    // Optionally include headers
        filter.setBeforeMessagePrefix("BEFORE REQUEST: ");
        filter.setAfterMessagePrefix("AFTER REQUEST: ");
        return filter;
    }
}