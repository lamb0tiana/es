from pydantic import BaseModel, validator, ValidationError
from typing import Any, Dict, Type, Optional


def create_advanced_model(name: str, fields: Dict[str, Any], validators: Dict[str, classmethod] = None) -> Type[
    BaseModel]:
    # Création d'un namespace pour les champs et les validateurs
    namespace = {
        '__annotations__': {field_name: field_type for field_name, (field_type, _) in fields.items()}
    }

    # Ajout des champs avec leurs valeurs par défaut ou des champs obligatoires
    for field_name, (_, default_value) in fields.items():
        namespace[field_name] = default_value

    if validators:
        # Ajouter les validateurs sous forme de méthodes dans le namespace
        for field_name, validator_func in validators.items():
            namespace[f'validate_{field_name}'] = validator(field_name, allow_reuse=True)(validator_func)

    # Créer une nouvelle classe BaseModel dynamiquement
    return type(name, (BaseModel,), namespace)


# Validator personnalisé pour l'âge
def validate_age(cls, v):
    if v < 18:
        raise ValueError('Age must be at least 18')
    return v


# Création du modèle dynamique avec le validateur
DynamicUserModel = create_advanced_model(
    'DynamicUser',
    {'name': (str, ...), 'age': (int, ...)},
    {'age': validate_age}
)

fields = [
    {'name': 'username', 'type': str, 'required': True},
    {'name': 'email', 'type': str, 'required': True},
    {'name': 'age', 'type': Optional[int], 'required': False},
]


