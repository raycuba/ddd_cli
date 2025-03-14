from .utils import *
from colorama import Fore, Style

class CreateViewCommand:
    def __init__(self, subparsers):      
        parser = subparsers.add_parser('create-view', help='Create a view for web')
        parser.add_argument('app_path', type=str, help='The relative path of the app within the project (for example, "apps/app1")')
        parser.add_argument('entity_name', type=str, help='The name of the entity')        
        parser.set_defaults(func=self.execute)           

    def execute(self, args):
        self.create_view(args.app_path, args.entity_name)

    def create_view(self, app_path, entity_name, **kwargs):
        """Crea una view para web"""
        views_dir = app_path
        views_templates_dir = os.path.join(views_dir, 'templates')

        views_path = os.path.join(views_dir, entity_name.lower() + '_views.py')
        forms_path = os.path.join(views_dir, entity_name.lower() + '_forms.py')

        # Crear directorios si no existen
        try:
            os.makedirs(views_dir, exist_ok=True)
            os.makedirs(views_templates_dir, exist_ok=True)

            # Crear archivos __init__.py
            create__init__files(views_dir)
        except OSError as e:
            print(Fore.RED + f"Failed to create directory '{views_dir}': {e}" + Style.RESET_ALL)
            return    
        
        #si ya existe el archivo view mostrar error
        if os.path.exists(views_path):
            print(Fore.RED + f"The file '{views_path}' already exists." + Style.RESET_ALL)
            return
        
        #si ya existe el archivo form mostrar error
        if os.path.exists(forms_path):
            print(Fore.RED + f"The file '{forms_path}' already exists." + Style.RESET_ALL)
            return
        
        web_test_path = os.path.join(views_templates_dir, 'web_test_' + entity_name.lower() + '.html')
        web_create_register_path = os.path.join(views_templates_dir, 'web_create_' + entity_name.lower() + '.html')
        web_edit_register_path = os.path.join(views_templates_dir, 'web_edit_' + entity_name.lower() + '.html')
        web_edit_save_register_path = os.path.join(views_templates_dir, 'web_edit_save_' + entity_name.lower() + '.html')
        web_list_registers_path = os.path.join(views_templates_dir, 'web_list_' + entity_name.lower() + '.html')
        web_view_register_path = os.path.join(views_templates_dir, 'web_view_' + entity_name.lower() + '.html')        
        
        #si ya existe el archivo web_create_register mostrar error
        if os.path.exists(web_create_register_path):
            print(Fore.RED + f"The file '{web_create_register_path}' already exists." + Style.RESET_ALL)
            return  

        #si ya existe el archivo web_edit_register mostrar error
        if os.path.exists(web_edit_register_path):
            print(Fore.RED + f"The file '{web_edit_register_path}' already exists." + Style.RESET_ALL)
            return

        #si ya existe el archivo web_edit_save_register mostrar error
        if os.path.exists(web_edit_save_register_path):
            print(Fore.RED + f"The file '{web_edit_save_register_path}' already exists." + Style.RESET_ALL)
            return

        #si ya existe el archivo web_list_registers mostrar error
        if os.path.exists(web_list_registers_path):
            print(Fore.RED + f"The file '{web_list_registers_path}' already exists." + Style.RESET_ALL)
            return

        #si ya existe el archivo web_view_register mostrar error
        if os.path.exists(web_view_register_path):
            print(Fore.RED + f"The file '{web_view_register_path}' already exists." + Style.RESET_ALL)
            return                                      
        
        #convertir app_path (ej: apps/ap1) a app_name (ej: apps.app1)
        app_name = app_path.replace('/', '.').replace('\\', '.').replace('..', '.')

        #renderizar views
        rendered_content_class = renderTemplate(templateName = 'view', fileName='web_views.py', render_params={'app_name':app_name, 'entity_name':entity_name})
        # Escribir views en el archivo
        with open(views_path, 'w') as f:
            f.write('\n' + rendered_content_class + '\n')
        print(f"Class View of Entity '{entity_name}' created at {views_path}")

        #renderizar forms
        rendered_content_forms = renderTemplate(templateName = 'view', fileName='web_forms.py', render_params={'entity_name':entity_name})
        # Escribir forms en el archivo
        with open(forms_path, 'w') as f:
            f.write('\n' + rendered_content_forms + '\n')
        print(f"Class Form of Entity '{entity_name}' created at {forms_path}")

        #renderizar templates
        readWriteTemplate(templateName='templates', fileName='web_create_register.html',  render_params={}, repository_path=web_create_register_path, failIfError=True)
        print(f"Template web_create of Entity '{entity_name}' created at {web_create_register_path}")

        readWriteTemplate(templateName='templates', fileName='web_edit_register.html',  render_params={'entity_name':entity_name}, repository_path=web_edit_register_path, failIfError=True)
        print(f"Template web_edit of Entity '{entity_name}' created at {web_edit_register_path}")

        readWriteTemplate(templateName='templates', fileName='web_edit_save_register.html',  render_params={'entity_name':entity_name}, repository_path=web_edit_save_register_path, failIfError=True)
        print(f"Template web_edit_save of Entity '{entity_name}' created at {web_edit_save_register_path}")

        readWriteTemplate(templateName='templates', fileName='web_list_registers.html',  render_params={'entity_name':entity_name}, repository_path=web_list_registers_path, failIfError=True)
        print(f"Template web_list of Entity '{entity_name}' created at {web_list_registers_path}")

        readWriteTemplate(templateName='templates', fileName='web_view_register.html',  render_params={'entity_name':entity_name}, repository_path=web_view_register_path, failIfError=True)
        print(f"Template web_view of Entity '{entity_name}' created at {web_view_register_path}")

