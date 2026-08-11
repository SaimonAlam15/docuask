from fastapi import Form
from pydantic import BaseModel

from .document_file import FileUploadResult


class DocumentCreate(BaseModel):
    title: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
    ) -> "DocumentCreate":
        return cls(title=title)


class DocumentResponse(BaseModel):
    id: str
    title: str
    document_file: FileUploadResult
