import axios from "axios";
import { useQuery } from "react-query";

export const getPosts = async () => {
  const { data } = await axios.get("/api/posts");
  return data;
};

export const usePosts = () => {
  return useQuery("posts", getPosts);
};
