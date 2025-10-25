import { useState, useMemo } from "react";
import NewListingDialog from "./new-listing-dialog";
import JobsCard from "./jobs-card";
import { useJobsQuery } from "./jobs.query";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

export default function JobsPage() {
  const { data: jobsData, isLoading, error } = useJobsQuery();
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // Extract all unique tags from jobs data (case insensitive)
  const allTags = useMemo(() => {
    if (!jobsData?.jobs) return [];
    
    const tagSet = new Set<string>();
    jobsData.jobs.forEach(job => {
      job.tags.forEach(tag => {
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
    
    return jobsData.jobs.filter(job => {
      const jobTagsLower = job.tags.map(tag => tag.toLowerCase());
      return selectedTags.some(selectedTag => 
        jobTagsLower.includes(selectedTag.toLowerCase())
      );
    });
  }, [jobsData, selectedTags]);

  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const clearAllTags = () => {
    setSelectedTags([]);
  };

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
                    variant={selectedTags.includes(tag) ? "default" : "outline"}
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
                  Showing {filteredJobs.length} job{filteredJobs.length !== 1 ? 's' : ''} 
                  {selectedTags.length > 0 && (
                    <span> matching any of: {selectedTags.map(tag => 
                      <span key={tag} className="font-medium capitalize">{tag}</span>
                    ).reduce((prev, curr, index) => 
                      index === 0 ? [curr] : [...prev, ', ', curr], [] as React.ReactNode[]
                    )}</span>
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
            <p className="text-muted-foreground mb-2">No jobs found with the selected tags.</p>
            <Button variant="outline" onClick={clearAllTags}>
              Clear filters
            </Button>
          </div>
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
