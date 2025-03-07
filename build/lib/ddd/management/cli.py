import argparse
from ddd.management.commands.create_entity import CreateEntityCommand
from ddd.management.commands.create_service import CreateServiceCommand
from ddd.management.commands.create_repository import CreateRepositoryCommand
from ddd.management.commands.create_dto import CreateDTOCommand
from ddd.management.commands.create_view_api_apiview import CreateViewApiApiViewCommand
from ddd.management.commands.create_view_api_viewset import CreateViewApiViewSetCommand
from ddd.management.commands.create_view import CreateViewCommand

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="CLI para soporte DDD en proyectos Python/Django")
        self.subparsers = self.parser.add_subparsers(dest="subcommand", help="Subcomandos disponibles")

        # Registro de subcomandos
        CreateEntityCommand(self.subparsers)
        CreateServiceCommand(self.subparsers)
        CreateRepositoryCommand(self.subparsers)
        CreateDTOCommand(self.subparsers)
        CreateViewApiApiViewCommand(self.subparsers)
        CreateViewApiViewSetCommand(self.subparsers)
        CreateViewCommand(self.subparsers)

    def run(self):
        args = self.parser.parse_args()
        if not args.subcommand:
            self.parser.print_help()
        else:
            # Ejecutar el subcomando seleccionado
            args.func(args)

def main():
    CLI().run()            

if __name__ == "__main__":
    main()
