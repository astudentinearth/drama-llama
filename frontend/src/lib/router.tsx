import LoginPage from "@/features/auth/login.page";
import RegisterPage from "@/features/auth/register.page";
import JobsPage from "@/features/jobs/jobs.page";
import Layout from "@/features/layout/layout";
import RoadmapPage from "@/features/roadmap/roadmap.page";
import { Route } from "react-router-dom";
import { Routes } from "react-router-dom";
import { BrowserRouter } from "react-router-dom";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<RoadmapPage />} />
          <Route path="/jobs" element={<JobsPage />} />
        </Route>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
}
