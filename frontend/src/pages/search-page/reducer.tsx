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
    case "SEARCH":
      draft.searchState = "loading";
      break;
    case "SEARCH_FAILED":
      console.error(action.error);
      draft.error = action.error.message;
      draft.searchState = "error";
      break;
    case "UPDATE_ALL_SEARCH_RESULTS":
      draft.searchState = "success";
      draft.searchResults = action.searchResults;
      break;
    case "UPDATE_SEARCH_RESULT_DETAILS":
      draft.searchResults[action.searchResultIndex].details =
        action.searchResultDetails;
      break;
    case "SELECT_SEARCH_RESULTS":
      draft.searchResults.forEach((searchResult, index) => {
        const searchResultInArray = action.indexes.includes(index);
        if (action.operation === "set") {
          searchResult.enabled = searchResultInArray;
        } else {
          if (searchResultInArray) {
            searchResult.enabled = action.operation === "add";
          }
        }
      });
      break;
    case "DOWNLOAD_CONTENT":
      draft.searchResults
        .filter((sr) => sr.enabled && sr.details.state === "idle")
        .forEach((searchResult) => {
          searchResult.details = { state: "loading" };
        });
      break;
    default:
      assertNever(action);
  }
}
