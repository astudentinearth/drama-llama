import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Plus } from "lucide-react";
import { useCreateSessionMutation } from "./roadmap.query";

interface CreateSessionDialogProps {
  variant?: "button" | "icon";
  size?: "default" | "sm" | "lg" | "icon" | "icon-sm" | "icon-lg";
}

export default function CreateSessionDialog({ 
  variant = "button", 
  size = "default" 
}: CreateSessionDialogProps) {
  const [open, setOpen] = useState(false);
  const [sessionName, setSessionName] = useState("");
  const [description, setDescription] = useState("");
  const navigate = useNavigate();
  
  const createSessionMutation = useCreateSessionMutation();

  const handleSubmit = () => {
    if (!sessionName.trim()) return;

    createSessionMutation.mutate(
      {
        sessionName: sessionName.trim(),
        description: description.trim(),
      },
      {
        onSuccess: (newSession) => {
          setOpen(false);
          setSessionName("");
          setDescription("");
          // Navigate to the new session
          navigate(`/roadmaps/${newSession.id}`);
        },
      }
    );
  };

  const handleOpenChange = (newOpen: boolean) => {
    console.log(newOpen);
    if (!newOpen) {
      // Reset form when closing
      setSessionName("");
      setDescription("");
    }
    setOpen(newOpen);
  };

  const TriggerButton = () => {
    if (variant === "icon") {
      return (
        <Button onClick={()=>setOpen(true)} variant="ghost" size={size}>
          <Plus className="w-4 h-4" />
        </Button>
      );
    }

    return (
      <Button onClick={()=>setOpen(true)} variant="outline" size={size}>
        <Plus className="w-4 h-4 mr-2" />
        Create Session
      </Button>
    );
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <TriggerButton />
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create Learning Session</DialogTitle>
          <DialogDescription>
            Start a new learning journey. Give your session a name and describe what you want to learn.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="sessionName">Session Name</Label>
            <Input
              id="sessionName"
              value={sessionName}
              onChange={(e) => setSessionName(e.target.value)}
              placeholder="e.g. Learn React Fundamentals"
              required
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what you want to learn and your goals..."
              rows={4}
            />
          </div>
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => setOpen(false)}
            disabled={createSessionMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={createSessionMutation.isPending || !sessionName.trim()}
          >
            {createSessionMutation.isPending ? "Creating..." : "Create Session"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}