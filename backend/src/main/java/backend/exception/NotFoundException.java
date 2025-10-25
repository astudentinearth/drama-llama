package backend.exception;

public class NotFoundException extends RuntimeException {
    public <T> NotFoundException(Class<T> type) {
        super(type.getName() + " not found.");
    }
}
