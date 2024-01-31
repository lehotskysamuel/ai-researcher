import React, { createContext, useCallback, useContext } from "react";
import { initialState, searchPageReducer } from "./reducer";
import { SearchPageAction, SearchPageState } from "./types";
import { useImmerReducer } from "use-immer";
import { useMutation } from "react-query";
import { generateSearchConfigTemplate } from "@/api/apis";

const SearchPageStateContext = createContext<SearchPageState | undefined>(undefined);

const SearchPageDispatchContext = createContext<React.Dispatch<SearchPageAction> | undefined>(undefined);

export const SearchPageContextProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [state, dispatch] = useImmerReducer(searchPageReducer, initialState);

  const { mutate } = useMutation(generateSearchConfigTemplate, {
    onSuccess: (data) => {
      dispatch({
        type: "UPDATE_SEARCH_QUERIES",
        searchQueries: data.search_queries,
      });
    },
    onError(error: Error) {
      dispatch({
        type: "SUBMIT_USER_QUERY_FAILED",
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
          mutate(action.userQuery);
          break;
        default:
          dispatch(action);
      }
    },
    [dispatch, mutate]
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
