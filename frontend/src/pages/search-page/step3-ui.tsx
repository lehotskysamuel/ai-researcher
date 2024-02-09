import ClickableText from "@/components/custom/clickable-text";
import { Loading } from "@/components/custom/loading";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ProgressWithPercentage } from "@/components/ui/progress";
import { LabeledSwitch } from "@/components/ui/switch";
import { TypographyH2 } from "@/components/ui/typography";
import { cn, createSequenceArray } from "@/lib/utils";
import { Immutable } from "immer";
import { ArrowDownToLine, Check, FolderSearch, X } from "lucide-react";
import { useSearchPageDispatch, useSearchPageState } from "./context";
import { SEARCH_ENGINES, SearchResult } from "./types";

export function Step3Ui() {
  const state = useSearchPageState();
  const dispatch = useSearchPageDispatch();

  const selectedResultsCount = state.searchResults.filter(
    (sr) => sr.enabled
  ).length;
  const downloadedResultsCount = state.searchResults.filter(
    (sr) =>
      sr.enabled &&
      (sr.details.state === "success" || sr.details.state === "error")
  ).length;
  const someResultsEnabled = selectedResultsCount > 0;
  const allResultsDownloaded = downloadedResultsCount === selectedResultsCount;
  const someResultsLoading = state.searchResults.some(
    (sr) => sr.details.state === "loading"
  );

  return (
    <>
      <hr className="m-8" />
      <TypographyH2>
        <span className="text-muted-foreground">Step 3 / </span>Select Search
        Results to Download
      </TypographyH2>

      <div className="flex flex-row flex-wrap">
        {state.searchResults.map((sr, index) => (
          <SearchResultCard
            key={sr.url}
            searchResult={sr}
            onEnabledChanged={(newEnabled) =>
              dispatch({
                type: "SELECT_SEARCH_RESULTS",
                indexes: [index],
                operation: newEnabled ? "add" : "remove",
              })
            }
          />
        ))}
      </div>

      <div className="flex space-x-4">
        <Button
          variant={"outline"}
          onClick={() =>
            dispatch({
              type: "SELECT_SEARCH_RESULTS",
              indexes: createSequenceArray(state.searchResults.length),
              operation: "set",
            })
          }
        >
          <Check size={16} className="mr-2" />
          Select All
        </Button>
        <Button
          variant={"outline"}
          onClick={() =>
            dispatch({
              type: "SELECT_SEARCH_RESULTS",
              indexes: [],
              operation: "set",
            })
          }
        >
          <X size={16} className="mr-2" />
          Select None
        </Button>
      </div>

      {!(someResultsEnabled && allResultsDownloaded) && (
        <>
          <Button disabled={!someResultsEnabled} className="my-4">
            <ArrowDownToLine size={16} className="mr-2" />
            Download Content
          </Button>
          {someResultsLoading && <Loading text="Downloading..." />}
          Progress:
          <ProgressWithPercentage
            finished={downloadedResultsCount}
            total={selectedResultsCount}
          />
        </>
      )}

      {someResultsEnabled && allResultsDownloaded && (
        <>
          <Button className="my-4">
            <FolderSearch size={16} className="mr-2" />
            Load Content to Knowledge Base
          </Button>
          <Loading text="Indexing..." />
          <ProgressWithPercentage finished={3} total={4} />
        </>
      )}
    </>
  );
}

const SearchResultCard = (props: {
  searchResult: Immutable<SearchResult>;
  onEnabledChanged: (newEnabled: boolean) => void;
}) => {
  const { searchResult, onEnabledChanged } = props;
  return (
    <div className="basis-1/2 p-2 odd:pl-0 even:pr-0">
      <Card
        className={cn({
          "opacity-50": !searchResult.enabled,
        })}
      >
        <CardHeader>
          <CardTitle className="flex gap-4">
            <div className="flex flex-col gap-2">
              <LabeledSwitch
                label={
                  <div className="flex items-center gap-2">
                    {searchResult.searchEngines.map((se, index) => (
                      <img
                        key={index}
                        className="w-6 h-6"
                        src={SEARCH_ENGINES[se]?.logo}
                        alt={SEARCH_ENGINES[se]?.displayName}
                      />
                    ))}
                  </div>
                }
                checked={searchResult.enabled}
                onCheckedChange={onEnabledChanged}
              />
              {/* todo proper url, open in new tab */}
              <ClickableText className="text-sm text-muted-foreground">
                {searchResult.url}
              </ClickableText>
              <span>{searchResult.title}</span>
            </div>
          </CardTitle>

          <CardDescription className="line-clamp-3">
            {searchResult.description}
          </CardDescription>
        </CardHeader>

        {searchResult.details.state !== "idle" && (
          <CardFooter>
            {searchResult.details.state === "success" && (
              <div className="w-full flex items-center justify-between">
                <span className="text-green-500">Successful</span>
                {/* todo dialog searchResult.details.htmlPreview */}
                <Button variant={"secondary"}>Preview</Button>
              </div>
            )}
            {searchResult.details.state === "error" && (
              <div className="w-full flex items-center justify-between">
                <span className="text-red-500 font-bold">Failed!</span>
                {/* todo searchResult.details.error */}
                <Button variant={"secondary"}>Details</Button>
              </div>
            )}
          </CardFooter>
        )}
      </Card>
    </div>
  );
};
