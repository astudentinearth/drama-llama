export interface JobListing {
  id: string;
  title: string;
  content: string;
  tags: string[];
  userId: string;
  active: boolean;
}

export interface CreateJobListing {
  title: string;
  content: string;
  tags: string[];
  active: boolean;
}

export interface JobListingsResponse {
  jobs: JobListing[];
}

export interface JobApplication {
  id: string;
  jobListingId: string;
  userId: string;
  message: string;
}

export interface CreateJobApplication {
  message: string;
}

export interface JobApplicationsResponse {
  applications: JobApplication[];
}

export interface ApplicationsCount {
  count: number;
}