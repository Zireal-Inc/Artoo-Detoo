import React, { useState } from 'react';
import { LoginForm } from './login-form';
import { SignupForm } from './signup-form';
import { Welcome } from '../welcome';
// import { StarFieldBackground } from '../star-field-background';
import { Button } from '@r2d2/ui';

type AuthView = 'login' | 'signup' | 'welcome';

interface AuthFlowProps {
  onAuthSuccess?: (userData?: any) => void;
  defaultView?: AuthView;
}

export function AuthFlow({ 
  onAuthSuccess, 
  defaultView = 'login' 
}: AuthFlowProps) {
  const [currentView, setCurrentView] = useState<AuthView>(defaultView);
  const [userData, setUserData] = useState<any>(null);

  const handleLoginSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would normally handle actual authentication
    // For demo purposes, we'll just simulate successful login
    const mockUserData = {
      name: "Demo User",
      email: "demo@example.com",
    };
    setUserData(mockUserData);
    setCurrentView('welcome');
    onAuthSuccess?.(mockUserData);
  };

  const handleSignupSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would normally handle actual registration
    // For demo purposes, we'll just simulate successful signup
    const mockUserData = {
      name: "New User",
      email: "new@example.com",
    };
    setUserData(mockUserData);
    setCurrentView('welcome');
    onAuthSuccess?.(mockUserData);
  };

  const handleLogout = () => {
    setUserData(null);
    setCurrentView('login');
  };

  return (
    <div className="relative min-h-screen w-full">
      {/* <StarFieldBackground /> */}
      
      <div className="relative z-10 flex min-h-screen items-center justify-center p-4">
        {currentView === 'login' && (
          <LoginForm 
            onSubmit={handleLoginSubmit}
            onSignupClick={() => setCurrentView('signup')}
          />
        )}
        
        {currentView === 'signup' && (
          <SignupForm 
            onSubmit={handleSignupSubmit}
            onLoginClick={() => setCurrentView('login')}
          />
        )}
        
        {currentView === 'welcome' && (
         <Welcome  />
        )}
      </div>
    </div>
  );
}

