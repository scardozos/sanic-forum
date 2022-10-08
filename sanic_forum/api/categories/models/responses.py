from typing import List, TypedDict

from sanic_forum.database.models.category.types import CategoryV1

class ListRootCategoriesResponseV1(TypedDict):
    categories: List[CategoryV1]

class ListChildrenCategoriesResponseV1(TypedDict):
    categories: List[CategoryV1]

class CreateCategoryResponseV1(TypedDict):
    category: CategoryV1
