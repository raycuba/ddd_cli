import argparse
from ddd.management.commands.create_entity import CreateEntityCommand

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="CLI para soporte DDD en proyectos Python")
        self.subparsers = self.parser.add_subparsers(dest="subcommand", help="Subcomandos disponibles")

        # Registro de subcomandos
        CreateEntityCommand(self.subparsers)

    def run(self):
        args = self.parser.parse_args()
        if not args.subcommand:
            self.parser.print_help()
        else:
            # Ejecutar el subcomando seleccionado
            args.func(args)

if __name__ == "__main__":
    CLI().run()
