import { useQuery } from "@tanstack/react-query";
import { getJobs } from "./jobs.api";

export function useJobsQuery() {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: getJobs,
  });
}