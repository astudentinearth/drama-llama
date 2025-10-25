import NewListingDialog from "./new-listing-dialog";
import JobsCard from "./jobs-card";
import { useJobsQuery } from "./jobs.query";

export default function JobsPage() {
  const { data: jobsData, isLoading, error } = useJobsQuery();

  return (
    <div className="page-transition p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Jobs</h1>
        <NewListingDialog />
      </div>
      
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <p className="text-muted-foreground">Loading jobs...</p>
        </div>
      )}
      
      {error && (
        <div className="flex justify-center items-center py-12">
          <p className="text-red-500">Failed to load jobs. Please try again.</p>
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
          <p className="text-muted-foreground">No job listings found. Create the first one!</p>
        </div>
      )}
    </div>
  );
}
