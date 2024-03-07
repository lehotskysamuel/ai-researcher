import json
import os
import pprint
import re
import string


def debug(obj):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(obj)


def sanitize_filename(filename):
    import unicodedata

    # special chars to ascii (áľťží to altzi etc)
    ascii_filename = (
        unicodedata.normalize("NFKD", filename)
        .encode("ASCII", "ignore")
        .decode()
    )
    no_colons = ascii_filename.replace(": ", " - ").replace(":", " - ")
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = "".join(c for c in no_colons if c in valid_chars)
    collapsed_whitespace = re.sub(r"\s+", " ", cleaned_filename)
    cleaned_filename = re.sub(
        r"^[._]+", "", collapsed_whitespace
    )  # avoid filenames starting with a dot
    return cleaned_filename.lower()


def sanitize_id(text):
    import unicodedata

    # special chars to ascii (áľťží to altzi etc)
    ascii_id = (
        unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode()
    )
    valid_chars = "_ %s%s" % (string.ascii_letters, string.digits)
    cleaned_id = "".join(c for c in ascii_id if c in valid_chars)
    no_whitespace = re.sub(r"\s+", "_", cleaned_id)
    return no_whitespace.lower()


def folder_empty_or_nonexistent(path):
    return (not os.path.exists(path)) or (
        os.path.isdir(path) and not os.listdir(path)
    )


def copy_file(source_path, dest_path):
    import shutil

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    shutil.copyfile(source_path, dest_path)


def dump_raw(input_str, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(input_str)


def read_raw(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def dump_json(input, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        json.dump(input, file, indent=2)


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def is_blank(text):
    return text is None or text.strip() == ""


def authors_to_string(authors):
    return ", ".join(
        list(
            map(
                lambda author: f"{author['name']} ({author['authorship_type']})",
                authors,
            )
        )
    )
