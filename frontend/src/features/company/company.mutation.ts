import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateCompany } from "./company.api";
import type { UpdateCompanyDTO } from "./company.types";

export function useUpdateCompanyMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ companyId, data }: { companyId: string; data: UpdateCompanyDTO }) =>
      updateCompany(companyId, data),
    onSuccess: (updatedCompany) => {
      // Invalidate and refetch company queries
      queryClient.invalidateQueries({ queryKey: ["company", updatedCompany.id] });
      queryClient.invalidateQueries({ queryKey: ["company", "my"] });
    },
  });
}