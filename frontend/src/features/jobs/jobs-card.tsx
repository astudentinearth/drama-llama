import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Link } from "react-router-dom";
import type { JobListing } from "./jobs.types";

interface JobsCardProps {
  job: JobListing;
}

export default function JobsCard({ job }: JobsCardProps) {
  return (
    <Link to={`/jobs/${job.id}`}>
      <Card className="h-full rounded-3xl hover:bg-card/50 cursor-pointer transition-colors">
        <CardHeader>
          <CardTitle className="text-lg">{job.title}</CardTitle>
          <CardDescription className="text-sm text-muted-foreground">
            <Link 
              to={`/company/${job.companyId}`}
              className="hover:text-primary hover:underline"
              onClick={(e) => e.stopPropagation()}
            >
              {job.companyName}
            </Link>
            &nbsp;|&nbsp;
            {job.active ? "Active" : "Inactive"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm line-clamp-3">{job.content}</p>
          {job.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {job.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}