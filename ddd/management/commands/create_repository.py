from .utils import *
from colorama import Fore, Style

class CreateRepositoryCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("create-repository", help='Create a new repository')
        parser.add_argument('app_path', type=str, help='The relative path of the app within the project (for example, "apps/app1")')
        parser.add_argument('entity_name', type=str, help='The name of the entity')
        parser.add_argument("--simulate", action="store_true", help="Simulate the creation of this entity without writing files")        
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        self.create_repository(args.app_path, args.entity_name, args.simulate)

    def create_repository(self, app_path, entity_name, simulate=False, **kwargs):
            """Crea un nuevo repositorio"""
            utils_dir = os.path.join(app_path, 'utils')
            repository_dir = os.path.join(app_path, 'infrastructure')
            repository_path = os.path.join(repository_dir, entity_name.lower() + '_repository.py')
            mappers_path = os.path.join(repository_dir, 'mappers.py')
            exceptions_path = os.path.join(repository_dir, 'exceptions.py')
            clean_dict_of_keys_path = os.path.join(utils_dir, 'clean_dict_of_keys.py')
            is_integer_path = os.path.join(utils_dir, 'is_integer.py')

            # decodficar app_path
            app_name, last_app_name, app_route, relative_app_path = decodeAppPath(app_path)

            if not simulate:
                # Crear directorios si no existen
                try:
                    os.makedirs(repository_dir, exist_ok=True)
                    create__init__files(repository_dir)
                    os.makedirs(utils_dir, exist_ok=True)
                    create__init__files(utils_dir)

                except OSError as e:
                    print(Fore.RED + f"Failed to create directory '{repository_dir}': {e}" + Style.RESET_ALL)
                    return    
            
                #si ya existe el archivo mostrar error
                if os.path.exists(repository_path):
                    print(Fore.RED + f"The file '{repository_path}' already exists" + Style.RESET_ALL)
                    return
            
            # Crear archivo de mappers.py        
            readWriteTemplate(templateName = 'repository', fileName='mappers.py', render_params={'entity_name':entity_name, 'app_name':app_name}, repository_path=mappers_path, failIfError=False, simulate=simulate)

            # Crear archivo de exceptions.py
            readWriteTemplate(templateName = 'repository', fileName='exceptions.py', render_params={}, repository_path=exceptions_path, failIfError=False, simulate=simulate)

            # Crear archivo clean_dict_of_keys.py
            readWriteTemplate(templateName = 'utils', fileName='clean_dict_of_keys.py', render_params={}, repository_path=clean_dict_of_keys_path, failIfError=False, simulate=simulate)

            # Crear archivo is_integer.py
            readWriteTemplate(templateName = 'utils', fileName='is_integer.py', render_params={}, repository_path=is_integer_path, failIfError=False, simulate=simulate)

            #renderizar class.py
            readWriteTemplate(templateName = 'repository', fileName='class.py', render_params={'entity_name':entity_name, 'app_name':app_name}, repository_path=repository_path, failIfError=True, simulate=simulate)
