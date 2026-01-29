# DDD CLI - Paquete para Django con Arquitectura DDD

## 🎯 Descripción del Proyecto

**DDD CLI** es un paquete pip que proporciona herramientas de línea de comandos para generar código estándar de Django siguiendo principios de **Domain-Driven Design (DDD)**. Automatiza la creación de entidades, servicios, repositorios, DTOs, serializers y vistas, manteniendo una estructura de proyecto consistente y bien organizada.

## 📦 Información del Paquete

- **Nombre**: `ddd-cli`
- **Versión**: 1.9.23
- **Autor**: Ragnar Bermúdez La O
- **Email**: ragnarbermudezlao@gmail.com
- **Python**: 3.12.8+
- **Framework**: Django + Django REST Framework

## 🚀 Instalación

```bash
pip install ddd-cli
```

## 📂 Estructura del Proyecto

```
ddd_cli/
├── ddd/
│   ├── management/
│   │   ├── commands/          # 🔧 Comandos CLI
│   │   │   ├── create_entity.py
│   │   │   ├── create_service.py
│   │   │   ├── create_repository.py
│   │   │   ├── create_dto.py
│   │   │   ├── create_serializer.py
│   │   │   ├── create_view.py
│   │   │   ├── create_view_api_apiview.py
│   │   │   ├── create_view_api_viewset.py
│   │   │   └── utils.py
│   │   └── templates/         # 📄 Plantillas Jinja2
│   │       ├── api/           # Plantillas para APIs
│   │       ├── dto/           # Plantillas para DTOs
│   │       ├── entity/        # Plantillas para entidades
│   │       ├── repository/    # Plantillas para repositorios
│   │       ├── routers/       # Plantillas para URLs
│   │       ├── serializer/    # Plantillas para serializers
│   │       ├── services/      # Plantillas para servicios
│   │       ├── templates/     # Plantillas HTML
│   │       ├── utils/         # Utilidades
│   │       └── view/          # Plantillas para vistas web
├── app/                       # 📋 Ejemplos de uso
│   ├── domain/
│   │   ├── entity1_entity.py
│   │   ├── entity1_exceptions.py
│   │   └── entity1_schemas.py
│   ├── entity1_urls.py
│   └── entity1_views.py
├── setup.py
├── README.md
└── requirements.txt
```

## 🛠️ Comandos Disponibles

### 🏗️ Entidades y Dominio
```bash
# Crear entidad de dominio con excepciones y esquemas
ddd create-entity app_path entity_name [--simulate]

# Ejemplo:
ddd create-entity apps/company company
```

### 🎯 Servicios
```bash
# Crear servicio de aplicación con lógica de negocio
ddd create-service app_path entity_name [--simulate]

# Ejemplo:
ddd create-service apps/company company
```

### 🗄️ Repositorios
```bash
# Crear repositorio con mappers y excepciones
ddd create-repository app_path entity_name [--simulate]

# Ejemplo:
ddd create-repository apps/company company
```

### 📊 DTOs (Data Transfer Objects)
```bash
# Crear DTOs con dataclass o Pydantic
ddd create-dto app_path dto_name [--simulate]

# Ejemplo:
ddd create-dto apps/company company_dto
```

### 🔄 Serializers
```bash
# Crear serializers de Django REST Framework
ddd create-serializer app_path serializer_name [--simulate]

# Ejemplo:
ddd create-serializer apps/company company
```

### 🌐 Vistas de API
```bash
# Crear vista API basada en APIView
ddd create-view-api-apiview app_path entity_name [--simulate]

# Crear vista API basada en ViewSet
ddd create-view-api-viewset app_path entity_name [--simulate]

# Ejemplos:
ddd create-view-api-apiview apps/company/api company
ddd create-view-api-viewset apps/company/api company
```

### 🖼️ Vistas Web
```bash
# Crear vistas web con formularios y templates
ddd create-view app_path entity_name [--simulate]

# Ejemplo:
ddd create-view apps/company company
```

## 📋 Opciones Globales

### `--simulate`
Simula la creación sin escribir archivos reales. Útil para:
- Verificar qué archivos se crearían
- Probar la configuración
- Debug del proceso

### `--help`
```bash
ddd --help              # Ayuda general
ddd create-entity --help # Ayuda específica del comando
```

## 🏗️ Arquitectura DDD Generada

