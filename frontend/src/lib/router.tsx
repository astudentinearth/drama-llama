import LoginPage from "@/features/auth/login.page";
import RegisterPage from "@/features/auth/register.page";
import CompanyPage from "@/features/company/company.page";
import JobsPage from "@/features/jobs/jobs.page";
import JobDetailPage from "@/features/jobs/job-detail.page.tsx";
import Layout from "@/features/layout/layout";
import RoadmapPage from "@/features/roadmap/roadmap.page";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to={"/roadmaps"} />} />
          <Route path="/roadmaps" element={<RoadmapPage />} />
          <Route path="/roadmaps/:sessionId" element={<RoadmapPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/jobs/:jobId" element={<JobDetailPage />} />
          <Route path="/company/:companyId" element={<CompanyPage />} />
        </Route>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
}
