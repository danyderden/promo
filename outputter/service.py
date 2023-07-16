import datetime
import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from outputter.models import PromoCode
from outputter.schemas import PromoCodeInsert, PromoCodeGiveOut


async def _insert_promo_code_list(promo_list: PromoCodeInsert,
                                  session: AsyncSession):
    for promo in promo_list.promo_list:
        session.add(PromoCode(id=uuid.uuid4(), promocode=promo))
    await session.commit()


async def _get_available_promo_code(session: AsyncSession):
    available_promo_code = select(PromoCode).where(PromoCode.status == True)
    result = await session.execute(available_promo_code)
    return result.scalars().first()


async def _mark_promo_code_as_give_out(session: AsyncSession,
                                       promo_code: PromoCode,
                                       action_info: PromoCodeGiveOut
                                       ):
    query = update(PromoCode).where(PromoCode.id == promo_code.id).values(
        status=False,
        reason=action_info.reason,
        user=action_info.user,
        issued_at=datetime.datetime.utcnow(),
        ticket_id=action_info.ticket_id)
    await session.execute(query)

    await session.commit()


async def _promo_code_give_out(session: AsyncSession,
                               action_info: PromoCodeGiveOut):
    promo_code: PromoCode = await _get_available_promo_code(session)
    await _mark_promo_code_as_give_out(session, promo_code, action_info)
    return promo_code.promocode
