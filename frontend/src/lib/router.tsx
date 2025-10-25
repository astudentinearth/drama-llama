import { getCurrentUser } from "@/features/auth/auth.api";
import LoginPage from "@/features/auth/login.page";
import RegisterPage from "@/features/auth/register.page";
import JobsPage from "@/features/jobs/jobs.page";
import Layout from "@/features/layout/layout";
import ProfilePage from "@/features/profile/profile.page";
import RoadmapPage from "@/features/roadmap/roadmap.page";
import { Navigate } from "react-router-dom";
import { Route } from "react-router-dom";
import { Routes } from "react-router-dom";
import { BrowserRouter } from "react-router-dom";

const protect = async () => {
  try {
    const user = await getCurrentUser();
  } catch {
    window.location.href = "/login";
  }
};

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to={"/roadmaps"} />} />
          <Route path="/roadmaps" element={<RoadmapPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Route>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
}
