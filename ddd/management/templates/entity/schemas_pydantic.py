# schemas in pydantic format

from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field, validator, model_validator, field_validator
from typing import Self, Dict, Any, Optional, ClassVar
from datetime import datetime
from uuid import UUID

class FileData(BaseModel):
    file_name: Optional[str] = None
    url: Optional[str] = None

class BaseDomainValueError(Exception):
    """Error de valor en atributos de la entidad [[ entity_name|capitalize_first ]]."""
    def __init__(self, detail: str, field: str = "value"):
        self.field = field
        self.detail = detail
        if field == "value":
            super().__init__(f"Value error: {detail}.")
        else:
            super().__init__(f"Field error in '{field}': {detail}.")   
    
class BaseEntity(BaseModel, ABC):
    """
    Clase de Entidad del dominio.
    Representa la lógica de negocio central y las reglas asociadas.
    """   

    domain_value_error_class: ClassVar[type] = BaseDomainValueError    

    class Meta:
        """
        Configuración de metadatos para la entidad.
        Define qué campos pueden enviarse (o no) en cada operación: creación (from_dict) y actualización (update).
        
                                | from_dict (creación)  | update() normal  | vía especial
        ------------------------|-----------------------|------------------|--------------
        required_fields         | obligatorio           | n/a              | n/a
        readonly_fields         | prohibido             | prohibido        | no existe
        protected_fields        | permitido/obligatorio | prohibido        | no existe
        special_update_fields   | permitido (depende)   | prohibido        | sí existe
        """

        required_fields: set = set()
        # Obligatorios al CREAR la entity (entity=from_dict(data)). No aplica a update().
        # Lanza una Excepcion si falta alguno al ejecutar el (entity=from_dict(data))

        readonly_fields: set = set()
        # Prohibidos SIEMPRE: en creación y en actualización.
        # Se generan internamente (ej: id, created_at), el cliente nunca los proporciona.

        protected_fields: set = set()
        # Permitidos en creación, pero INMUTABLES después: prohibidos en update().
        # Se fijan una vez y no se pueden modificar por la vía normal.

        special_update_fields: set = set()
        # Prohibidos en update() normal, pero SÍ modificables mediante un método dedicado
        # (ej: regenerate_api_key(), change_password()) con su propia validación.

        @classmethod
        def readonly_and_protected_fields(cls):
            # Unión de campos bloqueados en update(): inmutables (readonly) + fijados en creación (protected).
            return cls.readonly_fields | cls.protected_fields

    model_config = ConfigDict(
        validate_assignment=True,
        json_encoders={
            UUID: str,
            datetime: lambda v: v.isoformat() if v else None,
        }
    )            

    # -------------------------
    # VALIDACIÓN BASE
    # -------------------------    

    @abstractmethod
    def validate(self) -> None:
        pass
    
    @model_validator(mode='after')
    def _run_validation(self) -> Self:
        """
        Valida la entidad después de la creación o actualización.
            :raises BaseDomainValueError: Si las reglas de negocio no se cumplen.
        """

        # validar que esten los campos requeridos
        if self.Meta.required_fields:
            missing_fields = []
            for field in self.Meta.required_fields:
                if getattr(self, field) is None:
                    missing_fields.append(field)
            if missing_fields:
                raise self.domain_value_error_class(field=",".join(missing_fields), detail="Missing required fields")

        # Ejecutar validaciones definidas
        self.validate()

        return self

    # -------------------------
    # UPDATE
    # -------------------------        
        
    def update(self, data: Dict[str, Any], add_mode: bool = False, exclude_none: bool = False) -> None:
        """
        Actualiza la entidad con nuevos datos, respetando los campos permitidos.
        excluyendo siempre los campos de solo lectura y protegidos,
        los campos de actualizacion especial deben ser manejados aparte.
        
        :param data: Diccionario con los nuevos valores.
        :param add_mode: Si es True, permite añadir nuevos campos que no existan en la entidad.
        :param exclude_none: Si es True, excluye los campos con valor None al actualizar.
        :raises BaseDomainValueError: Si hay un error en la estructura de los datos.
        """
        exclude_fields = (
            self.Meta.readonly_fields
            | self.Meta.protected_fields
            | self.Meta.special_update_fields
        )     

        valid_data = {}

        for key, value in data.items():
            is_updatable = hasattr(self, key) or add_mode == True
            is_not_excluded = key not in exclude_fields

            if is_updatable and is_not_excluded:
                valid_data[key] = value

        # Crear copia actualizada (Pydantic valida automáticamente)
        updated = self.model_copy(update=valid_data)

        # Reemplazar atributos actuales con todos los valores, incluidos None
        for field, value in updated.model_dump(exclude_none=exclude_none).items():
            try:
                setattr(self, field, value)
            except TypeError as e:
                raise self.domain_value_error_class(field=field, detail=f"Error in data structure: {str(e)}") from e

        self._run_validation()

    # -------------------------
    # SERIALIZACIÓN
    # -------------------------

    def to_dict(self, exclude_none: bool = False, include_readonly_fields: bool = True, include_protected_fields: bool = True, include_special_update_fields: bool = True) -> Dict[str, Any]:
        """
        Convierte a diccionario (compatible con JSON)
        excluyendo los campos con valor None, los de solo lectura y los que requieren actualización especial.

        :param exclude_none: Excluir campos con valor None.
        :param include_readonly_fields: Incluir campos de solo lectura.
        :param include_protected_fields: Si es True, incluye los campos protegidos
        :param include_special_update_fields: Incluir campos que requieren actualización especial.
        :return: Diccionario con los atributos de la entidad.
        """
        # Construir el diccionario excluyendo campos según los parámetros
        exclude_fields = set()
        if not include_readonly_fields:
            exclude_fields.update(self.Meta.readonly_fields)
        if not include_protected_fields:
            exclude_fields.update(self.Meta.protected_fields)
        if not include_special_update_fields:
            exclude_fields.update(self.Meta.special_update_fields)

        return self.model_dump(exclude_none=exclude_none, exclude=exclude_fields)

    def to_orm_dict_for_create(self) -> dict:
        return self.to_dict(include_readonly_fields=False)
    
    def to_orm_dict_for_update(self) -> dict:
        return self.to_dict(include_readonly_fields=False, include_protected_fields=False, include_special_update_fields=False)

    # -------------------------
    # FROM_DICT
    # -------------------------        

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEntity":
        """
        Crea una instancia de la entidad a partir de un diccionario.
        
        excluyendo siempre los campos de solo lectura
        y validando que esten presentes los campos requeridos.

        :param data: Diccionario con los atributos para crear la entidad.
        :return: Instancia de la entidad creada.
        :raises BaseDomainValueError: Si faltan campos requeridos o hay errores en la
        """
        data = data.copy()

        # Se excluyen los campos de solo lectura para evitar que se modifiquen al persistirlos en db
        for field in cls.Meta.readonly_fields:
            data.pop(field, None)

        # construir la entidad
        try:
            return cls(**data)
        except TypeError as e:
            raise cls.domain_value_error_class(field="Error building entity", detail=str(e)) from e

    # -------------------------
    # FROM_ORM_DICT
    # -------------------------

    @classmethod
    def from_orm_dict(cls, data: dict) -> "BaseEntity":
        """
        Crea una entidad a partir de un modelo de persistencia (ORM).

        A diferencia de `from_dict`, no excluye campos de solo lectura ni valida
        `required_fields`, ya que los datos provienen de una fuente de confianza
        (la base de datos) y no de un input externo/usuario.

        :param model: Instancia del modelo ORM con los atributos de la entidad.
        :return: La entidad reconstruida.
        :raises BaseDomainValueError: Si hay un error reconstruyendo la entidad.
        """
        data = data.copy()

        try:
            entity = cls(**data)
        except TypeError as e:
            raise cls.domain_value_error_class("Error building entity from orm dict", str(e))

        return entity