from pydantic import create_model, Field, EmailStr

from typing import Optional, Callable, Any

from app.lib.constant import riesterDBColumns


def get_field_type(name: str) -> Callable[[], Any]:
    if "email" in name:
        return (Optional[EmailStr], Field(None, description=f"{name} de contact"))
    else:
        return (Optional[str], Field(None, description=f"{name} de contact"))


dynamic_fields = {name: get_field_type(name) for name in riesterDBColumns}


class Config:
    extra = 'forbid'


ContactModel = create_model(
    'ContactModel', **dynamic_fields, __config__=Config

)
