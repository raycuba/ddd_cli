from .utils import *

class CreateDTOCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser('create-dto', help='Crea un nuevo DTO')
        parser.add_argument('app_path', type=str, help='El path relativo de la app dentro del proyecto (por ejemplo, "apps/app1")')
        parser.add_argument('dto_name', type=str, help='El nombre del DTO')
        parser.add_argument(
            '--split', action='store_true', help='Crea un archivo separado para este DTO'
        )        
        parser.set_defaults(func=self.execute) 

    def execute(self, args):
        self.create_dto(args.app_path, args.dto_name, args.split)
        
    def create_dto(self, app_path, dto_name, split=False, **kwargs):
        """Crea un nuevo DTO"""
        dtos_dir = os.path.join(app_path, 'domain') if not split else os.path.join(app_path, 'domain', 'dtos')
        dtos_path = os.path.join(dtos_dir, 'dtos.py') if not split else os.path.join(dtos_dir, dto_name.lower() + '_dto.py')

        # Crear directorios si no existen
        try:
            os.makedirs(dtos_dir, exist_ok=True)

            # Crear archivos __init__.py
            create__init__files(dtos_dir)
        except OSError as e:
            print(f"No se pudo crear el directorio '{dtos_dir}': {e}")
            return
        
        #si split y ya existe el archivo mostrar error
        if split and os.path.exists(dtos_path):
            print(f"El archivo '{dtos_path}' ya existe. No se puede crear un archivo separado.")
            return

        # Escribir imports en el archivo 
        # si no existe el archivo template_imports
        if not os.path.exists(dtos_path):
            #renderizar imports
            rendered_content_imports = renderTemplate(templateName = 'dto', fileName='imports.txt', render_params={'dto_name':dto_name})

            # Escribir imports en el archivo
            with open(dtos_path, 'w') as f:
                f.write(rendered_content_imports + '\n')
            print(f"Imports of Dto '{dto_name}' created at {dtos_path}")

        #renderizar class
        rendered_content_class = renderTemplate(templateName = 'dto', fileName='class.txt', render_params={'dto_name':dto_name})

        # Escribir class en el archivo
        with open(dtos_path, 'a') as f:
            f.write('\n' + rendered_content_class + '\n')
        print(f"Class of Dto '{dto_name}' created at {dtos_path}")        