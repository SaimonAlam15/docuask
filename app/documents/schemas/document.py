from uuid import UUID

from fastapi import Form
from pydantic import BaseModel

from .document_file import FileUploadResult


class DocumentCreate(BaseModel):
    title: str
    user_id: UUID

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        user_id: str = Form(...),
    ) -> "DocumentCreate":
        return cls(title=title, user_id=user_id)


class DocumentResponse(BaseModel):
    id: str
    title: str
    document_file: FileUploadResult
