import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/features/auth/auth.query";
import { User } from "lucide-react";
import { useParams } from "react-router-dom";
import EditProfileDialog from "./edit-profile-dialog";
import { useUserProfile } from "./profile.query";

export default function ProfilePage() {
  const { userId } = useParams<{ userId: string }>();
  const { data: currentUser } = useAuth();
  
  // Use the userId from URL params, or fall back to current user's ID
  const profileUserId = userId || currentUser?.id;
  
  const { data: profileData, isLoading, error } = useUserProfile(profileUserId!);

  if (!profileUserId) {
    return (
      <div className="page-transition flex items-center justify-center min-h-[400px]">
        <div className="text-muted-foreground">Please log in to view profiles</div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="page-transition flex items-center justify-center min-h-[400px]">
        <div className="text-muted-foreground">Loading profile...</div>
      </div>
    );
  }

  if (error || !profileData) {
    return (
      <div className="page-transition flex items-center justify-center min-h-[400px]">
        <div className="text-destructive">Failed to load profile</div>
      </div>
    );
  }

  const { profile } = profileData;
  const isOwnProfile = !userId || userId === currentUser?.id;

  return (
    <div className="page-transition container mx-auto py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                <User className="h-8 w-8 text-primary" />
              </div>
              <div>
                <CardTitle className="text-2xl">{profile.fullName}</CardTitle>
                <p className="text-muted-foreground">{profile.jobTitle}</p>
              </div>
            </div>
            {isOwnProfile && <EditProfileDialog profile={profile} />}
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-3">Skills</h3>
              {profile.skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill, index) => (
                    <Badge key={index} variant="secondary">
                      {skill}
                    </Badge>
                  ))}
                </div>
              ) : (
                <p className="text-muted-foreground">No skills listed</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
