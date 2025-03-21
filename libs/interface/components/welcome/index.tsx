interface WelcomeProps {
  isLoading?: boolean;
}
  const [userData, setUserData] = useState<any>(null);

export function Welcome({isLoading = false }: WelcomeProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh]">
       <h1 className="text-3xl font-bold text-white">Welcome, Robin!</h1>
      
      {isLoading ? (
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
          <p className="text-muted-foreground">Loading desktop environment...</p>
        </div>
      ) : (
        <p>Your application is ready!</p>
      )}
    </div>
  );
}