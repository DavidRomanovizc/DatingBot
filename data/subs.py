from dataclasses import dataclass


@dataclass
class Item:
    id: int
    title: str
    description: str
    price: int
    photo_link: str


Sub_lvl_1 = Item(
    id=1,
    title="Поддержка нашего проекта",
    description="""
    Поддержка проекта
    """,
    price=1_990_00,
    photo_link="https://sun9-50.userapi.com/impg/t9W9XA1VCMhgq9hxDDI5kpNT9Rma1LUlfuOl2Q/P6J1lsYChTc.jpg?size=2118x1089&quality=96&sign=fbbd37bc2a2e7731e72d16845fdea93f&type=album"
)

Test_payment = Item(
    id=1,
    title="Поддержка нашего проекта",
    description="""
    Поддержка проекта
    """,
    price=1,
    photo_link="https://sun9-50.userapi.com/impg/t9W9XA1VCMhgq9hxDDI5kpNT9Rma1LUlfuOl2Q/P6J1lsYChTc.jpg?size=2118x1089&quality=96&sign=fbbd37bc2a2e7731e72d16845fdea93f&type=album"
)

items = [Sub_lvl_1, Test_payment]