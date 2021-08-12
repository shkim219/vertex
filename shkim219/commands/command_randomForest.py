import click
import shkim219.query
import os

@click.command("randomForest")
@click.argument('filename', nargs=1, type=click.Path())
def command(filename):
    curpath = os.path.abspath(os.getcwd())
    cd_in = os.chdir("skopytest")
    # cd_execute = os.system("mvn exec:java -Dexec.mainClass=\"randomforest.Client\"")
    cd_execute = os.system("mvn exec:java -Dexec.mainClass=\"randomforest.Client\" -Dexec.arguments=\"" + filename + "\"")
    filename2 = filename[0:filename.index(".csv")] + "predicted.csv"
    shkim219.query2.create_cell(curpath + "/skopytest/" + filename2,"randomForest")
    

    

if __name__ == '__main__':
    command()
