import click
import test

@click.command()
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.option("--output", "-o", nargs=1, type=click.Path())
def retrieve(filename, output):
    test.createFile(filename, output)

if __name__ == '__main__':
    retrieve
