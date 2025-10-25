package backend.upload.exception;

public class UploadFailedException extends RuntimeException {
    public UploadFailedException() {
        super("Failed to upload file.");
    }
}
