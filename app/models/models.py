from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

    # Relationships
    jobs = relationship(
        "Job",
        back_populates="owner"
    )

    applications = relationship(
        "Application",
        back_populates="user"
    )


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))

    description = Column(Text)

    skills = Column(String(500))
    salary = Column(String(100))

    job_type = Column(String(100))

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationships
    owner = relationship(
        "User",
        back_populates="jobs"
    )

    applications = relationship(
        "Application",
        back_populates="job"
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        String(50),
        default="applied",
        nullable=False
    )

    # Relationships
    job = relationship(
        "Job",
        back_populates="applications"
    )

    user = relationship(
        "User",
        back_populates="applications"
    )