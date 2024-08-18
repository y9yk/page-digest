from enum import Enum


class BaseEnum(str, Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return [c.value for c in cls]


class APP_ENV(BaseEnum):
    LOCAL = "local"
    STAGE = "stage"
    PRODUCTION = "prod"


class APIVersion(BaseEnum):
    V1 = "v1"
    V2 = "v2"


class QueryType(BaseEnum):
    JSON = "json"
    GRAPHQL = "graphql"
