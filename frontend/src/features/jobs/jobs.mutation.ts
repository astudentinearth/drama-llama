import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createJob } from "./jobs.api";

export interface CreateJobMutationArgs {
  title: string;
  content: string;
  tags: string[];
  active: boolean;
}

export function useCreateJobMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (args: CreateJobMutationArgs) => {
      return createJob(args);
    },
    onSuccess() {
      // Invalidate jobs queries to refresh the list
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
    },
  });
}