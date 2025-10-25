import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "@/features/auth/auth.query";

const ProtectedRoute = ({
  children,
}: {
  children: ReactNode | ReactNode[];
}) => {
  const user = useAuth().data;

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
