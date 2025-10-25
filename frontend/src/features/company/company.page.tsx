import { useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import { useCompanyQuery, useCompanyJobsQuery, useMyCompanyQuery } from "./company.query";
import { useAuth } from "../auth/auth.query";
import JobsCard from "../jobs/jobs-card";
import EditCompanyDialog from "./edit-company-dialog";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

export default function CompanyPage() {
  const { companyId } = useParams<{ companyId: string }>();
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const { data: currentUser } = useAuth();
  const { data: myCompany } = useMyCompanyQuery();

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

  // Check if current user is a recruiter and viewing their own company
  const isRecruiter = currentUser?.roles?.includes("RECRUITER");
  const isOwnCompany = myCompany?.id === companyId;
  const canEditCompany = isRecruiter && isOwnCompany;

  // Extract all unique tags from jobs data (case insensitive)
  const allTags = useMemo(() => {
    if (!jobsData?.jobs) return [];

    const tagSet = new Set<string>();
    jobsData.jobs.forEach((job) => {
      job.tags.forEach((tag) => {
        tagSet.add(tag.toLowerCase());
      });
    });

    return Array.from(tagSet).sort();
  }, [jobsData]);

  // Filter jobs based on selected tags (OR logic - at least one tag must match)
  const filteredJobs = useMemo(() => {
    if (!jobsData?.jobs || selectedTags.length === 0) {
      return jobsData?.jobs || [];
    }

    return jobsData.jobs.filter((job) => {
      const jobTagsLower = job.tags.map((tag) => tag.toLowerCase());
      return selectedTags.some((selectedTag) =>
        jobTagsLower.includes(selectedTag.toLowerCase())
      );
    });
  }, [jobsData, selectedTags]);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const clearAllTags = () => {
    setSelectedTags([]);
  };

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
        <div className="flex justify-between items-start mb-2">
          <h1 className="text-3xl font-bold">{company.name}</h1>
          {canEditCompany && <EditCompanyDialog company={company} />}
        </div>
        <hr className="mb-4" />
        <p className="text-muted-foreground text-lg">
          {company.description || "No description found."}
        </p>
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
          <>
            {/* Tag Filters */}
            {allTags.length > 0 && (
              <div className="mb-6">
                <div className="flex items-center gap-2 mb-3">
                  <h3 className="text-lg font-semibold">Filter by tags:</h3>
                  {selectedTags.length > 0 && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={clearAllTags}
                      className="text-xs"
                    >
                      <X className="w-3 h-3 mr-1" />
                      Clear all
                    </Button>
                  )}
                </div>

                <div className="flex flex-wrap gap-2">
                  {allTags.map((tag) => (
                    <Button
                      key={tag}
                      variant={
                        selectedTags.includes(tag) ? "default" : "outline"
                      }
                      size="sm"
                      onClick={() => toggleTag(tag)}
                      className="text-xs capitalize"
                    >
                      {tag}
                    </Button>
                  ))}
                </div>

                {selectedTags.length > 0 && (
                  <div className="mt-3 text-sm text-muted-foreground">
                    Showing {filteredJobs.length} job
                    {filteredJobs.length !== 1 ? "s" : ""}
                    {selectedTags.length > 0 && (
                      <span>
                        {" "}
                        matching any of:{" "}
                        {selectedTags
                          .map((tag) => (
                            <span key={tag} className="font-medium capitalize">
                              {tag}
                            </span>
                          ))
                          .reduce(
                            (prev, curr, index) =>
                              index === 0 ? [curr] : [...prev, ", ", curr],
                            [] as React.ReactNode[]
                          )}
                      </span>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Jobs Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredJobs.map((job) => (
                <JobsCard key={job.id} job={job} />
              ))}
            </div>
          </>
        )}

        {jobsData && filteredJobs.length === 0 && selectedTags.length > 0 && (
          <div className="flex justify-center items-center py-12">
            <div className="text-center">
              <p className="text-muted-foreground mb-2">
                No jobs found with the selected tags.
              </p>
              <Button variant="outline" onClick={clearAllTags}>
                Clear filters
              </Button>
            </div>
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
