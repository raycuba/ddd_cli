
from .utils import *

class CreateViewApiViewSetCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser('create-view-api-viewset', help='Crea una view para api basada en ViewSet')
        parser.add_argument('app_path', type=str, help='El path relativo de la app dentro del proyecto (por ejemplo, "apps/app1")')
        parser.add_argument('entity_name', type=str, help='El nombre de la entidad')  
        parser.set_defaults(func=self.execute)                  

    def execute(self, args):
        self.create_view_api_viewset(args.app_path, args.entity_name)

    def create_view_api_viewset(self, app_path, entity_name, **kwargs):
        """Crea una view para api basada en ApiViewSet"""
        views_dir = app_path
        views_path = os.path.join(views_dir, entity_name.lower() + '_views.py')

        # Crear directorios si no existen
        try:
            os.makedirs(views_dir, exist_ok=True)

            # Crear archivos __init__.py
            create__init__files(views_dir)
        except OSError as e:
            print(f"No se pudo crear el directorio '{views_dir}': {e}")
            return    
        
        #si ya existe el archivo mostrar error
        if os.path.exists(views_path):
            print(f"El archivo '{views_path}' ya existe.")
            return
        
        #convertir app_path (ej: apps/ap1) a app_name (ej: apps.app1)
        app_name = app_path.replace('/', '.').replace('\\', '.').replace('..', '.')

        #renderizar view
        rendered_content_class = renderTemplate(templateName = 'api', fileName='viewset_views.txt', render_params={'app_name':app_name, 'entity_name':entity_name})

        # Escribir class en el archivo
        with open(views_path, 'w') as f:
            f.write('\n' + rendered_content_class + '\n')
        print(f"Class View ApiViewSet of Entity '{entity_name}' created at {views_path}")