import { Draft } from "immer";
import { SearchPageState, SearchPageAction, SearchEngineEnum } from "./types";
import { assertNever } from "@/lib/utils";

export const initialState: SearchPageState = {
  configTemplateState: "idle",
  searchConfig: {
    searchQueries: [],
    searchEngineConfigs: Object.values(SearchEngineEnum).map(
      (searchEngine) => ({
        enabled: true,
        maxResults: 3,
        searchEngine: searchEngine,
      })
    ),
  },
  searchState: "idle",
  searchResults: [],
  error: null,
};

export function searchPageReducer(
  draft: Draft<SearchPageState>,
  action: SearchPageAction
) {
  switch (action.type) {
    case "SUBMIT_USER_QUERY":
      draft.configTemplateState = "loading";
      break;
    case "SUBMIT_USER_QUERY_FAILED":
      console.error(action.error);
      draft.error = action.error.message;
      draft.configTemplateState = "error";
      break;
    case "UPDATE_ALL_SEARCH_QUERIES":
      draft.configTemplateState = "success";
      draft.searchConfig.searchQueries = action.searchQueries;
      break;
    case "UPDATE_SEARCH_QUERY":
      draft.searchConfig.searchQueries[action.index] = action.searchQuery;
      break;
    case "CREATE_SEARCH_QUERY":
      draft.searchConfig.searchQueries.push("");
      break;
    case "DELETE_SEARCH_QUERY":
      draft.searchConfig.searchQueries.splice(action.index, 1);
      break;
    case "SELECT_SEARCH_ENGINE_CONFIGS":
      draft.searchConfig.searchEngineConfigs.forEach((sec, index) => {
        sec.enabled = action.indexes.includes(index);
      });
      break;
    case "UPDATE_SEARCH_ENGINE_CONFIG":
      draft.searchConfig.searchEngineConfigs[action.index] =
        action.searchEngineConfig;
      break;
    case "UPDATE_SEARCH_ENGINE_CONFIGS":
      draft.searchConfig.searchEngineConfigs.forEach((sec) => {
        sec.maxResults = action.maxResults;
      });
      break;
    case "UPDATE_ALL_SEARCH_RESULTS":
      draft.searchResults = action.searchResults;
      break;
    case "UPDATE_SEARCH_RESULT":
      draft.searchResults[action.index] = action.searchResult;
      break;
    case "SEARCH":
      draft.searchState = "loading";
      break;
    case "SEARCH_FAILED":
      console.error(action.error);
      draft.error = action.error.message;
      draft.searchState = "error";
      break;
    default:
      assertNever(action);
  }
}
