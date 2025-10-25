import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Edit } from "lucide-react";
import { useUpdateCompanyMutation } from "./company.mutation";
import type { Company } from "./company.types";

interface EditCompanyDialogProps {
  company: Company;
}

export default function EditCompanyDialog({ company }: EditCompanyDialogProps) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState(company.name);
  const [description, setDescription] = useState(company.description || "");
  
  const updateCompanyMutation = useUpdateCompanyMutation();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    updateCompanyMutation.mutate(
      {
        companyId: company.id,
        data: { name, description },
      },
      {
        onSuccess: () => {
          setOpen(false);
        },
      }
    );
  };

  const handleOpenChange = (newOpen: boolean) => {
    if (!newOpen) {
      // Reset form when closing
      setName(company.name);
      setDescription(company.description || "");
    }
    setOpen(newOpen);
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Edit className="w-4 h-4 mr-2" />
          Edit Company
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Company</DialogTitle>
          <DialogDescription>
            Update your company information. Changes will be visible to all users.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Company Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter company name"
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter company description"
              rows={4}
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={updateCompanyMutation.isPending}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={updateCompanyMutation.isPending || !name.trim()}
            >
              {updateCompanyMutation.isPending ? "Updating..." : "Update Company"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}