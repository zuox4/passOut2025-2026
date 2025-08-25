from pydantic import BaseModel


class AddPermission(BaseModel):
    groupName: str
    permission_teacher: str
