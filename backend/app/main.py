from fastapi import FastAPI
from app.routes import movies, recommender, statistics

app = FastAPI()

# Inclusion des différents routers
app.include_router(movies.router, prefix="/movie", tags=["Movies"])
app.include_router(recommender.router, prefix="/recommend_movies", tags=["Recommender"])
app.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])
