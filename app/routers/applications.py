from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Application, Job, User
from app.auth import get_current_user

from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# =========================
# FORMAT APPLICATION RESPONSE
# =========================
def format_application(application):
    return {
        "id": application.id,
        "job_id": application.job_id,
        "user_id": application.user_id,
        "status": application.status,
        "job_title": application.job.title if application.job else None,
        "candidate_name": application.user.name if application.user else None,
        "candidate_email": application.user.email if application.user else None
    }


# =========================
# APPLY FOR JOB
# =========================
@router.post("/", response_model=ApplicationResponse)
def apply_for_job(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["candidate", "student"]:
        raise HTTPException(
            status_code=403,
            detail="Only candidates and students can apply for jobs"
        )

    job = db.query(Job).filter(
        Job.id == application.job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_application = db.query(Application).filter(
        Application.job_id == application.job_id,
        Application.user_id == current_user.id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You have already applied for this job"
        )

    new_application = Application(
        job_id=application.job_id,
        user_id=current_user.id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return format_application(new_application)


# =========================
# GET MY APPLICATIONS
# =========================
@router.get(
    "/my",
    response_model=list[ApplicationResponse]
)
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    return [
        format_application(application)
        for application in applications
    ]


# =========================
# GET APPLICATIONS FOR JOB
# =========================
@router.get(
    "/job/{job_id}",
    response_model=list[ApplicationResponse]
)
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only recruiters can view applications
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Only recruiters can view job applications"
        )

    # Find the job
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Check whether recruiter owns the job
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only view applications for your own jobs"
        )

    # Get applications
    applications = db.query(Application).filter(
        Application.job_id == job_id
    ).all()

    return [
        format_application(application)
        for application in applications
    ]


# =========================
# UPDATE APPLICATION STATUS
# =========================
@router.put(
    "/{application_id}/status",
    response_model=ApplicationResponse
)
def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only recruiters can update status
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Only recruiters can update application status"
        )

    # Find application
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    # Find related job
    job = db.query(Job).filter(
        Job.id == application.job_id
    ).first()

    # Check job ownership
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update applications for your own jobs"
        )

    # Allowed statuses
    allowed_statuses = [
        "applied",
        "shortlisted",
        "interview",
        "selected",
        "rejected"
    ]

    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid application status"
        )

    # Update status
    application.status = status_update.status

    db.commit()
    db.refresh(application)

    return format_application(application)