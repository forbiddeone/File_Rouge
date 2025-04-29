from fastapi import APIRouter, HTTPException
from app.database import con

router = APIRouter()

@router.get("/{movie_id}")
def read_movie(movie_id: int):
    try:
        result = con.execute("SELECT * FROM films WHERE id = ?", (movie_id,)).fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Film introuvable")

        columns = [desc[1] for desc in con.execute("PRAGMA table_info('films')").fetchall()]
        return dict(zip(columns, result))

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
