# DDD CLI

Este paquete agrega comandos personalizados a Django para facilitar la implementación de una arquitectura Domain-Driven Design (DDD).

## Comandos disponibles

- `ddd create-entity <app_path> <entity_name> [--split]`
- `ddd create-service <app_path> <entity_name> <service_name> [--class-format] [--include-crud] [--split]`
- `ddd create-repository <app_path> <entity_name> [--include-crud]`
- `ddd create-dto <app_path> <dto_name> [--split]`
- `ddd create-view-api-apiview <app_path> <entity_name>`
- `ddd create-view-api-viewset <app_path> <entity_name>`
- `ddd create-view <app_path> <entity_name>`

## Mostrar ayuda
- `ddd --help`