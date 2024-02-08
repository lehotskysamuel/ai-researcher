import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AlertCircle, Play } from "lucide-react";
import { useState } from "react";
import { TypographyH1 } from "@/components/ui/typography";
import { useSearchPageDispatch, useSearchPageState } from "./context";
import { Loading } from "@/components/custom/loading";
import { Spinner } from "@/components/custom/spinner";
import { Step2Ui } from "./step2-ui";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export function Step1Ui() {
  const state = useSearchPageState();
  const dispatch = useSearchPageDispatch();

  return (
    <>
      <TypographyH1>AI Researcher</TypographyH1>

      <SearchInput
        isLoading={state.configTemplateState === "loading"}
        onSubmit={(userQuery) =>
          dispatch({ type: "SUBMIT_USER_QUERY", userQuery })
        }
      />

      {state.configTemplateState === "loading" && (
        <Loading text="Generating search queries..." />
      )}

      {state.configTemplateState === "error" && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error!</AlertTitle>
          <AlertDescription>{state.error}</AlertDescription>
        </Alert>
      )}

      {state.configTemplateState === "success" && <Step2Ui />}
    </>
  );
}

function SearchInput(props: {
  isLoading: boolean;
  onSubmit: (userQuery: string) => void;
}) {
  const [userQuery, setUserQuery] = useState<string>(
    // todo zmazat tuto otazku a nechat prazdne
    "What's an average lifespan in Europe and Slovakia?"
  );

  return (
    <div className="flex items-center gap-4 mb-4">
      <Input
        className="flex-1 p-2 border border-gray-200 rounded-md dark:border-gray-800"
        placeholder="Ask a question"
        value={userQuery}
        onChange={(e) => setUserQuery(e.target.value)}
      />

      {/* todo disable on load */}
      <Button onClick={() => props.onSubmit(userQuery)}>
        {props.isLoading ? (
          <Spinner size={16} className="mr-2" />
        ) : (
          <Play size={16} className="mr-2" />
        )}
        Start
      </Button>
    </div>
  );
}
