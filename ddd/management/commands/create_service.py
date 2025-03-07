from .utils import *

class CreateServiceCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("create-service", help='Crea un nuevo servicio')
        parser.add_argument("app_path", type=str, help='El path relativo de la app dentro del proyecto (por ejemplo, "apps/app1")')
        parser.add_argument("service_name", type=str, help='El nombre del servicio')  
        parser.add_argument("entity_name", type=str, help='El nombre de la entidad')
        parser.add_argument("--class-format", action="store_true", help="Crea un archivo con formato de clase")
        parser.add_argument("--include-crud", action="store_true", help="Incluye métodos CRUD en el servicio")
        parser.add_argument("--split", action="store_true", help='Crea un archivo separado para este servicio')
        parser.set_defaults(func=self.execute)         

    def execute(self, args):
        self.create_service(args.app_path, args.service_name, args.entity_name, args.class_format, args.include_crud, args.split)

    def create_service(self, app_path, service_name, entity_name, class_format=False, include_crud=False, split=False, **kwargs):
        """Crea un nuevo servicio"""
        services_dir = os.path.join(app_path, 'domain') if not split else os.path.join(app_path, 'domain', 'services')
        services_path = os.path.join(services_dir, 'services.py') if not split else os.path.join(services_dir, service_name.lower() + '_service.py')

        # Crear directorios si no existen
        try:
            os.makedirs(services_dir, exist_ok=True)

            # Crear archivos __init__.py
            create__init__files(services_dir)
        except OSError as e:
            print(f"No se pudo crear el directorio '{services_dir}': {e}")
            return
        
        #si split y ya existe el archivo mostrar error
        if split and os.path.exists(services_path):
            print(f"El archivo '{services_path}' ya existe. No se puede crear un archivo separado.")
            return

        # Escribir imports en el archivo 
        # si no existe el archivo template_imports
        if not os.path.exists(services_path):
            #renderizar imports
            rendered_content_imports = renderTemplate(templateName = 'service', fileName='imports.txt', render_params={'service_name':service_name, 'entity_name':entity_name})

            # Escribir imports en el archivo
            with open(services_path, 'w') as f:
                f.write(rendered_content_imports + '\n')
            print(f"Imports of Service '{service_name}' created at {services_path}")

        if class_format:
            #renderizar class

            if include_crud:
                #renderizar class con crud
                rendered_content_class = renderTemplate(templateName = 'service', fileName='class_crud.txt', render_params={'service_name':service_name, 'entity_name':entity_name})

            else:
                #renderizar class
                rendered_content_class = renderTemplate(templateName = 'service', fileName='class.txt', render_params={'service_name':service_name, 'entity_name':entity_name})

        else:
            #renderizar funcion

            if include_crud:
                #renderizar funcion con crud
                rendered_content_class = renderTemplate(templateName = 'service', fileName='function_crud.txt', render_params={'service_name':service_name, 'entity_name':entity_name})

            else:
                #renderizar funcion
                rendered_content_class = renderTemplate(templateName = 'service', fileName='function.txt', render_params={'service_name':service_name, 'entity_name':entity_name})        

        # Escribir class en el archivo
        with open(services_path, 'a') as f:
            f.write('\n' + rendered_content_class + '\n')
        print(f"Class of Service '{service_name}' created at {services_path}")        