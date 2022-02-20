from fastapi     import APIRouter, Depends

from app.api     import users, study_rooms, my_studies, reports
from app.core    import (
                    study_rooms_settings,
                    user_settings,
                    my_studies_settings,
                    report_settings
                    )
from app.service import auth_token


api_router = APIRouter()
api_router.include_router(
    users.router,
    prefix=user_settings.API_USER,
    tags=['users']
)
api_router.include_router(
    router       = study_rooms.router,
    prefix       = study_rooms_settings.API_STUDY_ROOM,
    # dependencies = [ Depends(auth_token) ],
    tags         = [ 'study_rooms' ]
)
api_router.include_router(
    router       = my_studies.router,
    prefix       = my_studies_settings.API_MY_STUDY,
    # dependencies = [ Depends(auth_token) ],
    tags         = [ 'my_studies' ]
)
api_router.include_router(
    router       = reports.router,
    prefix       = report_settings.API_REPORT,
    # dependencies = [ Depends(auth_token) ],
    tags         = [ 'reports' ]
)
