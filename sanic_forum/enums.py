from enum import Enum, IntEnum


class ApiVersion(Enum):
    V1 = "v1"


class CategoryType(IntEnum):
    FORUM_ROOT = 1
    FORUM_DIVIDER = 2
    FORUM_CATEGORY = 3
