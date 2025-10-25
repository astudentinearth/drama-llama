package backend.upload;

import io.minio.GetPresignedObjectUrlArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.http.Method;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.util.concurrent.TimeUnit;

@Service
public class S3Service {
    private final MinioClient minioClient;

    @Value("${minio.bucket.public}")
    private String publicBucketName;


    @Value("${minio.bucket.private}")
    private String privateBucketName;

    public S3Service(MinioClient minioClient) {
        this.minioClient = minioClient;
    }

    @SneakyThrows
    public void uploadPrivateObject(String key, InputStream inputStream, String contentType) {
        minioClient.putObject(PutObjectArgs.builder()
                .bucket(privateBucketName)
                .object(key)
                .stream(inputStream, -1, 10485760)
                .contentType(contentType)
                .build());
    }

    public String getPrivatePresignedUrl(String key) {
        return getPrivatePresignedUrl(key, 120);
    }

    @SneakyThrows
    public String getPrivatePresignedUrl(String key, int expiry) {
        GetPresignedObjectUrlArgs args = GetPresignedObjectUrlArgs.builder()
                .method(Method.GET)
                .bucket(privateBucketName)
                .object(key)
                .expiry(expiry, TimeUnit.SECONDS)
                .build();

        return minioClient.getPresignedObjectUrl(args);
    }
}
