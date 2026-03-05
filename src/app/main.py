import os
import logging
from src.app.fastapi.server import create_fastapi_app
level = os.getenv("LOGGER_LEVEL", logging.INFO)

logging.basicConfig(
    level=int(level),
    format="%(levelname)s - %(name)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.debug("!!!!! LOGGER LEVEL SET TO DEBUG !!!!!")

app = create_fastapi_app()
    


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )