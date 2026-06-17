from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database import engine, Base
from app.routers import projects, skills, problems, pages


def create_app() -> FastAPI:
    app = FastAPI(title="AI Team Hub")

    # Create tables (dev convenience; production uses Alembic)
    Base.metadata.create_all(bind=engine)

    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    app.include_router(projects.router)
    app.include_router(skills.router)
    app.include_router(problems.router)
    app.include_router(pages.router)

    from mcp_server.integration import setup_mcp
    setup_mcp(app)

    return app


app = create_app()
