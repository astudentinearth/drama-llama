package backend.auth.exception;

public class UsernameInUseException extends RuntimeException {
    public UsernameInUseException() {
        super("Username is already in use.");
    }
}
