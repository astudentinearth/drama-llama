
CREATE TABLE user_cv (
    id uuid primary key,
    user_id uuid not null,
    object_key varchar unique not null,
    created_at timestamp with time zone not null default current_timestamp,
    constraint fk_cv_to_user foreign key (user_id) references users(id) on delete cascade
);