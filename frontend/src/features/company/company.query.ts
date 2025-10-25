import { useQuery } from "@tanstack/react-query";
import { getCompanyById, getCompanyJobs, getMyCompany } from "./company.api";

export function useCompanyQuery(companyId: string) {
  return useQuery({
    queryKey: ["company", companyId],
    queryFn: () => getCompanyById(companyId),
    enabled: !!companyId,
  });
}

export function useCompanyJobsQuery(companyId: string) {
  return useQuery({
    queryKey: ["company", companyId, "jobs"],
    queryFn: () => getCompanyJobs(companyId),
    enabled: !!companyId,
  });
}

export function useMyCompanyQuery() {
  return useQuery({
    queryKey: ["company", "my"],
    queryFn: getMyCompany,
  });
}