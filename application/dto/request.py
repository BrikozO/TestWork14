from pydantic import BaseModel, Field


class GetQuotesQueryDTO(BaseModel):
    model_config = {'extra': 'forbid'}

    author: str = ''
    tags: list[str] = Field(default_factory=list)

    @property
    def empty(self):
        return len(self.author) == 0 and not self.tags
