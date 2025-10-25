import { useMutation } from "@tanstack/react-query";
import { login } from "./auth.api";
import { useNavigate } from "react-router-dom";

export interface LoginMutationArgs {
  username: string;
  password: string;
}

export function useLoginMutation() {
  const nav = useNavigate();

  return useMutation({
    mutationFn: async (args: LoginMutationArgs) =>
      login(args.username, args.password),
    onSuccess(_data, _variables, _onMutateResult, context) {
      context.client.invalidateQueries({ queryKey: ["auth"] });
      nav("/");
    },
  });
}
