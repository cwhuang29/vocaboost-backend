from pydantic import BaseModel


class CacheStoreConfig(BaseModel):
    url: str
    encoding: str = 'utf-8'
