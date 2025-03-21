import React, { useState, useEffect } from 'react';
import { LoginForm } from '../components/Auth/login-form';
import { SignupForm } from '../components/Auth/signup-form';
import { Welcome } from '../components/welcome';
import { DesktopComponent } from '../components/desktop';
import { StarFieldBackground } from '../components/star-field-background'; 

export function InterfaceApp() {
  const [currentPage, setCurrentPage] = useState<'login' | 'signup' | 'welcome' | 'desktop'>('login');
  const [isLoading, setIsLoading] = useState(false);

  // Function to handle login submission
  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setCurrentPage('welcome');

    // Simulate loading time for desktop component
    setTimeout(() => {
      setCurrentPage('desktop');
      setIsLoading(false);
    }, 3000);
  };

  // Function to navigate between login and signup
  const navigateToLogin = () => setCurrentPage('login');
  const navigateToSignup = () => setCurrentPage('signup');

  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
      {currentPage === 'login' && (
        <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
            <StarFieldBackground />
          <div className="w-full max-w-sm md:max-w-3xl">
            <LoginForm
              onSubmit={handleLogin}
              onSignupClick={navigateToSignup}
            />
          </div>
        </div>
      )}

      {currentPage === 'signup' && (
        <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
          <div className="w-full max-w-sm md:max-w-3xl">
            <SignupForm
              onSubmit={handleLogin}
              onLoginClick={navigateToLogin}
            />
          </div>
        </div>
      )}

      {currentPage === 'welcome' && (
        <Welcome isLoading={isLoading} />
      )}

      {currentPage === 'desktop' && (
        <DesktopComponent />
      )}
    </div>
  );
}
