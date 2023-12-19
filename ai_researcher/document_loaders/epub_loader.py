from typing import Dict, Iterator, List, Union

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from ai_researcher.utils import debug


class EPubLoader(BaseLoader):
    """
    EPubLoader is a class for loading and parsing ePub files, extracting the text
    and metadata from the eBook to create (langchain) Documents that can be processed
    further.

    Compared to UnstructuredEPubLoader from langchain's integrations, this class also preserves
    chapters, so one chapter will result in one Document.

    Attributes:
        file_path (str): The path to the ePub file.
        title (str): The title of the eBook extracted from its metadata.
        authors (List[Dict[str, Union[str, None]]]): A list of creators and contributors of the eBook.

    Example usage:
        epub_loader = EPubLoader('/path/to/ebook.epub')
        documents = epub_loader.load()
    """

    def __init__(self, file_path: str):
        """
        Initializes the EPubLoader with a given ePub.

        Args:
            file_path (str): The path to the ePub file to be loaded.

        Raises:
            FileNotFoundError: If the specified file_path does not exist or is inaccessible.
            ebooklib.epub.EpubException: If there is an error in reading or parsing the ePub file.
        """

        self.file_path = file_path
        self._book = epub.read_epub(file_path)

        self.title = self._book.title

        creators = [
            {
                "name": creator[0],
                "authorship_type": "creator",
                # TODO roles if they are present
                # "roles": []
            }
            for creator in (self._book.get_metadata("DC", "creator"))
        ]
        contributors = [
            {
                "name": contributor[0],
                "authorship_type": "contributor",
                # TODO roles if they are present
                # "roles": [],
            }
            for contributor in (self._book.get_metadata("DC", "contributor"))
        ]
        self.authors = creators + contributors

    def load(self) -> List[Document]:
        return list(self.lazy_load())

    def lazy_load(self) -> Iterator[Document]:
        for index, spine_item in enumerate(self._book.spine):
            item_id = spine_item[0]
            item = self._book.get_item_with_id(item_id)

            if item.get_type() == ebooklib.ITEM_IMAGE:
                # TODO: Describe with GPT Vision
                debug(["image", item.file_name])
            if item.get_type() == ebooklib.ITEM_AUDIO:
                # TODO Whisper
                debug(["audio", item.file_name])
            if item.get_type() == ebooklib.ITEM_VIDEO:
                # Ignore videos for now
                debug(["video", item.file_name])

            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                text = soup.get_text()

                # debug(html_to_text(item.get_body_content()))
                metadata: Dict[str, Union[str, None]] = {
                    "book_title": self.title,
                    "authors": self.authors,
                    "source": self.file_path,
                    "chapter_id": item_id,
                    "chapter_number": index + 1,
                }

                yield Document(
                    page_content=text,
                    metadata=metadata,
                )
