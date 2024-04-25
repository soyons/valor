from typing import List, Iterator

from valor.document import Document
from valor.knowledge.base import AssistantKnowledge


class DocumentKnowledgeBase(AssistantKnowledge):
    documents: List[Document]

    @property
    def document_lists(self) -> Iterator[List[Document]]:
        """Iterate over documents and yield lists of documents.
        Each object yielded by the iterator is a list of documents.

        Returns:
            Iterator[List[Document]]: Iterator yielding list of documents
        """

        for _document in self.documents:
            yield [_document]
