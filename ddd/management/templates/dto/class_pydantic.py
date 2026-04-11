class [[ dto_name|capitalize_first ]]Dto(BaseModel):
    """
    Data Transfer Object para [[ dto_name|decapitalize_first ]].

    Este DTO se utiliza para transferir datos entre capas del sistema, 
    como entre la capa de dominio y la capa de infraestructura o vistas.
    """

    # identificadores
    id: Optional[int] = None  # ID es opcional al crear un nuevo objeto

    # Atributos principales
    name: str  # Atributo obligatorio
    email: Optional[str] = None  # Atributo opcional

    # Relaciones
    related_id: Optional[int] = None  # ID de una entidad relacionada (opcional)

    # Relaciones Many-to-Many o Reverse FK
    relations: Optional[List[int]] = None  # Lista de IDs de entidades relacionadas    

    model_config = ConfigDict(
        validate_assignment=True,
        json_encoders={
            UUID: str,
            datetime: lambda v: v.isoformat() if v else None,
        }
    )    

    @model_validator(mode='after')
    def validate(self) -> Self:
        """
        Valida los datos del DTO.
        Transporte y validación básica de datos
        - Validaciones centradas en un conjunto específico de datos (integridad de datos)
        - Ejemplo: campos no nulos, longitud mínima
        """ 
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario (compatible con JSON)"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "[[ dto_name|capitalize_first ]]Dto":
        """Crea una instancia desde un diccionario"""
        return cls(**data)        


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
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    is_featured: Optional[bool] = None

    # Atributos con valor por defecto (no None)
    is_active: bool = True
    rating: Decimal = Decimal("0.0")

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
            raise ValueError("name must be at least 3 characters")
        return self

    @field_validator('email')
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and "@" not in v:
            raise ValueError("Invalid email address")
        return v

💡 Consejo:
Si añades un campo nuevo, no necesitas modificar `__init__`,
`to_dict()`, `from_dict()` ni `update()` → Pydantic lo maneja todo.
'''
