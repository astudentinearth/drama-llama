import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Edit } from "lucide-react";
import { useState } from "react";
import { useUpdateProfile } from "./profile.mutation";
import type { UpdateProfileDTO, UserProfileDTO } from "./profile.types";

interface EditProfileDialogProps {
  profile: UserProfileDTO;
}

export default function EditProfileDialog({ profile }: EditProfileDialogProps) {
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState<UpdateProfileDTO>({
    fullName: profile.fullName,
    jobTitle: profile.jobTitle,
    skills: profile.skills,
  });

  const updateProfileMutation = useUpdateProfile();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfileMutation.mutate(
      { userId: profile.userId, data: formData },
      {
        onSuccess: () => {
          setOpen(false);
        },
      }
    );
  };

  const handleSkillsChange = (value: string) => {
    const skills = value.split(",").map((skill) => skill.trim()).filter(Boolean);
    setFormData({ ...formData, skills });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Edit className="h-4 w-4 mr-2" />
          Edit Profile
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Profile</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="fullName">Full Name</Label>
            <Input
              id="fullName"
              value={formData.fullName}
              onChange={(e) =>
                setFormData({ ...formData, fullName: e.target.value })
              }
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="jobTitle">Job Title</Label>
            <Input
              id="jobTitle"
              value={formData.jobTitle}
              onChange={(e) =>
                setFormData({ ...formData, jobTitle: e.target.value })
              }
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="skills">Skills (comma-separated)</Label>
            <Textarea
              id="skills"
              value={formData.skills.join(", ")}
              onChange={(e) => handleSkillsChange(e.target.value)}
              placeholder="React, TypeScript, Node.js"
              rows={3}
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={updateProfileMutation.isPending}
            >
              {updateProfileMutation.isPending ? "Saving..." : "Save Changes"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}