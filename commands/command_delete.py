import click
import test

@click.command()
@click.argument('filename', nargs=1, type=click.Path(exists=True))
def delete(filename):
    test.delete(filename)

if __name__ == '__main__':
    delete()
