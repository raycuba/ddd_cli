@dataclass
class [[ entity_name.capitalize() ]]Entity:
    """
    Entidad del dominio para [[ entity_name.lower() ]].

    Esta clase representa la lógica de negocio central y las reglas asociadas 
    con [[ entity_name.lower() ]] en el sistema.
    """

    # Lista de campos especiales
    # Los campos especiales son aquellos que no deben ser actualizados directamente
    # o que requieren un tratamiento especial al ser guardados.
    # Por ejemplo: id, uuid, external_id, etc.
    SPECIAL_FIELDS = (
        'id', 'uuid', 'external_id', 'externals'
    )    

    # Identificadores
    id: Optional[int] = None  # ID relacionado con la base de datos
    uuid: Optional[UUID] = None

    # Atributos principales
    attributeName: Optional[str] = None  # Atributo opcional
    attributeEmail: Optional[str] = None  # Atributo opcional

    # Relaciones
    external_id: Optional[int] = None  # ID de una entidad relacionada (opcional)

    # Relaciones Many-to-Many o Reverse FK
    externals: Optional[List[int]] = None  # Lista de IDs de entidades relacionadas

    
    # Descomentar si se quiere hacer una validacion estricta
    #def __post_init__(self):
    #    self.validate()   


    def validate(self) -> None:
        """
        Valida la entidad antes de guardar o procesar.
        Lanza excepciones si las reglas de negocio no se cumplen.
        - Consistencia interna de los atributos
        - Validaciones intrínsecas al momento de creación/modificación
        """
        if not self.attributeName or len(self.attributeName) < 3:
            raise [[ entity_name.capitalize() ]]ValueError(field="attributeName", detail="attributeName must be at least 3 characters")

        if self.attributeEmail and len(self.attributeEmail) > 500:
            raise [[ entity_name.capitalize() ]]ValueError(field="attributeEmail", detail="attributeEmail must not exceed 500 characters")


    def update(self, data:dict, addMode:bool = False) -> None:
        """
        Actualiza los atributos de la entidad con valores nuevos.
        si addMode = True permite añadir campos nuevos
        :param data: Diccionario con los nuevos valores para los atributos.
        :param addMode: Si es True, permite añadir nuevos campos que no existan en la entidad.
        :raises [[ entity_name.capitalize() ]]ValueError: Si hay un error de estructura en los datos.
        """
        # Actualizar cada campo proporcionado en 'data'
        for key, value in data.items():
            if hasattr(self, key) or addMode:
                try:
                    setattr(self, key, value)             
                except TypeError as e:
                    raise [[ entity_name.capitalize() ]]ValueError(field=key, detail=f"Error in data structure: {str(e)}") from e

        self.validate()    


    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario.
        """
        return self.__dict__

        
    @staticmethod
    def from_dict(data: dict) -> "[[ entity_name.capitalize() ]]Entity":
        """
        Crea una instancia de la entidad a partir de un diccionario.
        """

        # aqui quitaremos de 'data' los campos no deseados para la entity

        # construir la entidad
        try:
            entity = [[ entity_name.capitalize() ]]Entity(**data)
        except TypeError as e:
            raise [[ entity_name.capitalize() ]]ValueError("Error building entity:", str(e)) from e

        return entity
        

    '''
    Ejemplos de: 

    - Atributos obligatorios y opcionales
        name: Optional[str] = None  # Nombre 
        email: Optional[str] = None  # Email opcional
        slug: Optional[str] = None  # Identificador único legible para URLs
        content: Optional[str] = None  # Contenido detallado o descripción extensa
        price: Optional[float] = None  # Precio o valor numérico
        quantity: Optional[int] = None  # Cantidad disponible o asociada
        rating: Optional[float] = None  # Valoración media (ej. 4.5 estrellas)
        is_active: bool = True  # Estado activo/inactivo
        is_featured: Optional[bool] = None  # Si es destacado/promocionado
        is_valid: Optional[bool] = True # Opcional, pero valor inicial no None
        updated_at: Optional[str] = None  # Fecha de última modificación (ISO 8601)
        deleted_at: Optional[str] = None  # Fecha de eliminación o "soft delete"
        image: Optional[str] = None  # URL hacia una imagen asociada
        video: Optional[str] = None  # URL hacia un video asociado
        latitude: Optional[float] = None  # Coordenada de latitud
        longitude: Optional[float] = None  # Coordenada de longitud
        location_name: Optional[str] = None  # Nombre del lugar (dirección o ciudad)
        created_by: Optional[int] = None  # Usuario que creó la entidad
        updated_by: Optional[int] = None  # Usuario que actualizó la entidad
        order_status: Optional[str] = None  # Estado de la orden (e.g., "PENDING", "COMPLETED")
        total_price: Optional[float] = None  # Precio total de la orden
        config: Optional[Dict] = field(default_factory=dict)  # Configuración adicional, ej. {"shipping": "free", "gift_wrap": True} 
        categories: Optional[List[str]] = field(default_factory=list)  # Lista de categorías asociadas, ej. ["electronics", "clothing"]
        items: Optional[List[Dict]] = None  # Lista de artículos asociados ej. [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]

    - Atributos de relación
        external_id: Optional[int] = None  # Identificador externo (ideal para relaciones 1-a-1 con otras entidades o FK)
        external_uuid: Optional[str] = None  # UUID externo
        externals: Optional[List[int]] = None  # Lista de identificadores externos (ideal para relaciones 1-a-M o M-a-M)
        externals_uuids: Optional[List[str]] = None  # Lista de UUIDs externos

    Nota: en un @dataclass lo mejor es que los atributos sean opcionales,
    y que se inicialicen con None, para evitar problemas de validación
    y que se puedan añadir nuevos atributos sin problemas.

    '''