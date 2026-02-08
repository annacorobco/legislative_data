from pydantic import BaseModel, Field, validator


class Person(BaseModel):
    id: int = Field(gt=0, description="Legislator ID")
    name: str = Field(description="Legislator name")

    class Cols:
        id = "id"
        name = "name"


class Bill(BaseModel):
    id: int = Field(gt=0, description="Bill ID")
    title: str = Field(description="Bill title")
    sponsor_id: int = Field(gt=0, description="Primary sponsor ID")

    class Cols:
        id = "id"
        title = "title"
        sponsor_id = "sponsor_id"


class Vote(BaseModel):
    id: int = Field(gt=0, description="Vote ID")
    bill_id: int = Field(gt=0, description="Bill ID")

    class Cols:
        id = "id"
        bill_id = "bill_id"


class VoteResult(BaseModel):
    id: int = Field(gt=0, description="Vote result ID")
    legislator_id: int = Field(gt=0, description="Legislator ID")
    vote_id: int = Field(gt=0, description="Vote ID")
    vote_type: int = Field(description="1 for Yea, 2 for Nay")

    class Cols:
        id = "id"
        legislator_id = "legislator_id"
        vote_id = "vote_id"
        vote_type = "vote_type"

    @validator('vote_type')
    def validate_vote_type(cls, v):
        if v not in [1, 2]:
            raise ValueError(f"vote_type must be 1 (Yea) or 2 (Nay), got {v}")
        return v


class BillVoteSummary(BaseModel):
    """Output model for bill vote statistics."""
    id: int = Field(gt=0)
    title: str
    supporter_count: int = Field(ge=0)
    opposer_count: int = Field(ge=0)
    primary_sponsor: str

    class Cols:
        id = "id"
        title = "title"
        supporter_count = "supporter_count"
        opposer_count = "opposer_count"
        primary_sponsor = "primary_sponsor"