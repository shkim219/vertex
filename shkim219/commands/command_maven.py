import click
import shkim219.query
import os

@click.command("maven")
def command():
    cd_back = os.system("cd ..")
    cd_back = os.system("cd ..")
    cd_install = os.system("wget https://mirrors.advancedhosters.com/apache//ignite/2.10.0/apache-ignite-2.10.0-bin.zip")
    cd_unzip = os.system("unzip apache-ignite-2.10.0-bin.zip")
    curpath = os.path.abspath(os.getcwd())
    cd_in = os.system("cd " + curpath + "\\vertex\\skopytest")
    cd_install = os.system("mvn install")
    cd_compile = os.system("mvn compile")
    
    