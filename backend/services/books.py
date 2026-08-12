

from backend.infra.open_library.client import OpenLibraryClient


class BooksService:
    def __init__(self, open_library_client: OpenLibraryClient) -> None:
        self.open_library_client = open_library_client

    async def get_books(self, subject)