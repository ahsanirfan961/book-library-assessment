import httpx
import os
from backend.infra.google_books.schemas import Volume
from backend.infra.open_library.schemas import SubjectWorks, Work
from dotenv import load_dotenv

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

async def get_gb_http_client():
    async with httpx.AsyncClient() as client:
        try:
            yield client
        finally:
            await client.aclose()

class GoogleBooksClient:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.http_client = http_client
        self.base_url = "https://www.googleapis.com/books/v1"
        self.api_key = GOOGLE_BOOKS_API_KEY

    def get_authorized_url(self, url: str) -> str:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}key={self.api_key}"

    async def search_by_isbn(self, isbn: str) -> Volume:
        url = f"{self.base_url}/volumes?q=isbn:{isbn}"
        response = await self.http_client.get(self.get_authorized_url(url))
        response.raise_for_status()

        res = response.json()
        if res["totalItems"] == 0:
            raise ValueError(f"No books found for ISBN: {isbn}")

        return Volume.model_validate(res["items"][0])

    
