import { useQuery } from "@tanstack/react-query";
import { getJobs, getJobById } from "./jobs.api";

export function useJobsQuery() {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: getJobs,
  });
}

export function useJobQuery(jobId: string) {
  return useQuery({
    queryKey: ["jobs", jobId],
    queryFn: () => getJobById(jobId),
    enabled: !!jobId,
  });
}