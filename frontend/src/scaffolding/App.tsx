import { QueryClient, QueryClientProvider } from "react-query";
import ErrorBoundary from "./error-boundary";
import { SearchPage } from "@/pages/search-page/search-page";

const queryClient = new QueryClient();

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <SearchPage />
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
