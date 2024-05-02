from fastapi import FastAPI, APIRouter;

from api.routes.fileTouching import router as fileRouter



def initialAppSetup():
    app = FastAPI()

    ## Any existing middleware setup
    v1_router = APIRouter() 

    v1_router.include_router(fileRouter)
    app.include_router(v1_router)

    return app

app = initialAppSetup()

@app.get("/")
def root_path():
    return {"Fitcheck": "API"}