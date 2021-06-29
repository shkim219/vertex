import click
import shkim219.query

@click.command("retrieve")
@click.argument('filename', nargs=1, type=click.Path)
@click.option("--output", "-o", nargs=1, type=click.Path())
def command(filename, output):
    shkim219.query.createFile(filename, output)

if __name__ == '__main__':
    command()
