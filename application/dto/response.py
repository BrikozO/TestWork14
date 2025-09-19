from pydantic import BaseModel, Field, computed_field

from application.dto.request import GetQuotesQueryDTO
from domain.models.quote import Quote


class QuotesFromDBResponseDTO(BaseModel):
    quotes: list[Quote]
    filt: GetQuotesQueryDTO = Field(alias="filter")

    @computed_field
    @property
    def is_empty(self) -> bool:
        return len(self.quotes) == 0
