package backend.auth.exception;

public class AuthenticationFailedException extends RuntimeException {
    public AuthenticationFailedException() {
        super("Authentication failed: Make sure you are logged in.");
    }
}
