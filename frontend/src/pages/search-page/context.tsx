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

  const enhancedDispatch = useCallback(
    (action: SearchPageAction) => {
      switch (action.type) {
        case "SUBMIT_USER_QUERY":
          dispatch({
            type: "SUBMIT_USER_QUERY",
            userQuery: action.userQuery,
          });
          api
            .generateSearchConfigTemplate(action.userQuery)
            .then((data) => {
              dispatch({
                type: "UPDATE_ALL_SEARCH_QUERIES",
                searchQueries: data.search_queries,
              });
            })
            .catch((error: Error) => {
              dispatch({
                type: "SUBMIT_USER_QUERY_FAILED",
                error: error,
              });
            });
          break;
        case "SEARCH":
          dispatch({
            type: "SEARCH",
          });
          api
            .startSearch({
              searchQueries: state.searchConfig.searchQueries,
              searchEngineConfigs: state.searchConfig.searchEngineConfigs,
            })
            .then((data) => {
              const searchResultsMap: Map<string, SearchResult> = new Map(); // key is url - grouping by urls because multiple search engines may find the same page

              data.search_results.forEach((searchResult) => {
                const existingEntry = searchResultsMap.get(searchResult.url);

                if (existingEntry) {
                  const newSearchEngine = parseSearchEngine(
                    searchResult.search_engine
                  );
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
            })
            .catch((error: Error) => {
              dispatch({
                type: "SEARCH_FAILED",
                error: error,
              });
            });
          break;
        case "DOWNLOAD_CONTENT":
          state.searchResults
            .filter(
              (sr) =>
                sr.enabled &&
                sr.details.state !== "success" &&
                sr.details.state !== "loading"
            )
            .forEach((sr, index) => {
              api
                .downloadContent(sr.url)
                .then((data) => {
                  dispatch({
                    type: "UPDATE_SEARCH_RESULT_DETAILS",
                    searchResultIndex: index,
                    searchResultDetails: data.success
                      ? {
                          state: "success",
                          content: data.content ?? "",
                        }
                      : {
                          state: "error",
                          error: data.error ?? "",
                        },
                  });
                })
                .catch((error: Error) => {
                  dispatch({
                    type: "UPDATE_SEARCH_RESULT_DETAILS",
                    searchResultIndex: index,
                    searchResultDetails: {
                      state: "error",
                      error: error.message,
                    },
                  });
                });
            });
          dispatch({
            type: "DOWNLOAD_CONTENT",
          });
          break;
        default:
          dispatch(action);
      }
    },
    [state, dispatch]
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
