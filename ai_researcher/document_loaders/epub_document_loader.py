from typing import Dict, Iterator, List, Union

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from ai_researcher.utils import debug


class EPubDocumentLoader(BaseLoader):
    def __init__(self, file_path: str):
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
                # TODO Sam -vyskusat rozdiel obidvoch, ale mozno chcem cele html kvoli BSoup
                soup = BeautifulSoup(item.get_content(), "html.parser")
                # soup = BeautifulSoup(item.get_body_content(), "html.parser")
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
