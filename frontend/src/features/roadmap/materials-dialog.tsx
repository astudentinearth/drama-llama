import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { BookOpen, Clock, CheckCircle, Circle } from "lucide-react";
import type { IMaterial } from "./roadmap.types";

interface MaterialsDialogProps {
  materials: IMaterial[];
  goalTitle: string;
}

export default function MaterialsDialog({ materials, goalTitle }: MaterialsDialogProps) {
  const [open, setOpen] = useState(false);
  const [selectedMaterial, setSelectedMaterial] = useState<IMaterial | null>(null);

  const getDifficultyColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "beginner":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
      case "intermediate":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300";
      case "advanced":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300";
    }
  };

  const getTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case "video":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300";
      case "article":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300";
      case "exercise":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300";
      case "project":
        return "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300";
    }
  };

  const formatTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <BookOpen className="w-4 h-4 mr-2" />
          View Materials ({materials.length})
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[1400px] max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle>Learning Materials</DialogTitle>
          <DialogDescription>
            Materials for: {goalTitle}
          </DialogDescription>
        </DialogHeader>
        
        <div className="flex flex-1 gap-4 overflow-hidden">
          {/* Materials List */}
          <div className="w-80 border-r pr-4 overflow-y-auto">
            <div className="space-y-2">
              {materials.map((material) => (
                <div
                  key={material.id}
                  className={`p-3 rounded-lg border cursor-pointer transition-colors hover:bg-accent ${
                    selectedMaterial?.id === material.id ? "bg-accent" : ""
                  }`}
                  onClick={() => setSelectedMaterial(material)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-sm line-clamp-2">{material.title}</h4>
                    {material.is_completed ? (
                      <CheckCircle className="w-4 h-4 text-green-500 shrink-0 ml-2" />
                    ) : (
                      <Circle className="w-4 h-4 text-gray-400 shrink-0 ml-2" />
                    )}
                  </div>
                  
                  <div className="flex flex-wrap gap-1 mb-2">
                    <Badge variant="secondary" className={`text-xs ${getTypeColor(material.material_type)}`}>
                      {material.material_type}
                    </Badge>
                    <Badge variant="secondary" className={`text-xs ${getDifficultyColor(material.difficulty_level)}`}>
                      {material.difficulty_level}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Clock className="w-3 h-3" />
                    {formatTime(material.estimated_time_minutes)}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Material Content */}
          <div className="flex-1 overflow-y-auto">
            {selectedMaterial ? (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold mb-2">{selectedMaterial.title}</h3>
                  <div className="flex items-center gap-2 mb-4">
                    <Badge className={getTypeColor(selectedMaterial.material_type)}>
                      {selectedMaterial.material_type}
                    </Badge>
                    <Badge className={getDifficultyColor(selectedMaterial.difficulty_level)}>
                      {selectedMaterial.difficulty_level}
                    </Badge>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Clock className="w-4 h-4" />
                      {formatTime(selectedMaterial.estimated_time_minutes)}
                    </div>
                  </div>
                </div>
                
                {selectedMaterial.description && (
                  <div>
                    <h4 className="font-medium mb-2">Description</h4>
                    <p className="text-sm text-muted-foreground mb-4">
                      {selectedMaterial.description}
                    </p>
                  </div>
                )}
                
                {selectedMaterial.content && (
                  <div>
                    <h4 className="font-medium mb-2">Content</h4>
                    <div className="prose prose-sm max-w-none dark:prose-invert">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {selectedMaterial.content}
                      </ReactMarkdown>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full text-muted-foreground">
                Select a material to view its content
              </div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}