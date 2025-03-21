export function DesktopComponent() {
  return (
    <div className="container mx-auto px-4">
      <header className="py-6 border-b mb-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <div className="flex items-center gap-4">
            <button className="px-3 py-2 rounded-md bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700">
              Notifications
            </button>
            <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center">
              U
            </div>
          </div>
        </div>
      </header>
      
      <main>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <div className="bg-card rounded-lg border p-6 h-[300px] flex items-center justify-center">
              <span className="text-muted-foreground">Main Content Area</span>
            </div>
          </div>
          <div>
            <div className="bg-card rounded-lg border p-6 h-[300px] flex items-center justify-center">
              <span className="text-muted-foreground">Sidebar</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}