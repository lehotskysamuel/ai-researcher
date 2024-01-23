import { useState } from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import ErrorBoundary from "./error-boundary";
import { SearchPage } from "../components/search-page";
import { SearchResultsPage } from "../components/search-results-page";

const queryClient = new QueryClient();

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <SearchPage></SearchPage>
        <SearchResultsPage></SearchResultsPage>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
