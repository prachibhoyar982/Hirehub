from pydantic import BaseModel
from typing import Literal

class ApplicationStatusUpdate(BaseModel):
    status: Literal[
        "applied",
        "shortlisted",
        "interview",
        "selected",
        "rejected"
    ]

class ApplicationCreate(BaseModel):
    job_id: int


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    status: str

    job_title: str | None = None
    candidate_name: str | None = None
    candidate_email: str | None = None

    class Config:
        from_attributes = True