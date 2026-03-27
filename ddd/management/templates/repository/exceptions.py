# infrastructure/exceptions.py

"""
EXCEPCIONES DE REPOSITORIO:
Servicio: Abstraen los errores técnicos de la persistencia (DB, API externa).
Cuándo usarlas: Para ocultar detalles del ORM (Django) y que la App no sepa qué DB usamos.
Ejemplos: EntityNotFound, DatabaseConnectionError, UniqueConstraintViolation.

nota: no se pueden importar desde otra aplicación.
"""

class ValidationError(Exception):
    """Excepción para errores de validación de datos."""
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validation failed.")
        
class AlreadyExistsError(Exception):
    """Excepción para cuando se intenta crear un recurso que ya existe."""
    def __init__(self, detail: str, field: str = "value"):
        self.field = field        
        self.detail = detail
        super().__init__("Resource already exists.")
        
class NotFoundError(Exception):
    """Excepción para cuando no se encuentra un recurso."""
    def __init__(self, id):
        self.id = id
        super().__init__(f"Resource with ID {id} not found.")
        
class OperationNotAllowedError(Exception):
    """Excepción para cuando se intenta realizar una operación no permitida."""
    def __init__(self, operation_name: str):
        super().__init__(f"Operation '{operation_name}' not allowed.")
        
class PermissionError(Exception):
    """Excepción para cuando el usuario no tiene permisos para modificar o acceder."""
    def __init__(self):
        super().__init__("Permission not allowed.")

class InfraestructureError(Exception):
    """Excepción base para errores técnicos (base de datos, red, etc)."""
    pass

class RepositoryError(InfraestructureError):
    """Error genérico del repositorio (fallo al leer/escribir)."""
    pass

class ConnectionDataBaseError(InfraestructureError):
    """No se pudo conectar a la base de datos."""
    pass

class TransactionError(InfraestructureError):
    """Error al manejar una transacción."""
    pass


class SerializationError(InfraestructureError):
    """Error al serializar/deserializar datos."""
    pass