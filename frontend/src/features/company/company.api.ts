import axios from "axios";
import { success } from "../../lib/api-util";
import type { Company } from "./company.types";
import type { JobListingsResponse } from "../jobs/jobs.types";

const COMPANY_URL = "/api/company";

export async function getCompanyById(id: string) {
  const response = await axios.get(`${COMPANY_URL}/${id}`);

  if (success(response)) {
    return response.data as Company;
  } else {
    throw new Error("Fetching company by ID failed");
  }
}

export async function getMyCompany() {
  const response = await axios.get(`${COMPANY_URL}/my`);

  if (success(response)) {
    return response.data as Company;
  } else {
    throw new Error("Fetching my company failed");
  }
}

export async function getCompanyJobs(companyId: string) {
  const response = await axios.get(`${COMPANY_URL}/${companyId}/jobs`);

  if (success(response)) {
    return response.data as JobListingsResponse;
  } else {
    throw new Error("Fetching company jobs failed");
  }
}