"""Pagination utilities."""
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""

    skip: int = 0
    limit: int = 100

    def validate(self):
        """Validate pagination parameters."""
        if self.skip < 0:
            self.skip = 0
        if self.limit < 1:
            self.limit = 1
        if self.limit > 1000:
            self.limit = 1000


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: List[T]
    total: int
    skip: int
    limit: int

    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        return (self.total + self.limit - 1) // self.limit

    @property
    def current_page(self) -> int:
        """Calculate current page."""
        return (self.skip // self.limit) + 1

    @property
    def has_next(self) -> bool:
        """Check if there are more pages."""
        return (self.skip + self.limit) < self.total

    @property
    def has_prev(self) -> bool:
        """Check if there are previous pages."""
        return self.skip > 0


def get_pagination_params(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
) -> PaginationParams:
    """
    Get and validate pagination parameters.

    Args:
        skip: Number of items to skip
        limit: Max items to return

    Returns:
        Validated pagination parameters
    """
    params = PaginationParams(
        skip=skip or 0,
        limit=limit or 100,
    )
    params.validate()
    return params
