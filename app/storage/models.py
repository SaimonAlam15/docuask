from pydantic import BaseModel


class DocumentFileResult(BaseModel):
    storage_key: str
    checksum: str
