from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from database import get_async_session
from outputter.schemas import PromoCodeInsert, PromoCodeGiveOut
from outputter.service import _insert_promo_code_list, _promo_code_give_out

promo_code_router = APIRouter(prefix='/promocode', tags=['Promocode'])


@promo_code_router.post('')
async def insert_promo_code_list(promo_list: PromoCodeInsert,
                                 session: AsyncSession = Depends(
                                     get_async_session)):
    try:
        await _insert_promo_code_list(promo_list, session)
        return JSONResponse(status_code=201, content={
            'status': 'success',
            'data': jsonable_encoder(promo_list),
            'detail': 'Promo codes have been added'
        })
    except HTTPException as error:
        return {
            'status': 'Not success',
            'data': error.args,
            'detail': error.detail
        }


@promo_code_router.patch('')
async def promo_code_give_out(action_info: PromoCodeGiveOut,
                              session: AsyncSession = Depends(
                                  get_async_session)):
    try:
        promo_code_to_give_out = await _promo_code_give_out(session,
                                                            action_info)
        return JSONResponse(status_code=200, content={
            'status': 'success',
            'data': jsonable_encoder(promo_code_to_give_out),
            'detail': None
        })
    except AttributeError:
        return HTTPException(status_code=404, detail={
            'status': 'No more',
            'data': 'No more promo in database',
        })
