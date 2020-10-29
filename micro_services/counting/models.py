from sqlalchemy import Column, DECIMAL, ForeignKey, String
from sqlalchemy.dialects.mysql import DATETIME, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BookTop3(Base):
    __tablename__ = 'book_top3'

    id = Column(INTEGER(11), primary_key=True)
    book_count = Column(INTEGER(11), nullable=False)
    count_time = Column(String(20, 'utf8_unicode_ci'), nullable=False, index=True)
    book_id = Column(INTEGER(11), nullable=False, index=True)


class PayOrderDetail(Base):
    __tablename__ = 'pay_order_detail'

    id = Column(INTEGER(11), primary_key=True)
    quantity = Column(INTEGER(11), nullable=False)
    price = Column(DECIMAL(10, 3), nullable=False)
    create_date = Column(DATETIME(fsp=6), nullable=False)
    book_id = Column(ForeignKey('book.id'), nullable=False, index=True)
    pay_order_id = Column(ForeignKey('pay_order.id'), nullable=False, index=True)
