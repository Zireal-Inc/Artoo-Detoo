import * as React from 'react';
import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';

// import { Button } from "@ui/components/ui/button/button"; 
import { Button } from "@r2d2/ui";
import { InterfaceApp } from '@r2d2/interface';
// import reactLogo from './assets/react.svg';
// import viteLogo from '/vite.svg';
import Home from './pages/home';
import './App.css';

function ViteWelcome() {
  const [count, setCount] = useState(0);

  return (
    <div className="max-w-4xl mx-auto p-8 text-center">
      <div className="flex justify-center gap-8 mb-8">
        <a
          href="https://vite.dev"
          target="_blank"
          className="hover:scale-110 transition-transform"
        >
          <img src="/vite.svg" className="h-24 p-6" alt="Vite logo" />
        </a>
        <a
          href="https://react.dev"
          target="_blank"
          className="hover:scale-110 transition-transform"
        >
          <img
            src="/vite.svg"
            className="h-24 p-6 animate-spin-slow"
            alt="React logo"
          />
        </a>
      </div>
      <h1 className="text-4xl font-bold mb-8">Vite + React</h1>
      <div className="mb-8">
        <Button
          onClick={() => setCount((count) => count + 1)}
          className="mb-4"
        >
          count is {count}
        </Button>
        <p className="text-muted-foreground">
          Edit{' '}
          <code className="text-sm bg-muted px-1 py-0.5 rounded">
            src/App.tsx
          </code>{' '}
          and save to test HMR
        </p>
      </div>
      <p className="text-muted-foreground">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  );
}

// Create a layout component that conditionally renders the navbar
function AppLayout() {
  const location = useLocation();
  const isInterfacePage = location.pathname === "/interface";
  
  return (
    <div>
      {!isInterfacePage && (
        <nav className="p-4">
          <Button asChild variant="secondary" className="mr-2">
            <Link to="/">Vite Demo</Link>
          </Button> 
          
          <Button asChild variant="destructive">
            <Link to="/home">Robin Home</Link>
            
          </Button> 

          <Button asChild variant="ghost">
            <Link to="/interface">@r2d2/interface</Link>
          </Button> 
        </nav>
      )}

      <Routes>
        <Route path="/" element={<ViteWelcome />} />
        <Route path="/home" element={<Home />} />
        <Route path="/interface" element={<InterfaceApp />} /> 
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppLayout />
    </Router>
  );
}

export default App;
