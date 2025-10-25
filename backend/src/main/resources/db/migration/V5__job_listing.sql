CREATE TABLE job_listing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    tags TEXT[],
    is_active boolean default true
);

CREATE INDEX idx_job_listing_user_id ON job_listing(user_id);
CREATE INDEX idx_job_listing_tags ON job_listing USING GIN(tags);