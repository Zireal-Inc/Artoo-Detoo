import { Button} from "@r2d2/ui";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <h1 className="text-4xl sm:text-5xl font-bold text-center sm:text-left">
          Welcome to <a href="#">Z</a>
        </h1>
          
        <p className="text-lg text-center sm:text-left">
          This is a simple example of a Next.js application.
        </p>

        <Button variant="destructive">Click Me</Button> 
        <Button variant="default" >Go to Next Page</Button>

      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
       <div className="flex gap-2 items-center">
          <span className="text-xs text-center sm:text-left">
            @Year Robin
          </span>
        </div>
      </footer>
    </div>
  );
}
