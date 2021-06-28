import click
import shkim219.query

@click.command("getfiles")
def command():
    print(shkim219.query.getFiles())

if __name__ == '__main__':
    command()
