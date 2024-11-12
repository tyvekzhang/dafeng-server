from src.main.pkg.common.config.config_manager import get_security_config
from src.main.pkg.server import app
from starlette.middleware.cors import CORSMiddleware

security = get_security_config()
origins = [origin.strip() for origin in security.backend_cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
