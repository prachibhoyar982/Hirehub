from fastapi import FastAPI

app = FastAPI(
    title="HireHub API",
    description="Job Recruitment Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "HireHub API is running"}