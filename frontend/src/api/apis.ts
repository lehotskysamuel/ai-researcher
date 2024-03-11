import { SearchEngineEnum } from "@/pages/search-page/types";
import axios from "axios";
import { Immutable } from "immer";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
});

export interface Step1Output {
  search_queries: string[];
}

export interface Step2Output {
  search_results: Array<{
    search_engine: string;
    url: string;
    title: string;
    description: string;
  }>;
}

export interface Step3Output {
  success: boolean;
  content: string | undefined;
  error: string | undefined;
}

export const generateSearchConfigTemplate = async (
  userQuery: string
): Promise<Step1Output> => {
  const { data } = await apiClient.post("/api/search-wizard/step1", {
    user_query: userQuery,
  });
  return data;
};

export const startSearch = async (
  props: Immutable<{
    searchQueries: string[];
    searchEngineConfigs: Array<{
      searchEngine: SearchEngineEnum;
      maxResults: number;
    }>;
  }>
): Promise<Step2Output> => {
  const { data } = await apiClient.post("/api/search-wizard/step2", {
    search_queries: props.searchQueries,
    search_engine_configs: props.searchEngineConfigs.map((sec) => ({
      search_engine: sec.searchEngine,
      max_results: sec.maxResults,
    })),
  });
  return data;
};

export const downloadContent = async (url: string): Promise<Step3Output> => {
  const { data } = await apiClient.post("/api/search-wizard/step3", {
    url,
  });
  return data;
};
