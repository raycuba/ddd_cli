# domain/exceptions.py

from .[[ entity_name.lower() ]]_schemas import BaseDomainValueError

class [[ entity_name|capitalize_first ]]ValueError(BaseDomainValueError):
    """Error de valor en atributos de la entidad [[ entity_name|capitalize_first ]]."""
    def __init__(self, detail: str, field: str = "value"):
        self.field = field
        self.detail = detail
        if field == "value":
            super().__init__(f"Value error: {detail}.")
        else:
            super().__init__(f"Field error in '{field}': {detail}.")