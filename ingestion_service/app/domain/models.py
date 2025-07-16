# Dominio: modelo de MatchID
from pydantic import BaseModel

class MatchID(BaseModel):
    match_id: int
