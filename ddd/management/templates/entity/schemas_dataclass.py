# schemas in dataclass format

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Self, ClassVar
from uuid import UUID, uuid4
from abc import ABC, abstractmethod

@dataclass
class FileData:
    file_name: Optional[str] = None
    url: Optional[str] = None  
        
class BaseDomainValueError(Exception):
    """Error de valor en atributos de la entidad [[ entity_name|capitalize_first ]]."""
    def __init__(self, detail: str = None, field: str = "value", *args, **kwargs):
        self.field = field
        self.detail = detail
        # Guardamos TODO lo que sobre en kwargs
        self.kwargs = kwargs
        
        # Prioridad de construcción del mensaje
        if field == "value" and detail:
            msg = f"Value error: {detail}."
        elif field and detail:
            msg = f"Field error in '{field}': {detail}."
        elif args:
            msg = args[0]
            # Si usamos el primer arg como mensaje, lo quitamos de la tupla 
            # para no duplicarlo en la base si fuera necesario
        else:
            msg = "Domain value error."
        
        # Pasamos el mensaje construido Y cualquier otro argumento posicional extra
        # que haya venido en *args (excepto el primero si ya lo usamos)
        super().__init__(msg, *args[1:] if (args and msg == args[0]) else args)
    
@dataclass
class BaseEntity(ABC):
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

    # -------------------------
    # VALIDACIÓN BASE
    # -------------------------    

    @abstractmethod
    def validate(self) -> None:
        pass    

    def _run_validation(self) -> Self:
        """
        Valida la entidad después de la creación o actualización.
            :raises BaseDomainValueError: Si las reglas de negocio no se cumplen.
        """

        missing_fields = [
            field for field in self.Meta.required_fields
            if getattr(self, field, None) is None
        ]
        if missing_fields:
            raise self.domain_value_error_class(",".join(missing_fields), "Missing required fields")

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
        :raises BaseDomainValueError: Si hay un error de estructura en los datos.
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
                    raise self.domain_value_error_class(field=key, detail=f"Error in data structure: {str(e)}") from e

        self._run_validation()     

    # -------------------------
    # SERIALIZACIÓN
    # -------------------------

    def to_dict(self, include_readonly_fields: bool = True, include_protected_fields: bool = True, include_special_update_fields: bool = True) -> dict:
        """
        Convierte la entidad a un diccionario, 
        excluyendo los campos con valor None, los de solo lectura y los que requieren actualización especial.

        :param include_readonly_fields: Si es True, incluye los campos de solo lectura.
        :param include_protected_fields: Si es True, incluye los campos protegidos
        :param include_special_update_fields: Si es True, incluye los campos que requieren actualización especial.
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

        return {
            k: v for k, v in vars(self).items() 
            if v is not None and k not in exclude_fields
        }    

    def to_orm_dict_for_create(self) -> dict:
        return self.to_dict(include_readonly_fields=False)
    
    def to_orm_dict_for_update(self) -> dict:
        return self.to_dict(include_readonly_fields=False, include_protected_fields=False, include_special_update_fields=False)

    # -------------------------
    # FROM_DICT
    # -------------------------   

    @classmethod
    def from_dict(cls, data: dict) -> "BaseEntity":
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

        try:
            entity = cls(**data)
        except TypeError as e:
            raise cls.domain_value_error_class("Error building entity", str(e))

        return entity._run_validation()

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
