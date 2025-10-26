import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Briefcase, Loader2 } from "lucide-react";
import { useApplyToJobMutation } from "./jobs.query";
import type { JobListing } from "./jobs.types";

interface ApplyJobDialogProps {
  job: JobListing;
  onApplicationSubmitted: () => void;
}

export default function ApplyJobDialog({ job, onApplicationSubmitted }: ApplyJobDialogProps) {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  
  const applyMutation = useApplyToJobMutation();

  const handleSubmit = () => {
    applyMutation.mutate(
      {
        jobId: job.id,
        message: message.trim() || "I am interested in this position and would like to apply.",
      },
      {
        onSuccess: () => {
          setOpen(false);
          setMessage("");
          onApplicationSubmitted();
        },
      }
    );
  };

  const handleOpenChange = (newOpen: boolean) => {
    if (!newOpen) {
      // Reset form when closing
      setMessage("");
    }
    setOpen(newOpen);
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button size="lg">
          <Briefcase className="w-4 h-4 mr-2" />
          Apply Now
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Apply for {job.title}</DialogTitle>
          <DialogDescription>
            Submit your application for this position at {job.companyName}. 
            You can include an optional cover letter or message.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="message">Cover Letter / Message (Optional)</Label>
            <Textarea
              id="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Tell the employer why you're interested in this position and what makes you a good fit..."
              rows={6}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground">
              If left empty, a default message will be sent with your application.
            </p>
          </div>
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => setOpen(false)}
            disabled={applyMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={applyMutation.isPending}
          >
            {applyMutation.isPending ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <Briefcase className="w-4 h-4 mr-2" />
                Submit Application
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}