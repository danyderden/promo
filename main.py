import uvicorn
from fastapi import FastAPI

from outputter.handlers import promo_code_router
app = FastAPI(title='Promo code out putter')
app.include_router(promo_code_router)
