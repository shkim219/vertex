import click
import shkim219.query2

@click.command("retrieveML")
@click.argument('filename', nargs=1, type=click.Path())
@click.argument('output', nargs=1, type=click.Path())
def command(filename, output):
    shkim219.query2.createFile(filename, output)

if __name__ == '__main__':
    command()