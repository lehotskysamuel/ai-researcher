import ClickableText from "@/components/custom/clickable-text";
import { Loading } from "@/components/custom/loading";
import { SliderBox } from "@/components/custom/slider-box";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { TypographyH2, TypographyH3 } from "@/components/ui/typography";
import { useCancelAction } from "@/lib/hooks";
import { createSequenceArray } from "@/lib/utils";
import { Pencil, Plus, Search, Trash } from "lucide-react";
import { useId, useState } from "react";
import { useSearchPageDispatch, useSearchPageState } from "./context";
import { SEARCH_ENGINES, SearchEngineConfig } from "./types";

const MIN_RESULTS = 1;
const MAX_RESULTS = 20;

export function Step2Ui() {
  const state = useSearchPageState();
  const dispatch = useSearchPageDispatch();

  const [groupedSliderResults, setGroupedSliderResults] = useState(3);

  return (
    <>
      <TypographyH2>Configure Search Parameters</TypographyH2>
      <TypographyH3>Configure Search Queries</TypographyH3>
      <div className="flex flex-col gap-2 list-disc">
        {state.searchConfig.searchQueries.map((sq, index) => (
          <SearchQuery
            key={`${index}${sq}`}
            defaultEditMode={sq === ""}
            defaultSearchQuery={sq}
            onDelete={() => {
              return dispatch({
                type: "DELETE_SEARCH_QUERY",
                index,
              });
            }}
            onChange={(newValue) => {
              dispatch({
                type: "UPDATE_SEARCH_QUERY",
                index,
                searchQuery: newValue,
              });
            }}
          />
        ))}

        <Button
          className="self-start py-2 px-4 my-4"
          size="sm"
          onClick={() => {
            dispatch({
              type: "CREATE_SEARCH_QUERY",
            });
          }}
        >
          <Plus size={16} className="mr-2" /> Add
        </Button>
      </div>

      <TypographyH3>Select Search Engines</TypographyH3>
      <div className="flex flex-col gap-2">
        {state.searchConfig.searchEngineConfigs.map(
          (sec: SearchEngineConfig, index) => {
            const onChange = (newValue: SearchEngineConfig) => {
              dispatch({
                type: "UPDATE_SEARCH_ENGINE_CONFIG",
                index,
                searchEngineConfig: newValue,
              });
            };

            const selectOne = () => {
              dispatch({
                type: "SELECT_SEARCH_ENGINE_CONFIGS",
                indexes: [index],
              });
            };
            return (
              <SearchEngine
                key={index}
                config={sec}
                onChange={onChange}
                selectOne={selectOne}
              />
            );
          }
        )}
      </div>

      <div className="flex items-center gap-2">
        <Button
          size="sm"
          variant="outline"
          onClick={() => {
            dispatch({
              type: "SELECT_SEARCH_ENGINE_CONFIGS",
              indexes: createSequenceArray(
                state.searchConfig.searchEngineConfigs.length
              ),
            });
          }}
        >
          Select All
        </Button>

        <SliderBox
          min={MIN_RESULTS}
          max={MAX_RESULTS}
          value={groupedSliderResults}
          onChange={(newValue) => {
            setGroupedSliderResults(newValue);
            dispatch({
              type: "UPDATE_SEARCH_ENGINE_CONFIGS",
              maxResults: newValue,
            });
          }}
        />
      </div>

      <Button className="my-4">
        <Search size={16} className="mr-2" />
        Search
      </Button>
      <Loading text="Searching..." />
    </>
  );
}

function SearchQuery(props: {
  defaultEditMode: boolean;
  defaultSearchQuery: string;
  onDelete: () => void;
  onChange: (newValue: string) => void;
}) {
  const { defaultSearchQuery, onDelete } = props;

  const [editMode, setEditMode] = useState<boolean>(props.defaultEditMode);
  const [searchQuery, setSearchQuery] = useState<string>(
    props.defaultSearchQuery
  );
  const [showDeleteConfirmation, setShowDeleteConfirmation] =
    useState<boolean>(false);

  const onSave = () => {
    setEditMode(false);
    props.onChange(searchQuery);
  };

  const onCancel = () => {
    setEditMode(false);
    setShowDeleteConfirmation(false);

    if (defaultSearchQuery === "") {
      onDelete();
    }
    setSearchQuery(defaultSearchQuery);
  };
  const ref = useCancelAction<HTMLDivElement>(onCancel);

  return (
    <div className="flex items-center text-sm" ref={ref}>
      {!editMode && (
        <>
          <span className="flex-1">{searchQuery}</span>
          <Button
            size="icon"
            variant="outline"
            onClick={() => setEditMode(true)}
            className="mr-2"
          >
            <Pencil className="h-4 w-4" />
          </Button>
          {!showDeleteConfirmation ? (
            <Button
              size="icon"
              variant="outline"
              onClick={() => setShowDeleteConfirmation(true)}
            >
              <Trash className="h-4 w-4" />
            </Button>
          ) : (
            <Button
              className="w-20"
              size="sm"
              variant="destructive"
              onClick={() => {
                setShowDeleteConfirmation(false);
                props.onDelete();
              }}
            >
              Sure?
            </Button>
          )}
        </>
      )}
      {editMode && (
        <>
          <Input
            className="flex-1 p-2 border rounded-md border-gray-200 dark:border-gray-800 mr-2"
            placeholder="Search query"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            autoFocus
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                onSave();
              }
            }}
          />
          <Button size="sm" variant="outline" onClick={onSave}>
            Save
          </Button>
        </>
      )}
    </div>
  );
}

function SearchEngine(props: {
  config: SearchEngineConfig;
  onChange: (newValue: SearchEngineConfig) => void;
  selectOne: () => void;
}) {
  const id = useId();

  return (
    <div className="flex items-center gap-4">
      <Checkbox
        id={id}
        checked={props.config.enabled}
        onCheckedChange={(newValue) =>
          props.onChange({ ...props.config, enabled: newValue === true })
        }
      />
      <ClickableText
        className="underline text-sm text-gray-400"
        onClick={props.selectOne}
      >
        (only)
      </ClickableText>
      <Label className="flex-1 flex items-center gap-2 " htmlFor={id}>
        <img
          className="w-6 h-6"
          src={SEARCH_ENGINES[props.config.searchEngine]?.logo}
          alt={SEARCH_ENGINES[props.config.searchEngine]?.displayName}
        />
        {SEARCH_ENGINES[props.config.searchEngine]?.displayName}
      </Label>

      <SliderBox
        min={MIN_RESULTS}
        max={MAX_RESULTS}
        value={props.config.maxResults}
        onChange={(newValue) =>
          props.onChange({ ...props.config, maxResults: newValue })
        }
      />
    </div>
  );
}
