from pydantic import  create_model
from typing import Optional

from app.lib.constant import riesterDBColumns

dynamic_fields = {name: (Optional[str], None) for name in riesterDBColumns}
class Config:
    extra = 'forbid'

UserModel = create_model(
    'UserModel', **dynamic_fields,    __config__=Config

)
