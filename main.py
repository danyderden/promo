import uvicorn
from fastapi import FastAPI

from outputter.handlers import promo_code_router
app = FastAPI(title='Promo code out putter')
app.include_router(promo_code_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, workers=1, env_file='.env')
