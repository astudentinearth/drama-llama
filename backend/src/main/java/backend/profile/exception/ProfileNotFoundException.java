package backend.profile.exception;

public class ProfileNotFoundException extends RuntimeException{
    public ProfileNotFoundException() {
        super("User profile not found");
    }
}
