import { SearchPageContextProvider } from "./context";
import { Step1Ui } from "./step1-ui";

export function SearchPage() {
  return (
    <SearchPageContextProvider>
      <main className="flex flex-col gap-4 p-4 max-w-screen-md mx-auto mb-24">
        <Step1Ui />
      </main>
    </SearchPageContextProvider>
  );
}
