import click
import shkim219.query
import shkim219.query2
import os

@click.command("kmeans")
@click.argument('filename', nargs=1, type=click.Path())
def command(filename):
    curpath = os.path.abspath(os.getcwd())
    print(curpath)
    cd_in = os.system("cd " + curpath + "\\vertex\\skopytest")
    cd_execute = os.system("mvn exec:java -Dexec.mainclass=\"kmeans.Client\" -Dexec.args=\"" + filename + " " + curpath + "\\vertex\\shkim219\\query\\__init__.py\"")
    shkim219.query2.create_cell(curpath + "\\vertex\\skopytest\\" + filename[0,filename.index(".csv")],"kmeans")
    

    

if __name__ == '__main__':
    command()
