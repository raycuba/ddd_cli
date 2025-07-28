
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import ValidationError

# importa las entidades utilizadas aqui
from ..models import Entity1
from ..utils.mappers import Mapper
from ..utils.clean_dict_of_keys import clean_dict_of_keys
from ..domain.entities import Entity1Entity
from ..domain.exceptions import EntityNotFoundError


class Entity1Repository:
    """
    Repositorio para manejar la persistencia de datos de la entidad: entity1.
    
    Este repositorio incluye:
    - Validación de existencia de registros.
    - Control de unicidad.
    - Métodos básicos.
    """

    @staticmethod
    def get_all(filters: Optional[dict] = None) -> List[ Entity1Entity ]:
        """
        Obtiene todos los registros de la entidad.
        :return: Lista de registros de la entidad.
        """

        instance_list = Entity1.objects.all()    

        # Aplicar filtros si se proporcionan
        if filters:
            if "nombre" in filters and filters["nombre"] != "":
                instance_list = instance_list.filter(nombre__icontains=filters["nombre"])      
                
        # Tener en cuenta los campos reales que se necesitan en el listado
        instance_list = instance_list.only("id", "nombre", "created_at")

        # Convertir a entidades usando el Mapper genérico
        return [Mapper.model_to_entity(instance, Entity1Entity) for instance in instance_list]        


    @staticmethod
    def get_by_id(id) -> Optional[ Entity1Entity ]:
        """
        Obtiene un registro por su ID.
        
        :param id: ID del registro a recuperar.
        :return: El entidad encontrada o None si no existe.
        """

        try:
            instance = Entity1.objects.get(id=id)
            return Mapper.model_to_entity(instance, Entity1Entity)

        except Entity1.DoesNotExist:
            return None


    @staticmethod
    def exists_by_field(field_name, value) -> bool:
        """
        Verifica si existe un registro con un valor específico para un campo dado.

        :param field_name: Nombre del campo a buscar.
        :param value: Valor del campo a verificar.
        :return: True si existe un registro con el valor dado, False en caso contrario.
        """

        return Entity1.objects.filter(**{field_name: value}).exists()


    @staticmethod
    def count_all(filters: Optional[dict] = None) -> int:
        """
        Cuenta registros que cumplen con ciertas condiciones.

        :param conditions: Condiciones de filtro como clave-valor.
        :return: Número de registros que cumplen las condiciones.
        """

        instance_list = Entity1.objects.all()    

        # Aplicar filtros si se proporcionan
        if filters:
            if "nombre" in filters and filters["nombre"] != "":
                instance_list = instance_list.filter(nombre__icontains=filters["nombre"])            

        return instance_list.count()            


    @staticmethod
    def create(entity: Entity1Entity, external_id: Optional[int], externals: Optional[List[int]], adicionalData=None) -> Entity1Entity:
        """
        Crea un nuevo registro.

        :param entity: Entidad con los datos necesarios para crear el registro.
        :param external_id: ID del padre si es necesario (opcional).
        :param externals: Lista de IDs de entidades relacionadas (opcional).
        :param adicionalData: Datos adicionales a incluir en la creación.
        :return: La entidad creada.
        :raises ValueError: Si los datos no son válidos.
        """
        #convertir a dict
        data = entity.to_dict()        

        # Eliminar de la data las propiedades que requieren un tratamiento especial
        data = clean_dict_of_keys(data, keys=entity.SPECIAL_FIELDS)

        # Crear el registro a partir de los campos presentes en la 'data'
        instance = Entity1(**data)

        # Si se proporciona un ID de otra entidad, actualizarlo
        # django crea el campo 'external_id' automáticamente si la relación es ForeignKey => otherEntity
        if external_id is not None:
            instance.external_id = external_id

        # Si se proporcionan IDs de entidades relacionadas, agregarlos
        if externals is not None:
            # Asignar directamente los IDs
            instance.externals.set(externals)

        # Si adicionalData, agregar datos adicionales
        if adicionalData:
            # Aquí puedes agregar lógica para manejar datos adicionales específicos
            # Por ejemplo, guardar una foto, un password, o cualquier otro campo especial
            pass

        # Validar y guardar
        try:
            instance.full_clean()  # Validaciones del modelo
            instance.save()

        except ValueError as e:
            raise ValueError(f"An error occurred while processing the value: {e}")
        
        return Mapper.model_to_entity(instance, Entity1Entity)


    @staticmethod
    def save(entity: Entity1Entity, external_id: Optional[int], externals: Optional[List[int]], adicionalData=None) -> Entity1Entity:
        """
        Guarda los cambios en una entidad existente.

        :param entity: Entidad con los datos a actualizar (debe traer el id en los campos).
        :param external_id: ID del padre si es necesario (opcional).
        :param externals: Lista de IDs de entidades relacionadas (opcional).
        :param adicionalData: Datos adicionales a incluir en la actualización.
        :return: La entidad guardada.
        :raises EntityNotFoundError: Si no existe el registro con el ID dado.
        :raises ValueError: Si los datos no son válidos.
        """

        try:
            # Recuperar el modelo existente basado en el ID de la entidad
            instance = Entity1.objects.get(id=entity.id)

            # Actualizar cada campo de la entidad en el modelo
            for key, value in entity.to_dict().items():
                if hasattr(instance, key):
                    if not key in instance.SPECIAL_FIELDS: # No actualizar campos especiales
                        setattr(instance, key, value)

            # Si se proporciona un ID de otra entidad, actualizarlo
            if external_id is not None:
                instance.external_id = external_id

            # Si se proporcionan IDs de entidades relacionadas, actualizarlos
            if externals is not None:
                # Asignar directamente los IDs
                instance.externals.set(externals)

            # Si adicionalData, agregar datos adicionales
            if adicionalData:
                # Aquí puedes agregar lógica para manejar datos adicionales específicos
                # Por ejemplo, guardar una foto, un password, o cualquier otro campo especial
                pass

            # Validar y guardar
            instance.full_clean()  # Validaciones del modelo Django
            instance.save()
            
            # Convertir el modelo actualizado de vuelta a una entidad
            return Mapper.model_to_entity(instance, Entity1Entity)

        except Entity1.DoesNotExist:
            raise EntityNotFoundError(f"No entity1 found with ID {id}")

        except ValidationError as e:
            raise ValueError(f"Validation error occurred: {e.message_dict}")


    @staticmethod
    def delete(id) -> bool:
        """
        Elimina un registro por su ID.

        :param id: ID del registro a eliminar.
        :raises EntityNotFoundError: Si no existe el registro con el ID dado.
        """

        try:
            instance = Entity1.objects.get(id=id)
            instance.delete()
            return True

        except Entity1.DoesNotExist:
            raise EntityNotFoundError(f"No entity1 found with ID {id}")


