import { useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useJobQuery, useJobApplicationsQuery } from "./jobs.query";
import { useCreateSessionMutation } from "../roadmap/roadmap.query";
import { useAuth } from "../auth/auth.query";
import { Session } from "../roadmap/roadmap.api";
import ApplyJobDialog from "./apply-job-dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, GraduationCap, Loader2, Building, Clock } from "lucide-react";

export default function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [isCreatingSession, setIsCreatingSession] = useState(false);
  const [hasAppliedLocally, setHasAppliedLocally] = useState(false);
  
  const { data: job, isLoading, error } = useJobQuery(jobId!);
  const { data: currentUser } = useAuth();
  const { data: applications } = useJobApplicationsQuery(jobId!);
  const createSessionMutation = useCreateSessionMutation();

  // Check if user has already applied (either from server or locally)
  const hasApplied = useMemo(() => {
    if (hasAppliedLocally) return true;
    
    if (applications && currentUser) {
      return applications.applications.some(app => app.userId === currentUser.id);
    }
    
    return false;
  }, [hasAppliedLocally, applications, currentUser]);

  const handleApplicationSubmitted = () => {
    setHasAppliedLocally(true);
  };

  const handleStartLearningSession = async () => {
    if (!job) return;
    
    setIsCreatingSession(true);
    
    try {
      // Create a new session
      const newSession = await createSessionMutation.mutateAsync({
        sessionName: `Job Preparation: ${job.title}`,
        description: `Learning session to prepare for the ${job.title} position at ${job.companyName}`,
      });

      // Send the initial message to the chat
      const session = Session(newSession.id);
      const message = `Can you help me get ready for this job?

**Job Title:** ${job.title}

**Job Description:**
${job.content}

**Required Skills/Tags:** ${job.tags.join(", ")}`;

      // Wait for the chat stream to complete
      await new Promise<void>((resolve, reject) => {
        session.chat(
          message,
          // onMessage - we don't care about the stream events
          () => {},
          // onError
          (error) => reject(error),
          // onComplete
          () => resolve()
        );
      });

      // Navigate to the session page
      navigate(`/roadmaps/${newSession.id}`);
    } catch (error) {
      console.error("Failed to create learning session:", error);
      // You might want to show an error toast here
    } finally {
      setIsCreatingSession(false);
    }
  };

  if (!jobId) {
    return (
      <div className="page-transition p-6">
        <div className="text-center py-12">
          <p className="text-red-500">Invalid job ID</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="page-transition p-6">
        <div className="flex justify-center items-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
        </div>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="page-transition p-6">
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold mb-2 text-red-500">Job Not Found</h2>
          <p className="text-muted-foreground mb-4">
            The requested job could not be loaded
          </p>
          <Button variant="outline" onClick={() => navigate("/jobs")}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Jobs
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-transition p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Button
            variant="ghost"
            onClick={() => navigate("/jobs")}
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Jobs
          </Button>
          
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{job.title}</h1>
              <div className="flex items-center gap-4 text-muted-foreground mb-4">
                <div className="flex items-center gap-1">
                  <Building className="w-4 h-4" />
                  <span>{job.companyName}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      job.active ? "bg-green-500" : "bg-gray-400"
                    }`}
                  />
                  <span>{job.active ? "Active" : "Inactive"}</span>
                </div>
              </div>
            </div>
            
            <div className="flex gap-3 ml-4">
              {hasApplied ? (
                <Button
                  variant="secondary"
                  size="lg"
                  disabled
                  className="bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400"
                >
                  <Clock className="w-4 h-4 mr-2" />
                  Pending
                </Button>
              ) : (
                <ApplyJobDialog job={job} onApplicationSubmitted={handleApplicationSubmitted} />
              )}
              
              <Button
                onClick={handleStartLearningSession}
                disabled={isCreatingSession || !job.active}
                size="lg"
                variant="outline"
              >
                {isCreatingSession ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Creating Session...
                  </>
                ) : (
                  <>
                    <GraduationCap className="w-4 h-4 mr-2" />
                    Start Learning Session
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Job Content */}
        <div className="bg-card rounded-lg p-6 border mb-6">
          <h2 className="text-xl font-semibold mb-4">Job Description</h2>
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <p className="whitespace-pre-wrap">{job.content}</p>
          </div>
        </div>

        {/* Tags */}
        {job.tags && job.tags.length > 0 && (
          <div className="bg-card rounded-lg p-6 border">
            <h2 className="text-xl font-semibold mb-4">Required Skills & Technologies</h2>
            <div className="flex flex-wrap gap-2">
              {job.tags.map((tag, index) => (
                <Badge key={index} variant="secondary" className="text-sm">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Apply Section */}
        <div className="mt-8 bg-linear-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-lg p-6 border">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/40 rounded-lg flex items-center justify-center">
              {hasApplied ? (
                <Clock className="w-6 h-6 text-green-600 dark:text-green-400" />
              ) : (
                <Building className="w-6 h-6 text-green-600 dark:text-green-400" />
              )}
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-1">
                {hasApplied ? "Application Submitted" : "Apply for This Position"}
              </h3>
              <p className="text-muted-foreground text-sm">
                {hasApplied 
                  ? "Your application has been submitted successfully. The employer will review it and get back to you."
                  : "Submit your application for this position. You can include an optional cover letter to stand out."
                }
              </p>
            </div>
            {hasApplied ? (
              <Button
                variant="secondary"
                size="lg"
                disabled
                className="bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400"
              >
                <Clock className="w-4 h-4 mr-2" />
                Pending
              </Button>
            ) : (
              <ApplyJobDialog job={job} onApplicationSubmitted={handleApplicationSubmitted} />
            )}
          </div>
        </div>

        {/* Learning Session CTA */}
        <div className="mt-6 bg-linear-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg p-6 border">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/40 rounded-lg flex items-center justify-center">
              <GraduationCap className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-1">Get Ready for This Job</h3>
              <p className="text-muted-foreground text-sm">
                Start a personalized learning session to prepare for this position. 
                Our AI will create a tailored roadmap based on the job requirements.
              </p>
            </div>
            <Button
              onClick={handleStartLearningSession}
              disabled={isCreatingSession || !job.active}
              size="lg"
              variant="outline"
            >
              {isCreatingSession ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <GraduationCap className="w-4 h-4 mr-2" />
                  Start Learning
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}