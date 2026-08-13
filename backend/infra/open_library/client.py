import httpx

from backend.infra.open_library.schemas import SubjectWorks, Work
from backend.schemas.common import Paginated


async def get_ol_http_client():
    async with httpx.AsyncClient() as client:
        try:
            yield client
        finally:
            await client.aclose()

class OpenLibraryClient:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.http_client = http_client
        self.base_url = "https://openlibrary.org"

    async def get_subject_works(self, subject: str, limit: int = 10, offset: int = 0) -> SubjectWorks:
        url = f"{self.base_url}/subjects/{subject}.json?limit={limit}&offset={offset}"
        response = await self.http_client.get(url)
        response.raise_for_status()
        res = response.json()
        return SubjectWorks(
            key=res["key"],
            name=res["name"],
            subject_type=res["subject_type"],
            work_count=res["work_count"],
            works=Paginated(
                limit=limit,
                offset=offset,
                total=res["work_count"],
                items=[Work.model_validate(work) for work in res["works"]]
        ))
    
    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Work]:
        url = f"{self.base_url}/search.json"
        response = await self.http_client.get(url, params={"q": query, "limit": limit, "offset": offset})
        response.raise_for_status()
        res = response.json()
        return Paginated(
            limit=limit,
            offset=offset,
            total=res["num_found"],
            items=[Work.model_validate(work) for work in res["docs"]]
        )
    
    async def get_work(self, book_id: str) -> Work:
        url = f"{self.base_url}/works/{book_id}.json"
        response = await self.http_client.get(url)
        response.raise_for_status()
        return Work.model_validate(response.json())
    
    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Work]:
        url = f"{self.base_url}/trending/weekly.json"
        response = await self.http_client.get(url, params={"limit": limit, "offset": offset})
        response.raise_for_status()
        works = response.json().get("works", [])
        return Paginated(
            limit=limit,
            offset=offset,
            total=len(works),
            items=[Work.model_validate(work) for work in works],
        )