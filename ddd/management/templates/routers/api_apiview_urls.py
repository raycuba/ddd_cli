"""
Router para [[ entity_name.lower() ]] API APIView.
"""

from django.urls import path
from . import [[ entity_name.lower() ]]_views

app_name = '[[ entity_name.lower() ]]'

# API endpoints con URLs individuales para cada operación HTTP
urlpatterns = [
    # Lista de [[ entity_name.lower() ]]s - GET /
    path('', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view({'get': 'list'}), name='[[ entity_name.lower() ]]-list'),
    
    # Crear [[ entity_name.lower() ]] - POST /
    path('', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view({'post': 'create'}), name='[[ entity_name.lower() ]]-create'),
    
    # Obtener [[ entity_name.lower() ]] específico - GET /<id>/
    path('<int:id>/', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view({'get': 'retrieve'}), name='[[ entity_name.lower() ]]-retrieve'),
    
    # Actualizar [[ entity_name.lower() ]] completo - PUT /<id>/
    path('<int:id>/', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view({'put': 'update'}), name='[[ entity_name.lower() ]]-update'),
    
    # Actualizar [[ entity_name.lower() ]] parcial - PATCH /<id>/
    path('<int:id>/', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view({'patch': 'partial_update'}), name='[[ entity_name.lower() ]]-partial-update'),
    
    # Eliminar [[ entity_name.lower() ]] - DELETE /<id>/
    path('<int:id>/', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view({'delete': 'destroy'}), name='[[ entity_name.lower() ]]-destroy'),
]

"""
Incluye este URLconf in your project's main urls.py:

    from django.urls import path, include
    
    urlpatterns = [
        path('api/[[ entity_name.lower() ]]s/', include('[[ app_name.lower() ]].[[ entity_name.lower() ]]_urls')),
    ]

This will create the following endpoints with individual URL patterns:
    GET    /api/[[ entity_name.lower() ]]s/     - List all [[ entity_name.lower() ]]s ([[ entity_name.lower() ]]-list)
    POST   /api/[[ entity_name.lower() ]]s/     - Create new [[ entity_name.lower() ]] ([[ entity_name.lower() ]]-create)
    GET    /api/[[ entity_name.lower() ]]s/{id}/ - Retrieve [[ entity_name.lower() ]] ([[ entity_name.lower() ]]-retrieve)
    PUT    /api/[[ entity_name.lower() ]]s/{id}/ - Update [[ entity_name.lower() ]] ([[ entity_name.lower() ]]-update)
    PATCH  /api/[[ entity_name.lower() ]]s/{id}/ - Partial update [[ entity_name.lower() ]] ([[ entity_name.lower() ]]-partial-update)
    DELETE /api/[[ entity_name.lower() ]]s/{id}/ - Delete [[ entity_name.lower() ]] ([[ entity_name.lower() ]]-destroy)

Note: Each HTTP method has its own dedicated URL pattern for maximum control and clarity.
"""
