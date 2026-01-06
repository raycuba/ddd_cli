"""
Router for [[ entity_name.lower() ]] API ViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import [[ entity_name.lower() ]]_views

app_name = '[[ entity_name.lower() ]]'

# Crear router y registrar ViewSet
router = DefaultRouter()
router.register(r'', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]ViewSet, basename='[[ entity_name.lower() ]]')

# URLs generadas automáticamente por el router
urlpatterns = [
    path('', include(router.urls)),
]

"""
Include this URLconf in your project's main urls.py:

    from django.urls import path, include
    
    urlpatterns = [
        path('api/[[ entity_name.lower() ]]s/', include('[[ app_name.lower() ]].[[ entity_name.lower() ]]_urls')),
    ]

The DefaultRouter will automatically generate the following endpoints:
    GET    /api/[[ entity_name.lower() ]]s/           - List [[ entity_name.lower() ]]s
    POST   /api/[[ entity_name.lower() ]]s/           - Create new [[ entity_name.lower() ]]
    GET    /api/[[ entity_name.lower() ]]s/{id}/      - Retrieve [[ entity_name.lower() ]]
    PUT    /api/[[ entity_name.lower() ]]s/{id}/      - Update [[ entity_name.lower() ]]
    PATCH  /api/[[ entity_name.lower() ]]s/{id}/      - Partial update [[ entity_name.lower() ]]
    DELETE /api/[[ entity_name.lower() ]]s/{id}/      - Delete [[ entity_name.lower() ]]

Additional router features:
    GET    /api/[[ entity_name.lower() ]]s/           - Browsable API root (if DEBUG=True)
    OPTIONS /api/[[ entity_name.lower() ]]s/          - API metadata
    
Benefits of using DefaultRouter:
    ✅ Automatic URL generation
    ✅ Consistent naming conventions  
    ✅ Built-in API browsability
    ✅ Less code maintenance
    ✅ Standard DRF patterns
"""