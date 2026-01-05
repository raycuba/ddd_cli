"""
Router for [[ entity_name.lower() ]] API ViewSet.
"""

from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from . import [[ entity_name.lower() ]]_views

app_name = '[[ entity_name.lower() ]]s'

# Router automático para ViewSet (recomendado)
router = DefaultRouter()
router.register(r'', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]ViewSet, basename='[[ entity_name.lower() ]]')

urlpatterns = [
    path('', include(router.urls)),
]

# Alternativa: URLs manuales con tipos explícitos (descomentar si necesitas control total)
# urlpatterns = [
#     # Lista y creación
#     path('', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]ViewSet.as_view({
#         'get': 'list', 
#         'post': 'create'
#     }), name='[[ entity_name.lower() ]]s-list'),
#     
#     # Detalle, actualización y eliminación
#     path('<int:pk>/', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]ViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'patch': 'partial_update',
#         'delete': 'destroy'
#     }), name='[[ entity_name.lower() ]]s-detail'),
# ]

"""Dont forget to include this router in your project's main urls.py file.
like this:

    path('[[ entity_name.lower() ]]s/', include('[[ app_name.lower() ]].[[ entity_name.lower() ]]_urls')),
"""