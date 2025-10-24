CREATE TABLE user_profile (
    user_id UUID NOT NULL,
    full_name VARCHAR(255),
    job_title VARCHAR(255),
    PRIMARY KEY (user_id),
    CONSTRAINT fk_userprofile_to_user
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);

CREATE TABLE user_profile_skills (
    user_id UUID NOT NULL,
    skill_name VARCHAR(255),

    CONSTRAINT fk_skills_to_userprofile
        FOREIGN KEY (user_id)
        REFERENCES user_profile (user_id)
        ON DELETE CASCADE
);