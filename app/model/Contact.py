from pydantic import create_model
from typing import Optional

from app.lib.constant import riesterDBColumns

dynamic_fields = {name: (Optional[str], None) for name in riesterDBColumns}


class Config:
    extra = 'forbid'


ContactModel = create_model(
    'ContactModel', **dynamic_fields, __config__=Config

)
