import click
import shkim219.query

@click.command()
def get_files():
    print(shkim219.query.getFiles())

if __name__ == '__main__':
    get_files()
