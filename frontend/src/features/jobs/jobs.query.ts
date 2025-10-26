import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getJobs, getJobById, createJobApplication, getJobApplications } from "./jobs.api";

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

export function useJobApplicationsQuery(jobId: string) {
  return useQuery({
    queryKey: ["jobs", jobId, "applications"],
    queryFn: () => getJobApplications(jobId),
    enabled: !!jobId,
  });
}

export function useApplyToJobMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ jobId, message }: { jobId: string; message: string }) =>
      createJobApplication(jobId, { message }),
    onSuccess: (_, variables) => {
      // Invalidate job applications queries
      queryClient.invalidateQueries({ 
        queryKey: ["jobs", variables.jobId, "applications"] 
      });
    },
  });
}