'''
En Django ORM los campos de relación se definen como ForeignKey, ManyToManyField o OneToOneField.
Para la traduccion de relaciones entre entidades, se pueden utilizar los siguientes campos:

- `external_id`: 
    Para relaciones de clave externa (ForeignKey) o uno a uno (OneToOneField)
        ej: external = models.ForeignKey(OtherEntity, on_delete=models.CASCADE, related_name='related_entities')
        o    ej: external = models.OneToOneField(OtherEntity, on_delete=models.CASCADE, related_name='related_entity')
            
    el model de Django crea automáticamente el campo `external_id` este campo es accesible como un atributo de la entidad.

- `external_uuid`: Para relaciones basadas en un UUID adicional aparte del ID.
        ej: external = models.UUIDField(default=uuid.uuid4, editable=False)
     es necesario definir en el model de Django una propiedad 'external_uuid' que retorne el UUID relacionado.
    @property
    def external_uuid(self):
        return str(self.external.uuid) if self.external else None

- `externals`: Para relaciones de muchos a muchos (ManyToManyField).
    Para relaciones de muchos a muchos:
        ej: externals = models.ManyToManyField(OtherEntity, related_name='related_entities')

- `externals_uuids`: Para relaciones de muchos a muchos basadas en UUID adicional aparte del ID.
        ej: externals = models.ManyToManyField(OtherEntity, related_name='related_entities')
    es necesario definir en el model de Django una propiedad 'external_uuids' que retorne una lista de UUIDs relacionados.
    @property
    def externals_uuids(self):
        return list(self.externals.values_list('uuid', flat=True))
'''

