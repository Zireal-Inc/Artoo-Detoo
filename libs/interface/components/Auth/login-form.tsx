import React from "react";
import { cn } from "@r2d2/ui";
import { Button } from "@r2d2/ui";
import { Card, CardContent } from "@r2d2/ui";
import { Input } from "@r2d2/ui";
import { Label } from "@r2d2/ui";

interface LoginFormProps extends React.ComponentProps<"div"> {
  onSubmit?: (e: React.FormEvent) => void;
  onSignupClick?: () => void;
}

export function LoginForm({
  className,
  onSubmit,
  onSignupClick,
  ...props
}: LoginFormProps) {
  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={onSubmit}>
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-balance text-muted-foreground">
                  Login to your Zireal Inc account
                </p>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="email@example.com"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                  <a
                    href="#"
                    className="ml-auto text-sm underline-offset-2 hover:underline"
                  >
                    Forgot your password?
                  </a>
                </div>
                <Input id="password" type="password" required />
              </div>
              <Button type="submit" className="w-full">
                Login
              </Button>

               
              <div className="text-center text-sm">
                Don&apos;t have an account?{" "}
                <a 
                  href="#" 
                  className="underline underline-offset-4"
                  onClick={(e) => {
                    e.preventDefault();
                    onSignupClick && onSignupClick();
                  }}
                >
                  Sign up
                </a>
              </div>
            </div>
          </form>
          <div className="relative bg-muted">
           
            <div className="absolute inset-0 z-10 flex items-center justify-center">
              <div className="px-6 text-center text-white">
                <h2 className="text-2xl font-bold tracking-tight">Welcome Back</h2>
                <p className="mt-2">Continue your journey through the cosmos.</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      <div className="text-balance text-center text-xs text-muted-foreground [&_a]:underline [&_a]:underline-offset-4 hover:[&_a]:text-primary">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </div>
    </div>
  )
}
