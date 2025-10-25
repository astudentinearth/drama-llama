import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "@/features/auth/auth.query";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({
  children,
}: {
  children: ReactNode | ReactNode[];
}) => {
  return children;
};

export default ProtectedRoute;
