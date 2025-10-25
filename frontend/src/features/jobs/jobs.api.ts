import axios from "axios";
import { success } from "../../lib/api-util";
import type {
  JobListing,
  CreateJobListing,
  JobListingsResponse,
  JobApplication,
  CreateJobApplication,
  JobApplicationsResponse,
  ApplicationsCount,
} from "./jobs.types";

const JOBS_URL = "/api/jobs";

// Job listing functions
export async function getJobs() {
  const response = await axios.get(JOBS_URL);

  if (success(response)) {
    return response.data as JobListingsResponse;
  } else {
    throw new Error("Fetching jobs failed");
  }
}

export async function getJobById(id: string) {
  const response = await axios.get(`${JOBS_URL}/${id}`);

  if (success(response)) {
    return response.data as JobListing;
  } else {
    throw new Error("Fetching job by ID failed");
  }
}

export async function createJob(data: CreateJobListing) {
  const response = await axios.post(JOBS_URL, data);

  if (success(response)) {
    return response.data as JobListing;
  } else {
    throw new Error("Creating job failed");
  }
}

export async function updateJob(id: string, data: Partial<CreateJobListing>) {
  const response = await axios.patch(`${JOBS_URL}/${id}`, data);

  if (success(response)) {
    return response.data as JobListing;
  } else {
    throw new Error("Updating job failed");
  }
}

// Job application functions
export async function createJobApplication(
  jobId: string,
  data: CreateJobApplication
) {
  const response = await axios.post(`${JOBS_URL}/${jobId}/applications`, data);

  if (success(response)) {
    return response.data as JobApplication;
  } else {
    throw new Error("Creating job application failed");
  }
}

export async function getJobApplications(jobId: string) {
  const response = await axios.get(`${JOBS_URL}/${jobId}/applications`);

  if (success(response)) {
    return response.data as JobApplicationsResponse;
  } else {
    throw new Error("Fetching job applications failed");
  }
}

export async function getApplicationsCount(jobId: string) {
  const response = await axios.get(`${JOBS_URL}/${jobId}/count`);

  if (success(response)) {
    return response.data as ApplicationsCount;
  } else {
    throw new Error("Fetching applications count failed");
  }
}
