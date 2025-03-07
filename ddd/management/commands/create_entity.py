from utils import *

class CreateEntityCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser("create-entity", help="Crea una nueva entidad")
        parser.add_argument("app_path", type=str, help='El path relativo de la app dentro del proyecto. Por ejemplo, "apps/app1"')
        parser.add_argument("entity_name", type=str, help="El nombre de la entidad")
        parser.add_argument("--split", action="store_true", help="Crea un archivo separado para esta entidad")
        parser.set_defaults(func=self.execute)     

    def execute(self, args):
        print(f"Creando entidad '{args.entity_name}' en '{args.app_path}'")
        if args.split:
            print("Creando la entidad en un archivo separado...")
