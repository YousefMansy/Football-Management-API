from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from footballfantasyapi import crud
from footballfantasyapi.api import deps
from footballfantasyapi.schemas import Team, TeamUpdate, User

router = APIRouter()


# @router.post("/team", status_code=201, response_model=Team)
# def create_team(
#         *,
#         team_in: TeamCreate,
#         current_user: User = Depends(deps.get_current_user)) -> dict:
#     """
#     Create a new Team
#     """
#     team = crud.team.create(db=db, obj_in=team_in)
#     return team


@router.get("/team/{team_id}", status_code=200, response_model=Team)
def fetch_team(
        *,
        team_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> dict:
    """
    Fetch a single team by ID
    """
    result = crud.team.get(db=db, id=team_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f'Team with ID {team_id} does not exist.'
        )
    return result


@router.put("/{team_id}", status_code=201, response_model=Team)
def update_team(
        *,
        team_id: int,
        team_in: TeamUpdate,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> dict:
    """
    Update team in the database.
    """
    team = crud.team.get(db, id=team_id)
    if not team:
        raise HTTPException(
            status_code=400, detail=f"Team with ID: {team_id} not found."
        )
    if team.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only update your own teams."
        )

    updated_team = crud.team.update(db=db, db_obj=team, obj_in=team_in)
    return updated_team
