from mangum import Mangum
from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

# local imports
from src.routes.auth_route import auth_route
from src.routes.chat_route import chat_route
from src.settings import setting, custom_swagger


# FastAPI app creation
app = FastAPI(
    title=setting.app_name,
    version=setting.app_version,
    root_path=setting.root_path,
    description=setting.app_desc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=setting.allow_origins.split(",") if setting.allow_origins else None,
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> ORJSONResponse:
    return ORJSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)

# Route inclusion
app.include_router(auth_route, prefix="/api")
app.include_router(chat_route, prefix="/api")

# Swagger UI configuration
def _custom_openapi():
    return custom_swagger(app)

app.openapi = _custom_openapi
    
# AWS Lambda handler
handler = Mangum(app)
