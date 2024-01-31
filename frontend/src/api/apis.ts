import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
});

export interface SearchConfigTemplate {
  search_queries: string[];
}

export const generateSearchConfigTemplate = async (
  userQuery: string
): Promise<SearchConfigTemplate> => {
  const { data } = await apiClient.post("/api/search-wizard/step1", {
    user_query: userQuery,
  });
  return data;
};
