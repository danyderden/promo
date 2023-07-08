import enum


from pydantic import BaseModel


class PromoCodeShowAvailable(BaseModel):
    promocode: str


class PromoCodeInsert(BaseModel):
    promo_list: list[str, str]


class ReasonType(str, enum.Enum):
    bug = 'bug'
    event = 'event'
    other = 'other'


class PromoCodeGiveOut(BaseModel):
    user: str
    reason: ReasonType
    ticket_id: str
