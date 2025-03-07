from .utils import *
from colorama import Fore, Style

class CreateEntityCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("create-entity", help="Create a new entity")
        parser.add_argument("app_path", type=str, help='The relative path of the app within the project (for example, "apps/app1")')
        parser.add_argument("entity_name", type=str, help="The name of the entity")
        parser.add_argument("--split", action="store_true", help="Create a separate file for this entity")
        parser.set_defaults(func=self.execute)     

    def execute(self, args):
        self.create_entity(args.app_path, args.entity_name, args.split)

    def create_entity(self, app_path, entity_name, split=False, **kwargs):
        """Crea una nueva entidad"""
        entities_dir = os.path.join(app_path, 'domain') if not split else os.path.join(app_path, 'domain', 'entities')
        entities_path = os.path.join(entities_dir, 'entities.py') if not split else os.path.join(entities_dir, entity_name.lower() + '_entity.py')

        # Crear directorios si no existen
        try:
            os.makedirs(entities_dir, exist_ok=True)
            
            # Crear archivos __init__.py
            create__init__files(entities_dir)
        except OSError as e:
            print(Fore.RED + f"Failed to create directory '{entities_dir}': {e}" + Style.RESET_ALL)
            return
        
        #si split y ya existe el archivo mostrar error
        if split and os.path.exists(entities_path):
            print(Fore.RED + f"File '{entities_path}' already exists. Cannot create separate file." + Style.RESET_ALL)
            return

        # Escribir imports en el archivo 
        # si no existe el archivo template_imports
        if not os.path.exists(entities_path):
            #renderizar imports
            rendered_content_imports = renderTemplate(templateName = 'entity', fileName='imports.txt', render_params={'entity_name':entity_name})

            # Escribir imports en el archivo
            with open(entities_path, 'w') as f:
                f.write(rendered_content_imports + '\n')
            print(f"Imports of Entity '{entity_name}' created at {entities_path}")

        #renderizar class
        rendered_content_class = renderTemplate(templateName = 'entity', fileName='class.txt', render_params={'entity_name':entity_name})

        # Escribir class en el archivo
        with open(entities_path, 'a') as f:
            f.write('\n' + rendered_content_class + '\n')
        print(f"Class of Entity '{entity_name}' created at {entities_path}")            
