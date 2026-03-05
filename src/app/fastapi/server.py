import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.di.injector import Injector
from src.features.users import router as user_routes
from ..setup.di import setup_dependencies
from ..exceptions import AppException


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    api_injecor = Injector()
    setup_dependencies(injector=api_injecor)
    app.state.injector = api_injecor

    yield


def create_fastapi_app():
    app = FastAPI(lifespan=lifespan)

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppException)
    async def app_error_handler(request, exc: AppException):
        print(str(exc))
        return JSONResponse(
            status_code=int(exc.status_code),
            content={"detaile": str(exc.detail)}
        )
    


    @app.exception_handler(Exception)
    async def server_error_handler(request, exc: Exception):
        print(str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to process request at this time"}
        )
    
    


    @app.get("/", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "Renters ok"}
    

    app.include_router(user_routes.router)

    return app
    
    