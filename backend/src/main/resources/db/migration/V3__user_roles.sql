
CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_name VARCHAR(100) NOT NULL,

    CONSTRAINT fk_roles_to_user
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);