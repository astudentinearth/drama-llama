import axios from "axios";
import { success } from "../../lib/api-util";
import type { User } from "../user";

const LOGIN_URL = "/api/auth/login";
const REGISTER_URL = "/api/auth/register";
const LOGOUT_URL = "/api/auth/logout";
const CURRENT_USER_URL = "/api/auth/me";

export interface RegisterDTO {
  username: string;
  password: string;
  email: string;
}

export async function login(username: string, password: string) {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  const response = await axios.post(LOGIN_URL, params, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  if (success(response)) {
    return response.data as User;
  } else throw new Error("Login failed");
}

export async function register(dto: RegisterDTO) {
  const response = await axios.post(REGISTER_URL, dto);

  if (success(response)) {
    return response.data as User;
  } else throw new Error("Registration failed");
}

export async function logout() {
  await axios.get(LOGOUT_URL);
}

export async function getCurrentUser() {
  const response = await axios.get(CURRENT_USER_URL);

  if (success(response)) {
    return response.data as User;
  } else throw new Error("Fetching current user failed");
}
