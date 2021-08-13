import click
import shkim219.query
import shkim219.query2
import os

@click.command("randomForest")
@click.argument('filename', nargs=1, type=click.Path())
@click.argument('testname', nargs=1, type=click.Path())
def command(filename, testname):
    curpath = os.path.abspath(os.getcwd())
    cd_in = os.chdir("skopytest")
    # cd_execute = os.system("mvn exec:java -Dexec.mainClass=\"randomforest.Client\"")
    cd_execute = os.system("mvn exec:java -Dexec.mainClass=\"randomforest.Client\" -Dexec.arguments=\"" + filename + " " + testname + "\"")
    testname2 = testname[0:testname.index(".csv")] + "predicted.csv"
    shkim219.query2.create_cell(curpath + "/skopytest/" + testname2,"randomForest")
    

    

if __name__ == '__main__':
    command()
