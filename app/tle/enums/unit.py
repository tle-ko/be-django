from typing import NamedTuple


_Unit = NamedTuple('_Unit', [
    ('name_ko', str),
    ('name_en', str),
    ('abbr', str),
])


class Unit:
    MEGA_BYTE = _Unit(
        name_ko="메가 바이트",
        name_en="Mega Bytes",
        abbr="MB",
    )
    SECOND = _Unit(
        name_ko="초",
        name_en="Seconds",
        abbr="s",
    )
