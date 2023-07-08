from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from outputter.schemas import PromoCodeInsert, PromoCodeGiveOut
from outputter.service import _insert_promo_code_list, _promo_code_give_out

promo_code_router = APIRouter(prefix='/promocode', tags=['Promocode'])


@promo_code_router.post('',
                        status_code=status.HTTP_201_CREATED)
async def insert_promo_code_list(promo_list: PromoCodeInsert,
                                 session: AsyncSession = Depends(
                                     get_async_session)):
    await _insert_promo_code_list(promo_list, session)

    return {"status": "success"}


@promo_code_router.patch('')
async def promo_code_give_out(action_info: PromoCodeGiveOut,
                              session: AsyncSession = Depends(
                                  get_async_session)):
    promo_code_to_give_out = await _promo_code_give_out(session, action_info)
    return {'promo': promo_code_to_give_out}
