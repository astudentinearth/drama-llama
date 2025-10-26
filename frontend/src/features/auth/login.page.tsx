import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useLoginMutation } from "./auth.mutation";
import Logo from "@/components/logo";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const mutation = useLoginMutation();
  return (
    <Card className="w-96 page-transition h-fit p-4 px-6 pb-6 gap-4 absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2">
      <Logo />
      <div />
      <h1 className="text-2xl">Sign in</h1>
      <Label>Username</Label>
      <Input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter your username"
      />
      <Label>Password</Label>
      <Input
        value={password}
        type="password"
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter your password"
      />
      <Button
        onClick={() => mutation.mutate({ username, password })}
        disabled={!username || !password || mutation.isPending}
      >
        Sign in
      </Button>
      <hr></hr>
      <span className="flex justify-center gap-2">
        Don&apos;t have an account?{" "}
        <Link className="text-primary hover:underline" to={"/register"}>
          Create account
        </Link>
      </span>
    </Card>
  );
}
