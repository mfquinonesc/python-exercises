import click
from generate_command import generate,g

@click.group()
def cli():
    pass 

cli.add_command(generate)
cli.add_command(g)

if __name__ == '__main__':
    cli()