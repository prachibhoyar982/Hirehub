from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Job, User
from app.schemas.jobs import JobCreate, JobResponse
from app.auth import get_current_user


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# =========================
# CREATE JOB
# =========================

@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only recruiters and admins can create jobs"
        )

    new_job = Job(
        **job.model_dump(),
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# =========================
# GET ALL JOBS
# =========================

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()

    return jobs


# =========================
# GET SINGLE JOB
# =========================

@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# =========================
# UPDATE JOB
# =========================

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only recruiters and admins can update jobs"
        )

    existing_job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not existing_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Ownership check
    if existing_job.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only update your own jobs"
        )

    for key, value in job.model_dump().items():
        setattr(existing_job, key, value)

    db.commit()
    db.refresh(existing_job)

    return existing_job


# =========================
# DELETE JOB
# =========================

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only recruiters and admins can delete jobs"
        )

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Ownership check
    if job.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own jobs"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }


# =========================
# SEARCH JOBS
# =========================
# =========================
# SEARCH JOBS
# =========================

@router.get("/search/")
def search_jobs(
    keyword: str | None = None,
    location: str | None = None,
    job_type: str | None = None,
    skills: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort: str = "latest",
    db: Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than or equal to 1"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    if sort not in ["latest", "oldest"]:
        raise HTTPException(
            status_code=400,
            detail="Sort must be either 'latest' or 'oldest'"
        )

    query = db.query(Job)

    # Keyword search
    if keyword:
        query = query.filter(
            (Job.title.ilike(f"%{keyword}%")) |
            (Job.company.ilike(f"%{keyword}%")) |
            (Job.location.ilike(f"%{keyword}%")) |
            (Job.job_type.ilike(f"%{keyword}%")) |
            (Job.skills.ilike(f"%{keyword}%"))
        )

    # Location filter
    if location:
        query = query.filter(
            Job.location.ilike(f"%{location}%")
        )

    # Job type filter
    if job_type:
        query = query.filter(
            Job.job_type.ilike(f"%{job_type}%")
        )

    # Skills filter
    if skills:
        query = query.filter(
            Job.skills.ilike(f"%{skills}%")
        )

    # Total matching jobs
    total = query.count()

    # Sorting
    if sort == "latest":
        query = query.order_by(Job.id.desc())
    else:
        query = query.order_by(Job.id.asc())

    # Pagination
    offset = (page - 1) * limit

    jobs = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "jobs": jobs
    }