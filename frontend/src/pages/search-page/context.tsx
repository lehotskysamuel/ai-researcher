import * as api from "@/api/apis";
import React, { createContext, useCallback, useContext } from "react";
import { useMutation } from "react-query";
import { useImmerReducer } from "use-immer";
import { initialState, searchPageReducer } from "./reducer";
import {
  SearchEngineEnum,
  SearchPageAction,
  SearchPageState,
  SearchResult,
  SearchResultDetails,
  parseSearchEngine,
} from "./types";

const SearchPageStateContext = createContext<SearchPageState | undefined>(
  undefined
);

const SearchPageDispatchContext = createContext<
  React.Dispatch<SearchPageAction> | undefined
>(undefined);

export const SearchPageContextProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [state, dispatch] = useImmerReducer(searchPageReducer, initialState);

  // TODO this is such a shit, rework state management and drop useReducers
  const { mutate: generateSearchConfigTemplate } = useMutation(
    api.generateSearchConfigTemplate,
    {
      onSuccess: (data) => {
        dispatch({
          type: "UPDATE_ALL_SEARCH_QUERIES",
          searchQueries: data.search_queries,
        });
      },
      onError(error: Error) {
        dispatch({
          type: "SUBMIT_USER_QUERY_FAILED",
          error: error,
        });
      },
    }
  );

  const { mutate: startSearch } = useMutation(api.startSearch, {
    onSuccess: (data) => {
      const searchResultsMap: Map<string, SearchResult> = new Map(); // key is url - grouping by urls because multiple search engines may find the same page

      data.search_results.forEach((searchResult) => {
        const existingEntry = searchResultsMap.get(searchResult.url);

        if (existingEntry) {
          const newSearchEngine = parseSearchEngine(searchResult.search_engine);
          if (
            newSearchEngine !== undefined &&
            !existingEntry.searchEngines.includes(newSearchEngine)
          ) {
            existingEntry.searchEngines.push(newSearchEngine);
          }
        } else {
          searchResultsMap.set(searchResult.url, {
            enabled: true,
            url: searchResult.url,
            title: searchResult.title,
            searchEngines: [
              parseSearchEngine(searchResult.search_engine),
            ].filter((se) => se !== undefined) as SearchEngineEnum[],
            description: searchResult.description,
            details: { state: "idle" },
          });
        }
      });

      dispatch({
        type: "UPDATE_ALL_SEARCH_RESULTS",
        searchResults: Array.from(searchResultsMap.values()),
      });
    },
    onError(error: Error) {
      dispatch({
        type: "SEARCH_FAILED",
        error: error,
      });
    },
  });

  const enhancedDispatch = useCallback(
    (action: SearchPageAction) => {
      switch (action.type) {
        case "SUBMIT_USER_QUERY":
          dispatch({
            type: "SUBMIT_USER_QUERY",
            userQuery: action.userQuery,
          });
          generateSearchConfigTemplate(action.userQuery);
          break;
        case "SEARCH":
          dispatch({
            type: "SEARCH",
          });
          startSearch({
            searchQueries: state.searchConfig.searchQueries,
            searchEngineConfigs: state.searchConfig.searchEngineConfigs,
          });
          break;
        default:
          dispatch(action);
      }
    },
    [state, dispatch, generateSearchConfigTemplate, startSearch]
  );

  return (
    <SearchPageStateContext.Provider value={state}>
      <SearchPageDispatchContext.Provider value={enhancedDispatch}>
        {children}
      </SearchPageDispatchContext.Provider>
    </SearchPageStateContext.Provider>
  );
};

export const useSearchPageState = () => {
  const context = useContext(SearchPageStateContext);

  if (context === undefined) {
    throw new Error(
      "useSearchPageState must be used within a SearchPageContextProvider"
    );
  }
  return context;
};

export const useSearchPageDispatch = () => {
  const context = useContext(SearchPageDispatchContext);

  if (context === undefined) {
    throw new Error(
      "useSearchPageDispatch must be used within a SearchPageContextProvider"
    );
  }
  return context;
};
