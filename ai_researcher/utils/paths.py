import os

prompts: str = "prompt_templates/summarizers"
data_root = "data"
# TODO Sam - premenovat folder na splits-raw
splits_raw: str = os.path.join(data_root, "chapters-raw")
summary: str = os.path.join(data_root, "summary")
