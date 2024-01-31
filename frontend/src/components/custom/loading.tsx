import { Spinner } from "./spinner";

export function Loading(props: { text: string }) {
  return (
    <div className="flex justify-center items-center gap-4 my-4">
      <Spinner />
      <p>{props.text}</p>
    </div>
  );
}
