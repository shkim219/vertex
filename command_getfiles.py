import click
import test

@click.command()
def get_files():
    test.getFiles()

if __name__ == '__main__':
    get_files()