'''
### 💡 ¿Por qué ir más allá de los repositorios básicos?
Este repositorio ya implementa una base sólida para DDD en Django: 
mapeo de entidades, validaciones, manejo de relaciones (`external_id`, `externals`) y encapsulación del ORM.  
Sin embargo, a medida que el dominio crezca, 
métodos como `get_all()` o `create()` pueden volverse insuficientes o ineficientes.

En DDD, el repositorio debe hablar el **lenguaje del negocio**, no solo ofrecer operaciones CRUD genéricas.  
Por eso, es valioso **enriquecerlo estratégicamente**, manteniendo la coherencia con esta plantilla.

### 🚀 Cómo enriquecer este repositorio (sin romper su diseño actual)
#### 1. 🗣️ **Métodos específicos orientados al dominio**
    En lugar de exponer solo filtros genéricos por `nombre`, puedes agregar métodos que expresen reglas de negocio:
        @staticmethod
        def get_activos():
            return Entity1.objects.filter(estado='activo')

        @staticmethod
        def find_by_slug(slug: str) -> OptionalEntity1Entity:
            try:
                instance = Entity1.objects.get(slug=slug)
                return Mapper.model_to_entity(instance, Entity1Entity)
            except Entity1.DoesNotExist:
                return None

    Estos métodos se integran naturalmente con `get_by_id()` y `get_all()`, y evitan que la lógica de negocio se repita en servicios.

#### 2. 🔍 **QuerySets y Managers personalizados**
    Puedes encapsular lógica común (como filtros por estado o relaciones) en un `Manager` personalizado:
        class Entity1Manager(models.Manager):
            def activos(self):
                return self.filter(estado='activo')
            def con_relacion(self):
                return self.select_related('external').prefetch_related('externals')

        class Entity1(models.Model):
            ...
            objects = Entity1Manager()

    Luego, en el repositorio:
        @staticmethod
        def get_all(filters=None):
            instance_list = Entity1.objects.activos()  # Usa tu Manager
            if filters and "nombre" in filters:
                instance_list = instance_list.filter(nombre__icontains=filters["nombre"])
            return [Mapper.model_to_entity(inst, Entity1Entity) for inst in instance_list]

        @staticmethod
        def get_all_with_relations():
            instance_list = Entity1.objects.activos().con_relacion() # Usa tu Manager
            if filters:
                instance_list = instance_list.filter(nombre__icontains=filters["nombre"])
            return [Mapper.model_to_entity(inst, Entity1Entity) for inst in instance_list]

    Así mantienes el diseño actual, pero con mejor rendimiento y expresividad.

#### 3. 📦 **Paginación + optimización de consultas**
    La plantilla ya usa `.only()` para optimizar carga. Puedes extenderlo con paginación:

        @staticmethod
        def get_paginated(page: int, size: int, filters=None):
            offset = (page - 1) * size
            limit = offset + size
            instance_list = Entity1.objects.all()
            if filters and "nombre" in filters:
                instance_list = instance_list.filter(nombre__icontains=filters["nombre"])
            instance_list = instance_list.only("id", "nombre", "created_at")[offset:limit]
            return [Mapper.model_to_entity(inst, Entity1Entity) for inst in instance_list]

    Ideal para APIs o listados grandes.

#### 4. 🔄 **Separación de lectura y escritura (CQRS básico)**
    Aunque la plantilla combina lectura y escritura, puedes dividirla cuando el sistema escala:

        class Entity1ReadRepository:
            @staticmethod
            def get_all(...):  # Igual al actual
            @staticmethod
            def count_all(...):  # Ya implementado

        class Entity1WriteRepository:
            @staticmethod
            def create(...):   # Usa `adicionalData` para lógica especial
            @staticmethod
            def save(...):     # Con validaciones y relaciones
            @staticmethod
            def delete(...):   # Con manejo de errores

    Esto permite optimizar consultas (lectura) sin afectar la lógica de mutación (escritura).

#### 5. 🧠 **Consultas complejas bien encapsuladas**
    Cuando necesites agregaciones o filtros avanzados, encapsúlalos en métodos del repositorio:

        from django.db.models import Count
        @staticmethod
        def get_con_muchos_externals(min_relaciones=3):
            instances = Entity1.objects.annotate(
                total_externals=Count('externals')
            ).filter(total_externals__gt=min_relaciones)
            return [Mapper.model_to_entity(inst, Entity1Entity) for inst in instances]

    Así mantienes el mapeo y la coherencia del dominio.

#### 6. **Uso de `select_related` y `prefetch_related`**
    La plantilla no los usa aún, pero son fáciles de integrar en `get_all()` o nuevos métodos:

        @staticmethod
        def get_all_with_relations():
            instance_list = Entity1.objects.select_related('external').prefetch_related('externals')
            if filters:
                instance_list = instance_list.filter(nombre__icontains=filters["nombre"])
            return [Mapper.model_to_entity(inst, Entity1Entity) for inst in instance_list]

    Evita el problema N+1 cuando accedes a relaciones.

#### 7. **Consultas RAW o expresiones ORM avanzadas**
    Usa `Q`, `F`, `Subquery`, o SQL crudo **dentro del repositorio** cuando el ORM no alcance:

        from django.db.models import Q, 
        @staticmethod
        def search_advanced(query):
            instances = Entity1.objects.filter(
                Q(nombre__icontains=query) | Q(descripcion__icontains=query)
            )
            return [Mapper.model_to_entity(inst, Entity1Entity) for inst in instances]

        @staticmethod
        def reactivar_registros():
            Entity1.objects.filter(estado='inactivo').update(estado=F('estado_anterior'))

        @staticmethod
        def busqueda_compleja_sql():
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM app_entity1 WHERE estado = %s", ['activo'])
                rows = cursor.fetchall()
            return [Mapper.model_to_entity(row, Entity1Entity) for row in rows]

    El repositorio sigue siendo el único punto de acceso al ORM.

#### 8. **Manejo de excepciones y errores**
    La plantilla ya captura `DoesNotExist` y `ValidationError`. Puedes mejorarla:

        try:
            # Lógica que puede generar excepciones
            pass

        except ValidationError as e:
            raise ValueError(f"Error de validación en entity1: {e.message_dict}")
        except Exception as e:
            # Evita exponer errores internos
            raise ValueError(f"No se pudo guardar el entity1: operación no permitida.")

    Así proteges la capa de dominio de detalles técnicos.

#### 9. **Documentación y claridad**
    Los métodos del repositorio deben reflejar intenciones del negocio, no solo operaciones técnicas:
        @staticmethod
        def get_all(filters=None) -> ListEntity1Entity:
            """
            Obtiene todos los entity1 que coincidan con los filtros.
            Usa `.only()` para optimizar rendimiento.
            :param filters: Diccionario con filtros (ej. {"nombre": "juan"}).
            :return: Lista de entidades Entity1.
            """
    Esto hace que el repositorio sea autoexplicativo.

#### 10. **Pruebas unitarias y de integración**
    Cada método debe tener pruebas. Ejemplo con `create()`:
        from django.test import TestCase
        from .repositories import UserRepository    

        class UserRepositoryTests(TestCase):
            def setUp(self):
                # Configuración inicial para las pruebas, si es necesario
                pass
        
            def test_create_con_external_y_externals(self):
                entity = Entity1Entity(nombre="Test")
                created = Entity1Repository.create(
                    entity=entity,
                    external_id=1,
                    externals=[1, 2],
                    adicionalData={"archivo": "file.pdf"}
                )
                self.assertIsNotNone(created.id)
                self.assertEqual(created.nombre, "Test")

                # Verifica relaciones
                instance = Entity1.objects.get(id=created.id)
                self.assertEqual(instance.external_id, 1)
                self.assertEqual(instance.externals.count(), 2)

    Así aseguras que `external_id`, `externals` y `adicionalData` funcionen como esperas.

### ✅ Conclusión
Esta plantilla ya cumple con lo esencial para DDD en Django.  
Las recomendaciones no son "extras", sino **posibles evoluciones naturales** que puedes aplicar **cuando el dominio lo requiera**.

El repositorio sigue siendo el traductor entre tu modelo de negocio y Django ORM.  
Hazlo más expresivo, no más complejo.
'''
