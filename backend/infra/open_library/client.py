import httpx

from backend.infra.open_library.schemas import SubjectWorks, Work

class OpenLibraryClient:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.http_client = http_client
        self.base_url = "https://openlibrary.org"

    async def get_subject_works(self, subject: str) -> SubjectWorks:
        url = f"{self.base_url}/subjects/{subject}.json"
        response = await self.http_client.get(url)
        response.raise_for_status()
        return SubjectWorks.model_validate_json(response.json())
    
    async def search_books(self, query: str) -> list[Work]:
        url = f"{self.base_url}/search/books.json"
        response = await self.http_client.get(url, params={"q": query})
        response.raise_for_status()
        return [Work.model_validate_json(work) for work in response.json()["docs"]]
    
    async def get_book(self, book_id: str) -> Work:
        url = f"{self.base_url}/books/{book_id}.json"
        response = await self.http_client.get(url)
        response.raise_for_status()
        return Work.model_validate_json(response.json())