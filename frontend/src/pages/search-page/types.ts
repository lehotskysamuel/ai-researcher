import googleLogo from "super-tiny-icons/images/svg/google.svg";
import bingLogo from "super-tiny-icons/images/svg/bing.svg";
import redditLogo from "super-tiny-icons/images/svg/reddit.svg";
import duckDuckGoLogo from "super-tiny-icons/images/svg/duckduckgo.svg";
import { Immutable } from "immer";

type LoadingState = "idle" | "loading" | "error" | "success";

export enum SearchEngineEnum {
  Google = "google",
  Bing = "bing",
  DuckDuckGo = "duckduckgo",
  Reddit = "reddit",
}

type SearchEngineDisplayData = {
  displayName: string;
  logo: string;
};

export const SEARCH_ENGINES: Immutable<
  Record<SearchEngineEnum, SearchEngineDisplayData>
> = {
  google: {
    displayName: "Google",
    logo: googleLogo,
  },
  bing: {
    displayName: "Bing",
    logo: bingLogo,
  },
  duckduckgo: {
    displayName: "DuckDuckGo",
    logo: duckDuckGoLogo,
  },
  reddit: {
    displayName: "Reddit",
    logo: redditLogo,
  },
};

type SearchConfig = {
  searchQueries: string[];
  searchEngineConfigs: SearchEngineConfig[];
};

export type SearchEngineConfig = {
  enabled: boolean;
  searchEngine: SearchEngineEnum;
  maxResults: number;
};

export type SearchPageState = Immutable<{
  error: string | null;
  configTemplateState: LoadingState;
  searchConfig: SearchConfig;
}>;

export type SearchPageAction =
  | { type: "SUBMIT_USER_QUERY"; userQuery: string }
  | { type: "SUBMIT_USER_QUERY_FAILED"; error: Error }
  | { type: "UPDATE_SEARCH_QUERIES"; searchQueries: string[] }
  | { type: "CREATE_SEARCH_QUERY" }
  | { type: "UPDATE_SEARCH_QUERY"; index: number; searchQuery: string }
  | { type: "DELETE_SEARCH_QUERY"; index: number }
  | {
      type: "UPDATE_SEARCH_ENGINE_CONFIG";
      index: number;
      searchEngineConfig: SearchEngineConfig;
    }
  | {
      type: "SELECT_SEARCH_ENGINE_CONFIGS";
      indexes: number[];
    }
  | {
      type: "UPDATE_SEARCH_ENGINE_CONFIGS";
      maxResults: number;
    };
