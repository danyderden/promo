from httpx import AsyncClient


async def test_insert_promo_code_list_handler_success(
        async_client: AsyncClient):
    response = await async_client.post(url='promocode', json={'promo_list': [
        'promo1',
        'promo2',
        'promo3']
    })
    assert response.status_code == 201
    assert response.json()['status'] == 'success'
    assert response.json()['data']['promo_list'] == ['promo1', 'promo2', 'promo3']
    assert response.json()['detail'] == 'Promo codes have been added'


async def test_promo_code_give_out_handler(async_client: AsyncClient):
    await async_client.post(url='promocode', json={'promo_list': [
        'promo1',
        'promo2',
        'promo3']
    })
    response = await async_client.patch('promocode', json={
        'user': 'some_user',
        'reason': 'bug',
        'ticket_id': 'some_ticket_id'
    })
    print(response.json())
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert response.json()['data'] == 'promo1'
    assert response.json()['detail'] is None


async def test_promo_code_give_out_no_promo_handler(async_client: AsyncClient):
    response = await async_client.patch('promocode', json={
        'user': 'some_user',
        'reason': 'bug',
        'ticket_id': 'some_ticket_id'

    })
    assert response.json()['status_code'] == 404
    assert response.json()['detail']['status'] == 'No more'
    assert response.json()['detail']['data'] == 'No more promo in database'
