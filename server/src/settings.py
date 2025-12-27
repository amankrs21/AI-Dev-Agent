from __future__ import annotations

from pydantic import Field
from fastapi import FastAPI
from typing import ClassVar
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from fastapi.openapi.utils import get_openapi

load_dotenv()

class Settings(BaseSettings):

    app_version: ClassVar[str] = "3.1.0"
    app_name: ClassVar[str] = "AI Dev Agent"
    app_desc: ClassVar[str] = "An AI-powered development assistant."
    
    root_path: str = Field(default="/", alias="ROOT_PATH")
    allow_origins: str = Field(default="", alias="ALLOW_ORIGINS")

    # Auth/JWT
    jwt_secret: str | None = Field(default=None, alias="JWT_SECRET")
    jwt_expires: int = Field(default=3600, alias="JWT_EXPIRES")

    # Storage
    data_dir: str = Field(default="data", alias="DATA_DIR")

    # Mongo
    mongo_schema: str = "cluster0"
    mongo_url: str | None = Field(default=None, alias="MONGO_URL")

    # LLM
    mistral_api_key: str | None = Field(default=None, alias="MISTRAL_API_KEY")
    huggingface_key: str | None = Field(default=None, alias="HUGGINGFACE_API_KEY")


    # LangSmith (optional)
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = Field(default=None, alias="LANGSMITH_API_KEY")
    langsmith_project: str | None = Field(default=None, alias="LANGSMITH_PROJECT")
    
    
setting = Settings()


# Custome Swagger Config
def custom_swagger(app: FastAPI) -> dict:
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    base_server_url = app.root_path
    openapi_schema["servers"] = [{"url": base_server_url}]
    components = openapi_schema.get("components", {})
    components.setdefault("securitySchemes", {})["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema
