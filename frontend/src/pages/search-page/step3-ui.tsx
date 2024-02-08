import {
  CardTitle,
  CardDescription,
  CardHeader,
  Card,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import ClickableText from "@/components/custom/clickable-text";
import { LabeledSwitch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";
import { SEARCH_ENGINES, SearchEngineEnum } from "./types";
import { TypographyH2, TypographyP } from "@/components/ui/typography";
import { ArrowDownToLine, FolderSearch, FolderSearch2 } from "lucide-react";
import { Progress, ProgressWithPercentage } from "@/components/ui/progress";
import { Loading } from "@/components/custom/loading";

export function Step3Ui() {
  return (
    <>
      <TypographyH2>
        <span className="text-muted-foreground">Step 3 / </span>Select Search
        Results to Download
      </TypographyH2>
      <div className="flex flex-row flex-wrap">
        <SearchResult
          selected={true}
          url="www.example.com"
          title="Card Title"
          searchEngines={[SearchEngineEnum.Google, SearchEngineEnum.Bing]}
          description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
          elementum, orci at volutpat viverra, risus purus aliquet nibh, in
          lacinia libero lorem in est."
          state={SearchResultState.NONE}
        />
        <SearchResult
          selected={true}
          url="www.example.com"
          title="Card Title"
          searchEngines={[SearchEngineEnum.Google]}
          description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
          elementum, orci at volutpat viverra, risus purus aliquet nibh, in
          lacinia libero lorem in est."
          state={SearchResultState.NONE}
        />
        <SearchResult
          selected={true}
          url="www.example.com"
          title="Card Title"
          searchEngines={[SearchEngineEnum.Google, SearchEngineEnum.DuckDuckGo]}
          description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
          elementum, orci at volutpat viverra, risus purus aliquet nibh, in
          lacinia libero lorem in est."
          state={SearchResultState.SUCCESS}
        />
        <SearchResult
          selected={true}
          url="www.example.com"
          title="Card Title"
          searchEngines={[SearchEngineEnum.Google]}
          description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
          elementum, orci at volutpat viverra, risus purus aliquet nibh, in
          lacinia libero lorem in est."
          state={SearchResultState.FAILED}
        />
      </div>

      <div className="flex space-x-4">
        <Button variant={"outline"}>Select All</Button>
        <Button variant={"outline"}>Select None</Button>
      </div>

      <Button className="w-full">
        <ArrowDownToLine size={16} className="mr-2" />
        Download Content
      </Button>
      <Loading text="Downloading..." />
      <ProgressWithPercentage finished={2} total={4} />

      <Button className="w-full">
        <FolderSearch size={16} className="mr-2" />
        Load Content to Knowledge Base
      </Button>
      <Loading text="Indexing..." />
      <ProgressWithPercentage finished={3} total={4} />
    </>
  );
}

enum SearchResultState {
  SUCCESS = "success",
  FAILED = "failed",
  LOADING = "loading",
  NONE = "none",
}

interface SearchResultProps {
  selected: boolean;
  url: string;
  title: string;
  searchEngines: Array<SearchEngineEnum>;
  description: string;
  state: SearchResultState;
}

const SearchResult = (props: SearchResultProps) => {
  return (
    <div className="basis-1/2 p-2 odd:pl-0 even:pr-0">
      <Card
        className={cn({
          "opacity-50": !props.selected,
        })}
      >
        <CardHeader>
          <CardTitle className="flex gap-4">
            <div className="flex flex-col gap-2">
              <LabeledSwitch
                label={
                  <div className="flex items-center gap-2">
                    {props.searchEngines.map((se, index) => (
                      <img
                        key={index}
                        className="w-6 h-6"
                        src={SEARCH_ENGINES[se]?.logo}
                        alt={SEARCH_ENGINES[se]?.displayName}
                      />
                    ))}
                  </div>
                }
                checked={props.selected}
              />
              {/* todo proper url, open in new tab */}
              <ClickableText className="text-sm text-muted-foreground">
                {props.url}
              </ClickableText>
              <span>{props.title}</span>
            </div>
          </CardTitle>

          <CardDescription className="line-clamp-3">
            {props.description}
          </CardDescription>
        </CardHeader>

        {props.state !== SearchResultState.NONE && (
          <CardFooter>
            {props.state === SearchResultState.SUCCESS && (
              <div className="w-full flex items-center justify-between">
                <span className="text-green-500">Successful</span>
                <Button variant={"secondary"}>Preview</Button>
              </div>
            )}
            {props.state === SearchResultState.FAILED && (
              <div className="w-full flex items-center justify-between">
                <span className="text-red-500 font-bold">Failed!</span>
                <Button variant={"secondary"}>Details</Button>
              </div>
            )}
          </CardFooter>
        )}
      </Card>
    </div>
  );
};
