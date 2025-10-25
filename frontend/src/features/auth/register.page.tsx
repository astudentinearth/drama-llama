import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useRegisterMutation } from "./auth.mutation";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [userType, setUserType] = useState<"recruiter" | "jobhunter" | null>(null);
  const mutation = useRegisterMutation();

  const handleRegister = () => {
    if (userType && username && password && email) {
      mutation.mutate({
        username,
        password,
        email,
        recruiter: userType === "recruiter",
      });
    }
  };

  return (
    <Card className="w-96 page-transition h-fit p-4 px-6 pb-6 gap-4 absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2">
      <span className="flex w-full text-center justify-center font-extrabold text-brand text-4xl">
        GrowthWay
      </span>
      <div />
      <h1 className="text-2xl">Create account</h1>
      
      <Label>I am a...</Label>
      <div className="flex gap-2">
        <Button
          variant={userType === "jobhunter" ? "default" : "outline"}
          onClick={() => setUserType("jobhunter")}
          className="flex-1"
        >
          Job Hunter
        </Button>
        <Button
          variant={userType === "recruiter" ? "default" : "outline"}
          onClick={() => setUserType("recruiter")}
          className="flex-1"
        >
          Recruiter
        </Button>
      </div>

      <Label>Username</Label>
      <Input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter your username"
      />
      
      <Label>Email</Label>
      <Input
        value={email}
        type="email"
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      
      <Label>Password</Label>
      <Input
        value={password}
        type="password"
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter your password"
      />
      
      <Button
        onClick={handleRegister}
        disabled={!username || !password || !email || !userType || mutation.isPending}
      >
        Create account
      </Button>
      
      <hr />
      
      <span className="flex justify-center gap-2">
        Already have an account?{" "}
        <Link className="text-primary hover:underline" to={"/login"}>
          Sign in
        </Link>
      </span>
    </Card>
  );
}