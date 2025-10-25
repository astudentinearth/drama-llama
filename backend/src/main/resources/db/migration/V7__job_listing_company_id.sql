-- Migration to add company_id column to job_listing table
ALTER TABLE job_listing
ADD COLUMN company_id UUID REFERENCES company(id) ON DELETE
    CASCADE;

-- Create an index on the new company_id column for performance
CREATE INDEX idx_job_listing_company_id ON job_listing(company_id);