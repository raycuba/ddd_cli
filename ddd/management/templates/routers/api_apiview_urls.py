"""
Router for [[ entity_name.lower() ]] API APIView.
"""

from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from . import [[ entity_name.lower() ]]_views

app_name = '[[ entity_name.lower() ]]s'

router_[[ entity_name.lower() ]] = DefaultRouter() if settings.DEBUG else SimpleRouter()

# define routes
router_[[ entity_name.lower() ]].register('', [[ entity_name.lower() ]]_views.[[ entity_name|capitalize_first ]]APIView, basename='[[ entity_name.lower() ]]s')

"""Dont forget to include this router in your project's main urls.py file.
like this:

    path('[[ entity_name.lower() ]]s/', include((router_[[ entity_name.lower() ]].urls, "[[ entity_name.lower() ]]s"), namespace="[[ entity_name.lower() ]]s")),
"""
