
from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    salary: str | None = None
    job_type: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    salary: str | None = None
    job_type: str | None = None
    user_id: int

    class Config:
        from_attributes = True

