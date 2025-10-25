import { useMutation } from "@tanstack/react-query";
import { login, register, logout, type RegisterDTO } from "./auth.api";
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
export interface RegisterMutationArgs {
  username: string;
  password: string;
  email: string;
  recruiter: boolean;
}

export function useRegisterMutation() {
  const nav = useNavigate();

  return useMutation({
    mutationFn: async (args: RegisterMutationArgs) => {
      // First register the user
      const user = await register(args);
      // Then automatically log them in
      await login(args.username, args.password);
      return user;
    },
    onSuccess(_data, _variables,  _onMutateResult, _context) {
      // Navigate to roadmaps after successful registration and login
      nav("/roadmaps");
    },
  });
}

export function useLogoutMutation() {
  const nav = useNavigate();

  return useMutation({
    mutationFn: async () => {
      await logout();
    },
    onSuccess(_data, _variables, _onMutateResult, context) {
      // Invalidate auth queries to clear user data
      context.client.invalidateQueries({ queryKey: ["auth"] });
      // Navigate to login page
      nav("/login");
    },
  });
}