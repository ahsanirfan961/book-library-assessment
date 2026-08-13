import httpx
from backend.infra.google_books.client import GoogleBooksClient
from backend.infra.google_books.schemas import Volume
from backend.infra.models import EnrichmentQueue


class RatingMatcher:
    async def match(self, item: EnrichmentQueue) -> Volume | None:
        raise NotImplementedError


class IsbnMatcher(RatingMatcher):
    def __init__(self, client: GoogleBooksClient):
        self.client = client

    async def match(self, item: EnrichmentQueue) -> Volume | None:
        if not item.isbn:
            return None
        try:
            return await self.client.search_by_isbn(item.isbn)
        except (ValueError, httpx.HTTPStatusError):
            return None


class TitleAuthorMatcher(RatingMatcher):
    def __init__(self, client: GoogleBooksClient):
        self.client = client

    async def match(self, item: EnrichmentQueue) -> Volume | None:
        if not item.title:
            return None
        try:
            return await self.client.search_by_title_author(item.title, item.author or "")
        except ValueError:
            return None


class CompositeRatingMatcher:
    def __init__(self, matchers: list[RatingMatcher]):
        self.matchers = matchers

    async def match(self, item: EnrichmentQueue) -> Volume | None:
        for matcher in self.matchers:
            volume = await matcher.match(item)
            if volume:
                return volume
        return None
