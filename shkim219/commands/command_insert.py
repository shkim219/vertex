import click
import shkim219.query

@click.command("insert")
@click.argument('filename', nargs=1, type=click.Path(exists=True))
def command(filename):
    shkim219.query.create_cell(filename)

if __name__ == '__main__':
    command()
