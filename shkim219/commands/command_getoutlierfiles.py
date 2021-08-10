import click
import shkim219.query2

@click.command("getoutlierfiles")
def command():
    print(shkim219.query2.getFiles())

if __name__ == '__main__':
    command()
