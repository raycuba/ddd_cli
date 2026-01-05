from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated

# importar serializers
from .serializers import [[ entity_name|capitalize_first ]]DTOSerializer

# importa las excepciones personalizadas
from .domain.[[ entity_name.lower() ]]_exceptions import (
    [[ entity_name|capitalize_first ]]ValueError,
    [[ entity_name|capitalize_first ]]ValidationError,
    [[ entity_name|capitalize_first ]]AlreadyExistsError,
    [[ entity_name|capitalize_first ]]NotFoundError,
    [[ entity_name|capitalize_first ]]OperationNotAllowedError,
    [[ entity_name|capitalize_first ]]PermissionError
)

# importa las excepciones de repositorio
from .infrastructure.exceptions import (
    ConnectionDataBaseError,
    RepositoryError
)

# importar servicios específicos del dominio
from [[ app_name.lower() ]].services.[[ entity_name.lower() ]]_service import [[ entity_name|capitalize_first ]]Service

class [[ entity_name|capitalize_first ]]ViewSet(ViewSet):
    """
    ViewSet para manejar operaciones CRUD relacionadas con [[ entity_name|decapitalize_first ]].
    
    Este ViewSet interactúa con:
    - Los servicios del dominio para manejar la lógica de negocio.
    - Los repositorios para acceder a la capa de persistencia.
    """

    # Serializer por defecto para documentación
    serializer_class = [[ entity_name|capitalize_first ]]DTOSerializer    

    # Definición de permisos y autenticación
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    # Definición de métodos HTTP permitidos
    # http_method_names = ['get', 'post', 'put', 'delete']


    @extend_schema(
        operation_id="[[ entity_name|decapitalize_first ]]_list",
        summary="Retrieve a list or a specific [[ entity_name|decapitalize_first ]]",
        description="Retrieve a list of all [[ entity_name|decapitalize_first ]] or a specific one by ID",
        responses={
            200: [[ entity_name|capitalize_first ]]DTOSerializer(many=True),
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["[[ entity_name|decapitalize_first ]]s"]
    )
    def list(self, request):
        """
        Endpoint para obtener una lista de todos los [[ entity_name|decapitalize_first ]].
        
        - Se valida y adapta la solicitud.
        - Se utiliza el servicio `list_[[ entity_name|decapitalize_first ]]` para manejar la lógica.
        """

        [[ entity_name|decapitalize_first ]]Service = [[ entity_name|capitalize_first ]]Service() # Instanciar el servicio

        try:
            # Llamar al servicio para recuperar todos los registros
            [[ entity_name|decapitalize_first ]]List = [[ entity_name|decapitalize_first ]]Service.list()

            # Serializar la lista de registros
            response_serializer_list = [[ entity_name|capitalize_first ]]DTOSerializer([[ entity_name|decapitalize_first ]]List, many=True)       

            # Retornar los datos serializados con un estado HTTP 200 OK
            return Response(response_serializer_list.data, status=status.HTTP_200_OK)

        except ([[ entity_name|capitalize_first ]]ValueError) as e:
            # Manejar errores de validación si los datos no son válidos
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="[[ entity_name|decapitalize_first ]]_retrieve",
        summary="Retrieve a specific [[ entity_name|decapitalize_first ]] by ID",
        description="Retrieve a specific [[ entity_name|decapitalize_first ]] by its ID",
        responses={
            200: [[ entity_name|capitalize_first ]]DTOSerializer,
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["[[ entity_name|decapitalize_first ]]s"]
    )
    def retrieve(self, request, pk: int = None):
        """
        Endpoint para obtener un [[ entity_name|decapitalize_first ]] específico por su ID (pk).
        
        - Valida y adapta la solicitud al dominio.
        - Utiliza el servicio `retrieve_[[ entity_name|decapitalize_first ]]` para manejar la lógica.
        """

        [[ entity_name|decapitalize_first ]]Service = [[ entity_name|capitalize_first ]]Service() # Instanciar el servicio

        try:
            # Llamar al servicio para recuperar un registro específico
            [[ entity_name|decapitalize_first ]] = [[ entity_name|decapitalize_first ]]Service.retrieve(entity_id=pk)

            # Serializar el registro recuperado
            response_serializer = [[ entity_name|capitalize_first ]]DTOSerializer([[ entity_name|decapitalize_first ]])        

            # Retornar el resultado con un estado HTTP 200 OK
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except [[ entity_name|capitalize_first ]]NotFoundError as e:
            # Manejar errores si no se encuentra el registro
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except [[ entity_name|capitalize_first ]]ValueError as e:
            # Manejar errores de validación si el ID no es válido
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="[[ entity_name|decapitalize_first ]]_create",
        summary="Create a new [[ entity_name|decapitalize_first ]]",
        description="Create a new [[ entity_name|decapitalize_first ]] with the provided data",
        request_body=[[ entity_name|capitalize_first ]]DTOSerializer,
        responses={
            201: [[ entity_name|capitalize_first ]]DTOSerializer,
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["[[ entity_name|decapitalize_first ]]s"]
    )
    def create(self, request):
        """
        Endpoint para crear un nuevo [[ entity_name|decapitalize_first ]].
        
        - Valida y adapta los datos entrantes.
        - Llama al servicio `create_[[ entity_name|decapitalize_first ]]` para manejar la creación.
        """
        
        # Datos enviados en el cuerpo de la solicitud
        serializer = [[ entity_name|capitalize_first ]]DTOSerializer(data=request.data)
        if not serializer.is_valid():
            # Si la validación falla, retornar un error 400 BAD REQUEST
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el ID de la entidad relacionada si existe
        external_id = request.data.get('external_id', None)

        # Si se proporcionan IDs de entidades relacionadas, agregarlos
        externals = request.data.get('externals', None)   
        
        [[ entity_name|decapitalize_first ]]Service = [[ entity_name|capitalize_first ]]Service() # Instanciar el servicio

        try:
            # Llamar al servicio para crear el registro
            [[ entity_name|decapitalize_first ]] = [[ entity_name|decapitalize_first ]]Service.create(data=serializer.validated_data, external_id=external_id, externals=externals)

            # Serializar el nuevo registro creado
            response_serializer = [[ entity_name|capitalize_first ]]DTOSerializer([[ entity_name|decapitalize_first ]])      

            # Retornar el resultado con un estado HTTP 201 CREATED
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except [[ entity_name|capitalize_first ]]AlreadyExistsError as e:
            # Manejar errores si ya existe un registro con el mismo nombre
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ([[ entity_name|capitalize_first ]]ValueError, [[ entity_name|capitalize_first ]]ValidationError) as e:
            # Manejar errores de validación si los datos no son válidos
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="[[ entity_name|decapitalize_first ]]_update",
        summary="Update an existing [[ entity_name|decapitalize_first ]]",
        description="Update an existing [[ entity_name|decapitalize_first ]] with the provided ID and data",
        request_body=[[ entity_name|capitalize_first ]]DTOSerializer,
        responses={
            200: [[ entity_name|capitalize_first ]]DTOSerializer,
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found")
        },
        tags=["[[ entity_name|decapitalize_first ]]s"]
    )
    def update(self, request, pk: int = None):
        """
        Endpoint para actualizar un [[ entity_name|decapitalize_first ]] existente.
        
        - Valida y adapta los datos entrantes.
        - Llama al servicio `update_[[ entity_name|decapitalize_first ]]` para manejar la actualización.
        """

        # Datos enviados en el cuerpo de la solicitud
        serializer = [[ entity_name|capitalize_first ]]DTOSerializer(data=request.data) 
        if not serializer.is_valid():
            # Si la validación falla, retornar un error 400 BAD REQUEST
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el ID de la entidad relacionada si existe
        external_id = request.data.get('external_id', None)

        # Si se proporcionan IDs de entidades relacionadas, agregarlos
        externals = request.data.get('externals', None)                  

        [[ entity_name|decapitalize_first ]]Service = [[ entity_name|capitalize_first ]]Service() # Instanciar el servicio

        try:
            # Llamar al servicio para actualizar el registro
            [[ entity_name|decapitalize_first ]] = [[ entity_name|decapitalize_first ]]Service.update(entity_id=pk, data=serializer.validated_data, external_id=external_id, externals=externals)

            # Serializar el registro actualizado
            response_serializer = [[ entity_name|capitalize_first ]]DTOSerializer([[ entity_name|decapitalize_first ]])          

            # Retornar el resultado con un estado HTTP 200 OK
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except [[ entity_name|capitalize_first ]]NotFoundError as e:
            # Manejar errores si no se encuentra el registro con el ID dado
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ([[ entity_name|capitalize_first ]]ValueError, [[ entity_name|capitalize_first ]]ValidationError) as e:
            # Manejar errores de validación si los datos no son válidos
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="[[ entity_name|decapitalize_first ]]_delete",
        summary="Delete an existing [[ entity_name|decapitalize_first ]]",
        description="Delete an existing [[ entity_name|decapitalize_first ]] with the provided ID",
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found")
        },
        tags=["[[ entity_name|decapitalize_first ]]s"]
    )
    def destroy(self, request, pk: int = None):
        """
        Endpoint para eliminar un [[ entity_name|decapitalize_first ]] existente.
        
        - Valida y adapta la solicitud.
        - Llama al servicio `delete_[[ entity_name|decapitalize_first ]]` para manejar la eliminación.
        """

        [[ entity_name|decapitalize_first ]]Service = [[ entity_name|capitalize_first ]]Service() # Instanciar el servicio

        try:
            # Llamar al servicio para eliminar el registro
            [[ entity_name|decapitalize_first ]] = [[ entity_name|decapitalize_first ]]Service.delete(entity_id=pk)

            # Retornar un estado HTTP 204 NO CONTENT para confirmar la eliminación
            return Response(status=status.HTTP_204_NO_CONTENT)

        except [[ entity_name|capitalize_first ]]NotFoundError as e:
            # Manejar errores si no se encuentra el registro con el ID dado
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ([[ entity_name|capitalize_first ]]ValueError, [[ entity_name|capitalize_first ]]ValidationError) as e:
            # Manejar errores de validación si el ID no es válido
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

