from abc import ABC, abstractmethod
from datetime import datetime


class DBHandler(ABC):
    """Abstract base class for database handlers."""

    @abstractmethod
    async def fetch_raw_data(
        self,
        country: str,
        city: str,
        date_from: datetime,
        date_to: datetime,
    ) -> list[dict[str, str]]:
        """Fetch all raw documents relevant to (country, city) within an optional date range."""

        raise NotImplementedError

    @abstractmethod
    async def fetch_user_context(
        self,
        country: str,
        city: str,
        user_id: str,
    ) -> str:
        """Fetch user_context unique per (country, city, user_id)."""

        raise NotImplementedError
