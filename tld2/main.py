import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from tld2.modules.approver.handler import approver_router
from tld2.modules.auth.login_handler import login_router
from tld2.modules.company.handler import company_router
from tld2.modules.library.handler import library_router
from tld2.modules.user.handler import user_router


app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user', tags=['user'])
main_api_router.include_router(login_router, prefix='/login', tags=['login'])
main_api_router.include_router(approver_router, prefix='/approver', tags=['approver'])
main_api_router.include_router(company_router, prefix='/company', tags=['company'])
main_api_router.include_router(library_router, prefix='/library', tags=['library'])


app.include_router(main_api_router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
