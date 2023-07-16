from httpx import AsyncClient

from outputter.handlers import insert_promo_code_list, promo_code_give_out
from outputter.schemas import PromoCodeInsert, PromoCodeGiveOut
from tests.conftest import async_session_maker


async def test_insert_promo_code_list():
    async with async_session_maker() as session:
        promo_list = PromoCodeInsert(promo_list=['promo1', 'promo2'])
        response = await insert_promo_code_list(promo_list=promo_list,
                                                session=session)
        assert response['status'] == 'success'
        assert response['data'] == 'Promo codes have been added'
        assert response[
                   'detail'] == promo_list


async def test_promo_code_give_out(async_client: AsyncClient):
    async with async_session_maker() as session:
        await async_client.post(url='promocode', json={'promo_list': ['promo1']
                                                       })
        action_info = PromoCodeGiveOut(user='user', ticket_id='ticket_id',
                                       reason='bug')
        response = await promo_code_give_out(action_info=action_info,
                                             session=session)
        assert response['status'] == 'success'
        assert response['promo code'] == 'promo1'
