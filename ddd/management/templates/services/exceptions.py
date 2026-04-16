# services/exceptions.py

"""
EXCEPCIONES DE APLICACIÓN: 
Servicio: Orquestan la comunicación y validan el flujo de entrada.
"""

class BaseApplicationException(Exception):
    """Errores de flujo o técnicos controlados."""
    def __init__(self, *args, **kwargs):
        # Si no se pasan argumentos, usamos un mensaje por defecto
        if not args:
            args = ("Error en la operación",)
        super().__init__(*args)
        self.kwargs = kwargs

class [[ entity_name|capitalize_first ]]Error(BaseApplicationException):
    """Excepción base para errores relacionados con los servicios [[ entity_name|capitalize_first ]]."""
    def __init__(self, *args, **kwargs):
        if not args:
            args = ("Error en la operación de [[ entity_name|capitalize_first ]]",)
        super().__init__(*args, **kwargs)

class [[ entity_name|capitalize_first ]]ValidationError([[ entity_name|capitalize_first ]]Error):
    """Errores de validación de datos antes de guardar el modelo."""
    def __init__(self, errors=None, *args, **kwargs):
        self.errors = errors
        msg = args[0] if args else f"Validation in [[ entity_name|capitalize_first ]] failed."
        super().__init__(msg, **kwargs)

class [[ entity_name|capitalize_first ]]AlreadyExistsError([[ entity_name|capitalize_first ]]Error):
    """Cuando se intenta crear una [[ entity_name|capitalize_first ]] que ya existe."""
    def __init__(self, detail=None, field="value", *args, **kwargs):
        self.field = field        
        self.detail = detail
        msg = args[0] if args else f"[[ entity_name|capitalize_first ]] already exists."
        super().__init__(msg, **kwargs)

class [[ entity_name|capitalize_first ]]NotFoundError([[ entity_name|capitalize_first ]]Error):
    """Cuando se intenta acceder a una [[ entity_name|capitalize_first ]] inexistente."""
    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        msg = args[0] if args else f"[[ entity_name|capitalize_first ]] with ID {id} not found."
        super().__init__(msg, **kwargs)

class [[ entity_name|capitalize_first ]]OperationNotAllowedError([[ entity_name|capitalize_first ]]Error):
    """Cuando se intenta realizar una operación no permitida."""
    def __init__(self, operation_name=None, *args, **kwargs):
        self.operation_name = operation_name
        msg = args[0] if args else f"Operation '{operation_name}' not allowed in [[ entity_name|capitalize_first ]]."
        super().__init__(msg, **kwargs)

class [[ entity_name|capitalize_first ]]PermissionError([[ entity_name|capitalize_first ]]Error):
    """Cuando el usuario no tiene permisos para modificar o acceder."""
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else "Permission not allowed in [[ entity_name|capitalize_first ]]."
        super().__init__(msg, **kwargs)