from .utils import *

class CreateRepositoryCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("create-repository", help='Crea un nuevo repositorio')
        parser.add_argument('app_path', type=str, help='El path relativo de la app dentro del proyecto (por ejemplo, "apps/app1")')
        parser.add_argument('entity_name', type=str, help='El nombre de la entidad')
        parser.add_argument(
            '--include-crud', action='store_true', help='Incluye métodos CRUD en el repositorio'
        )
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        self.create_repository(args.app_path, args.entity_name, args.include_crud)

    def create_repository(self, app_path, entity_name, include_crud, **kwargs):
            """Crea un nuevo repositorio"""
            repository_dir = os.path.join(app_path, 'infrastructure')
            repository_path = os.path.join(repository_dir, entity_name.lower() + '_repository.py')

            app_name = app_path.replace('/', '.').replace('\\', '.').replace('..', '.')

            # Crear directorios si no existen
            try:
                os.makedirs(repository_dir, exist_ok=True)

                # Crear archivos __init__.py
                create__init__files(repository_dir)
            except OSError as e:
                print(f"No se pudo crear el directorio '{repository_dir}': {e}")
                return    
            
            #si ya existe el archivo mostrar error
            if os.path.exists(repository_path):
                print(f"El archivo '{repository_path}' ya existe.")
                return
            
            #renderizar class
            rendered_content_class = renderTemplate(templateName = 'repository', fileName='class.txt', render_params={'entity_name':entity_name, 'include_crud':include_crud, 'app_name':app_name})

            # Escribir class en el archivo
            with open(repository_path, 'w') as f:
                f.write('\n' + rendered_content_class + '\n')
            print(f"Class Repository of Entity '{entity_name}' created at {repository_path}")
