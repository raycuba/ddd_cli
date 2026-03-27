# services/exceptions.py

"""
EXCEPCIONES DE APLICACIÓN: 
Servicio: Orquestan la comunicación y validan el flujo de entrada.
Cuándo usarlas: Para errores de formato, falta de datos o traducción de errores técnicos.
Ejemplos: InvalidServiceInput, ClientCardServiceUnavailable, MalformedIdentifierError.

nota: se pueden importar desde otra aplicación, pero no desde el dominio. 
"""

class BaseApplicationException(Exception):
    """Errores de flujo o técnicos controlados (Ej: Formato ID inválido)"""
    def __init__(self, message="Error en la operación"):
        self.message = message
        super().__init__(self.message)

class [[ entity_name|capitalize_first ]]Error(BaseApplicationException):
    """Excepción base para errores relacionados con los servicios [[ entity_name|capitalize_first ]]."""
    def __init__(self, message="Error en la operación de [[ entity_name|capitalize_first ]]"):
        self.message = message
        super().__init__(self.message)

class [[ entity_name|capitalize_first ]]ValidationError([[ entity_name|capitalize_first ]]Error):
    """Errores de validación de datos antes de guardar el modelo."""
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validation in [[ entity_name|capitalize_first ]] failed.")

class [[ entity_name|capitalize_first ]]AlreadyExistsError([[ entity_name|capitalize_first ]]Error):
    """Cuando se intenta crear una [[ entity_name|capitalize_first ]] que ya existe."""
    def __init__(self, detail: str, field: str = "value"):
        self.field = field        
        self.detail = detail
        super().__init__(f"[[ entity_name|capitalize_first ]] already exists.")

class [[ entity_name|capitalize_first ]]NotFoundError([[ entity_name|capitalize_first ]]Error):
    """Cuando se intenta acceder a una [[ entity_name|capitalize_first ]] inexistente."""
    def __init__(self, id):
        self.id = id
        super().__init__(f"[[ entity_name|capitalize_first ]] with ID {id} not found.")

class [[ entity_name|capitalize_first ]]OperationNotAllowedError([[ entity_name|capitalize_first ]]Error):
    """Cuando se intenta realizar una operación no permitida."""
    def __init__(self, operation_name: str):
        super().__init__(f"Operation '{operation_name}' not allowed in [[ entity_name|capitalize_first ]].")        

class [[ entity_name|capitalize_first ]]PermissionError([[ entity_name|capitalize_first ]]Error):
    """Cuando el usuario no tiene permisos para modificar o acceder."""
    def __init__(self):
        super().__init__("Permission not allowed in [[ entity_name|capitalize_first ]].")      
