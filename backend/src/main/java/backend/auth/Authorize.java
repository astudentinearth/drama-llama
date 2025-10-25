package backend.auth;

public class Authorize {
    public static final String MEMBER = "hasAuthority('ROLE_MEMBER')";
    public static final String RECRUITER = "hasAuthority('ROLE_RECRUITER')";
}
