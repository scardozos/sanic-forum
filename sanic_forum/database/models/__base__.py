from sanic_forum.enums import ApiVersion


class BaseModel(object):
    def serialize(self, version: ApiVersion) -> dict:
        raise NotImplementedError()
