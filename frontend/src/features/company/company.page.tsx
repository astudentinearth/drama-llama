import { useParams } from "react-router-dom";
import { useCompanyQuery, useCompanyJobsQuery } from "./company.query";
import JobsCard from "../jobs/jobs-card";

export default function CompanyPage() {
  const { companyId } = useParams<{ companyId: string }>();

  const {
    data: company,
    isLoading: isCompanyLoading,
    error: companyError,
  } = useCompanyQuery(companyId!);

  const {
    data: jobsData,
    isLoading: isJobsLoading,
    error: jobsError,
  } = useCompanyJobsQuery(companyId!);

  if (!companyId) {
    return (
      <div className="page-transition p-6">
        <div className="flex justify-center items-center py-12">
          <p className="text-red-500">Invalid company ID.</p>
        </div>
      </div>
    );
  }

  if (isCompanyLoading) {
    return (
      <div className="page-transition p-6">
        <div className="flex justify-center items-center py-12">
          <p className="text-muted-foreground">Loading company...</p>
        </div>
      </div>
    );
  }

  if (companyError) {
    return (
      <div className="page-transition p-6">
        <div className="flex justify-center items-center py-12">
          <p className="text-red-500">
            Failed to load company. Please try again.
          </p>
        </div>
      </div>
    );
  }

  if (!company) {
    return (
      <div className="page-transition p-6">
        <div className="flex justify-center items-center py-12">
          <p className="text-muted-foreground">Company not found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-transition p-6">
      {/* Company Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{company.name}</h1>
        <hr className="mb-4"/>
        <p className="text-muted-foreground text-lg">{company.description || "No description found."}</p>
      </div>

      {/* Jobs Section */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold mb-4">Open Positions</h2>

        {isJobsLoading && (
          <div className="flex justify-center items-center py-12">
            <p className="text-muted-foreground">Loading jobs...</p>
          </div>
        )}

        {jobsError && (
          <div className="flex justify-center items-center py-12">
            <p className="text-red-500">
              Failed to load jobs. Please try again.
            </p>
          </div>
        )}

        {jobsData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobsData.jobs.map((job) => (
              <JobsCard key={job.id} job={job} />
            ))}
          </div>
        )}

        {jobsData && jobsData.jobs.length === 0 && (
          <div className="flex justify-center items-center py-12">
            <p className="text-muted-foreground">
              No open positions at this company.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