### 📁 Estructura de Capas
```
app/
├── domain/                    # 🏛️ Capa de Dominio
│   ├── entity_name_entity.py     # Entidades
│   ├── entity_name_exceptions.py # Excepciones específicas
│   └── entity_name_schemas.py    # Esquemas de validación
├── infrastructure/            # 🔧 Capa de Infraestructura
│   ├── repositories/             # Repositorios
│   └── mappers/                  # Mappers de datos
├── services/                  # 🎯 Capa de Aplicación
│   └── entity_name_service.py    # Servicios de aplicación
├── serializers/               # 🔄 Serialización
│   └── entity_name_serializer.py
├── dtos/                      # 📊 Transferencia de Datos
│   └── dto_name.py
├── api/                       # 🌐 API REST
│   ├── entity_name_views.py      # Vistas de API
│   └── entity_name_urls.py       # Rutas de API
├── views/                     # 🖼️ Vistas Web
│   ├── entity_name_views.py      # Vistas web
│   ├── entity_name_forms.py      # Formularios
│   └── entity_name_urls.py       # Rutas web
└── templates/                 # 📄 Plantillas HTML
    └── entity_name/
```

### 🎨 Patrones Implementados

1. **Entity Pattern**: Entidades de dominio con validaciones
2. **Repository Pattern**: Acceso a datos desacoplado
3. **Service Pattern**: Lógica de negocio encapsulada
4. **DTO Pattern**: Transferencia de datos estructurada
5. **Mapper Pattern**: Transformación entre capas
6. **Exception Handling**: Manejo de errores específico por dominio

## 📄 Plantillas y Tecnologías

### 🔧 Tecnologías Utilizadas
- **Django** - Framework web
- **Django REST Framework** - API REST
- **Jinja2** - Motor de plantillas
- **Colorama** - Salida colorizada en terminal
- **Dataclass/Pydantic** - Estructuras de datos

### 📝 Tipos de Plantillas
- **Entity**: Dataclass y Pydantic
- **DTO**: Dataclass y Pydantic  
- **Repository**: Clases con mappers
- **Services**: Servicios de aplicación
- **API Views**: APIView y ViewSet
- **Web Views**: Vistas con formularios
- **Templates**: HTML con formularios Django

## 💡 Ejemplos de Uso

### 🏢 Crear Módulo Completo de Company
```bash
# 1. Crear entidad
ddd create-entity apps/companies company

# 2. Crear servicio
ddd create-service apps/companies company  

# 3. Crear repositorio
ddd create-repository apps/companies company

# 4. Crear DTO
ddd create-dto apps/companies company_dto

# 5. Crear API REST
ddd create-view-api-viewset apps/companies/api company

# 6. Crear vistas web
ddd create-view apps/companies company
```

### 🚀 Workflow Típico
```bash
# Desarrollo de nueva funcionalidad
ddd create-entity apps/products product
ddd create-service apps/products product
ddd create-repository apps/products product
ddd create-view-api-apiview apps/products/api product
```

## 📚 Documentación de Archivos Generados

### 🏛️ Entidades (`entity.py`)
- Clases de dominio con validaciones
- Excepciones específicas del dominio
- Esquemas de validación de datos

### 🎯 Servicios (`service.py`)
- Lógica de negocio encapsulada
- Operaciones CRUD del dominio
- Validaciones de reglas de negocio

### 🗄️ Repositorios (`repository.py`)
- Interfaz de acceso a datos
- Mappers entre modelos y entidades
- Manejo de excepciones de infraestructura

### 🌐 APIs (`views.py`, `urls.py`)
- Endpoints REST completos
- Documentación con drf-spectacular
- Manejo de errores HTTP estandardizado

## ⚙️ Configuración y Personalización

### 🎛️ Variables de Plantilla
Las plantillas usan variables Jinja2:
- `{{ entity_name }}` - Nombre de la entidad
- `{{ app_name }}` - Nombre de la aplicación  
- `{{ entity_name|capitalize_first }}` - Primera letra mayúscula
- `{{ entity_name|decapitalize_first }}` - Primera letra minúscula

### 🔧 Customización
- Modificar plantillas en `ddd/management/templates/`
- Extender comandos en `ddd/management/commands/`
- Añadir filtros Jinja2 en `utils.py`

## 🤝 Contribución

### 📁 Estructura de Desarrollo
```bash
# Instalación en modo desarrollo
cd ddd_cli/
python setup.py develop

# Ejecutar tests
python -m pytest

# Crear nueva plantilla
# 1. Agregar archivo en ddd/management/templates/
# 2. Crear o modificar comando en ddd/management/commands/
# 3. Actualizar CLI en cli.py
```

## 🎉 Beneficios

✅ **Consistencia**: Estructura estandarizada en todos los proyectos  
✅ **Rapidez**: Generación automática de código boilerplate  
✅ **DDD**: Arquitectura limpia con separación de responsabilidades  
✅ **Mantenibilidad**: Código bien organizado y documentado  
✅ **Escalabilidad**: Estructura preparada para proyectos grandes  
✅ **Best Practices**: Implementa patrones y convenciones estándar  

## 📞 Soporte

- **Issues**: Reportar bugs y solicitudes de funcionalidad
- **Documentación**: README.md para uso básico
- **Ejemplos**: Directorio `app/` con casos de uso reales

---

**DDD CLI** - Simplificando el desarrollo Django con arquitectura DDD 🚀 