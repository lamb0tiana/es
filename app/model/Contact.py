from pydantic import  create_model
from typing import Optional

from app.lib.constant import riesterDBColumns

dynamic_fields = {name: (Optional[str], None) for name in riesterDBColumns}

UserModel = create_model(
    'UserModel', **dynamic_fields
)

fields = [
    {'name': 'username', 'type': str, 'required': True},
    {'name': 'email', 'type': str, 'required': True},
    {'name': 'age', 'type': Optional[int], 'required': False},
]


