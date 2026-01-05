"""
Router for [[ entity_name.lower() ]] API APIView.
"""

from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from . import [[ entity_name.lower() ]]_views

app_name = '[[ entity_name.lower() ]]s'

# URLs manuales con tipos explícitos evitar warnings de drf-spectacular
urlpatterns = [
    # Lista de [[ entity_name.lower() ]]s
    path('', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view(), name='[[ entity_name.lower() ]]_list_create'),
    
    # Detalle de [[ entity_name.lower() ]] por ID
    path('<int:id>/', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView.as_view(), name='[[ entity_name.lower() ]]_detail'),
]

"""Dont forget to include this router in your project's main urls.py file.
like this:

    path('[[ entity_name.lower() ]]s/', include('[[ app_name.lower() ]].[[ entity_name.lower() ]]_urls')),
"""
