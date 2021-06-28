import click
import shkim219.query

@click.command("delete")
@click.argument('filename', nargs=1, type=click.Path())
def command(filename):
    print(shkim219.query.delete(filename))

if __name__ == '__main__':
    command()
