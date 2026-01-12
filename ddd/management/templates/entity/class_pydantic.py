# entity in pydantic format

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any, ClassVar
from typing_extensions import Self
from uuid import UUID
from datetime import datetime
from .[[ entity_name.lower() ]]_exceptions import *
from .[[ entity_name.lower() ]]_schemas import FileData, BaseEntity

class [[ entity_name|capitalize_first ]]Entity(BaseEntity):
    """
    Entidad del dominio para [[ entity_name|decapitalize_first ]].

    Esta clase representa la lógica de negocio central y las reglas asociadas 
    con [[ entity_name|decapitalize_first ]] en el sistema.
    """

    domain_value_error_class = [[ entity_name|capitalize_first ]]ValueError    

    class Meta:
        required_fields = {"name", "email", "related_id"} # Requeridos para la creación
        readonly_fields = {"id", "uuid", "created_at", "updated_at"} # Prohibidos siempre en creacion/actualizaciones
        protected_fields = {"related_id"} # Prohibidos en ciertas operaciones y actualizaciones
        special_update_fields = {"relations", "photo"} # Prohibidos en actualizaciones normales, requieren manejo especial
        readonly_and_protected_fields = readonly_fields.union(protected_fields)

    # Identificadores
    id: Optional[int] = None  # ID relacionado con la base de datos
    uuid: Optional[UUID] = None

    # Atributos principales
    name: Optional[str] = None  # Atributo opcional
    email: Optional[str] = None  # Atributo opcional
    role: Optional[str] = None  # Atributo opcional
    status: Optional[str] = None  # Atributo opcional    
    photo: Optional[FileData] = None  # Atributo opcional

    # Relaciones
    related_id: Optional[int] = None  # ID de una entidad relacionada (opcional)

    # Relaciones Many-to-Many o Reverse FK
    relations: Optional[List[int]] = None  # Lista de IDs de entidades relacionadas

    # Descomentar si se quiere hacer una validacion estricta
    #def __post_init__(self):
    #    self.validate()   

    def validate(self) -> Self:
        """
        Valida la entidad antes de guardar o procesar.

        Lanza excepciones si las reglas de negocio no se cumplen.
        - Consistencia interna de los atributos
        - Validaciones intrínsecas al momento de creación/modificación
        """
        # Validaciones de ejemplo
        if not self.name or len(self.name) < 3:
            raise self.domain_value_error_class(field="name", detail="name must be at least 3 characters")

        if self.email and len(self.email) > 500:
            raise self.domain_value_error_class(field="email", detail="email must not exceed 500 characters")

        if self.relations and not all(isinstance(x, int) for x in self.relations):
            raise self.domain_value_error_class(field="relations", detail="relations must be a list of integers")  

        return self

        

'''
Guía para añadir nuevos campos a entidades Pydantic (v2)

- ✅ **Atributos opcionales**: usa `Optional[Tipo] = None`
- ✅ **Listas/Dicts por defecto**: usa `Field(default_factory=list)` o `Field(default_factory=dict)`
- ✅ **Atributos obligatorios**: define sin valor por defecto → fallará si no se proporciona
- ✅ **Valores por defecto simples**: asigna directamente (`is_active: bool = True`)
- ✅ **Fechas/horas**: usa `datetime` (no str) → Pydantic parsea ISO automáticamente
- ✅ **Archivos/URLs**: define submodelos tipados (ej. `FileData`) en vez de `dict`

Ejemplos:

    # Atributos simples opcionales
    name: Optional[str] = None
    email: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_featured: Optional[bool] = None

    # Atributos con valor por defecto (no None)
    is_active: bool = True
    rating: float = 0.0

    # Colecciones con valor por defecto (¡nunca asignes [] o {} directamente!)
    categories: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)
    items: List[Dict[str, Any]] = Field(default_factory=list)

    # Fechas (usa datetime, no str)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Relaciones (IDs)
    related_id: Optional[int] = None # Identificador externo (ideal para relaciones 1-a-1 con otras entidades o FK)
    relations: Optional[List[int]] = None # Lista de identificadores externos (ideal para relaciones 1-a-M o M-a-M)
    
    # Referencias UUID a otras entidades (solo son refencias)
    external_uuid: Optional[str] = None  # UUID externo (para relaciones 1-a-1)
    relations_uuids: Optional[List[str]] = None  # Lista de UUIDs externos  (para relaciones 1-a-M o M-a-M)

    # Objetos complejos (mejor que dict)
    image: Optional[FileData] = None
    address: Optional[AddressData] = None

⚠️ Importante:
- No uses `field(default_factory=...)` (eso es de dataclasses)
- En Pydantic v2, usa `Field(default_factory=...)` desde `pydantic`
- Los campos se validan automáticamente al crear la instancia
- Para validaciones personalizadas, usa `@model_validator` o `@field_validator`

💡 Validadores: ejemplos de uso:

    @model_validator(mode='after')
    def validate(self) -> self:
        if not self.name or len(self.name) < 3:
            raise self.domain_value_error_class("name must be at least 3 characters")
        return self

    @field_validator('email')
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and "@" not in v:
            raise self.domain_value_error_class("Invalid email address")
        return v

💡 Consejo:
Si añades un campo nuevo, no necesitas modificar `__init__`,
`to_dict()`, `from_dict()` ni `update()` → Pydantic lo maneja todo.
'''

    