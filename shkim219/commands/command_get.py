import click
import shkim219.query

@click.command("get")
@click.argument('filename', nargs=1, type=click.Path())
def command(filename):
    retArray = shkim219.retrievecells(filename)
    for singleCell in retArray:
        print(singleCell)

if __name__ == '__main__':
    command()

