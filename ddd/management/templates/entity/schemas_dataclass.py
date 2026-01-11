from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Self
from uuid import UUID, uuid4
from abc import ABC, abstractmethod

@dataclass
class FileData:
    file_name: Optional[str] = None
    url: Optional[str] = None

class DomainValueError(Exception):
    def __init__(self, field: str, detail: str):
        super().__init__(f"{field}: {detail}")
    
@dataclass
class BaseEntity(ABC):
    """
    Clase de Entidad del dominio.
    Representa la lógica de negocio central y las reglas asociadas.
    """   

    class Meta:
        """
        Configuración de metadatos para la entidad.
        Define el comportamiento especial de los campos.
        """    
        required_fields: set = set() # Campos requeridos para la creación
        readonly_fields: set = set() # Campos de solo lectura - No pueden ser modificados una vez establecidos (prohibidos siempre en creacion/actualizaciones)
        protected_fields: set = set() # Campos que no deben ser incluidos en actualizaciones (prohibidos en ciertas operaciones)
        special_update_fields: set = set() # Campos que requieren actualización especial - Necesitan validaciones o procesamiento especial aparte

    # -------------------------
    # VALIDACIÓN BASE
    # -------------------------    

    @abstractmethod
    def validate(self) -> None:
        pass    

    def _run_validation(self) -> Self:
        """
        Valida la entidad después de la creación o actualización.
            :raises DomainValueError: Si las reglas de negocio no se cumplen.
        """

        missing_fields = [
            field for field in self.Meta.required_fields
            if getattr(self, field, None) is None
        ]
        if missing_fields:
            raise DomainValueError(",".join(missing_fields), "Missing required fields")

        self.validate()
        return self       

    # -------------------------
    # UPDATE
    # -------------------------        

    def update(self, data:dict[str, Any], addMode:bool = False) -> None:
        """
        Actualiza los atributos de la entidad con valores nuevos de forma simple
        excluyendo siempre los campos de solo lectura y protegidos,
        los campos de actualizacion especial deben ser manejados aparte.
        si addMode = True permite añadir campos nuevos

        :param data: Diccionario con los nuevos valores para los atributos.
        :param addMode: Si es True, permite añadir nuevos campos que no existan en la entidad.
        :raises DomainValueError: Si hay un error de estructura en los datos.
        """
        exclude_fields = (
            self.Meta.readonly_fields
            | self.Meta.protected_fields
            | self.Meta.special_update_fields
        )

        # Actualizar cada campo proporcionado en 'data'
        for key, value in data.items():
            if (hasattr(self, key) or addMode == True) and (key not in exclude_fields):
                try:
                    setattr(self, key, value)             
                except TypeError as e:
                    raise DomainValueError(field=key, detail=f"Error in data structure: {str(e)}") from e

        self._run_validation()     

    # -------------------------
    # SERIALIZACIÓN
    # -------------------------

    def to_dict(self, include_readonly_fields: bool = True, include_special_fields: bool = True) -> dict:
        """
        Convierte la entidad a un diccionario, 
        excluyendo los campos con valor None, los de solo lectura y los que requieren actualización especial.

        :param include_readonly_fields: Si es True, incluye los campos de solo lectura.
        :param include_special_fields: Si es True, incluye los campos que requieren actualización especial.
        :return: Diccionario con los atributos de la entidad.
        """
        # Construir el diccionario excluyendo campos según los parámetros
        exclude_fields = set()
        if not include_readonly_fields:
            exclude_fields.update(self.Meta.readonly_fields)
        if not include_special_fields:
            exclude_fields.update(self.Meta.special_update_fields)

        return {
            k: v for k, v in vars(self).items() 
            if v is not None and k not in exclude_fields
        }    

    # -------------------------
    # FROM_DICT
    # -------------------------   

    @classmethod
    def from_dict(cls, data: dict) -> "BaseEntity":
        """
        Crea una instancia de la entidad a partir de un diccionario.

        excluyendo siempre los campos de solo lectura
        y validando que esten presentes los campos requeridos.
        """
        data = data.copy()

        for field in cls.Meta.readonly_fields:
            data.pop(field, None)

        try:
            entity = cls(**data)
        except TypeError as e:
            raise DomainValueError("Error building entity", str(e))

        return entity._run_validation()
