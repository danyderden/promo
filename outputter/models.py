import enum
import uuid

from sqlalchemy import Column, Enum, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class ReasonType(str, enum.Enum):
    bug = 'bug'
    event = 'event'
    other = 'other'


class PromoCode(Base):
    __tablename__ = 'promocode'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    status = Column(Boolean, default=True)
    promocode = Column(String, nullable=False)

    user = Column(String, nullable=True)
    issued_at = Column(DateTime(timezone=True), nullable=True)
    reason = Column(Enum(ReasonType), nullable=True)
    ticket_id = Column(String, nullable=True)
