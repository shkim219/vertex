import click
import test

@click.command()
@click.argument('filename', nargs=1, type=click.Path(exists=True))
def insert(filename):
    test.create_cell(filename)

if __name__ == '__main__':
    insert()
