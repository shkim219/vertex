import click
import shkim219.query
import shkim219.query2
import os

@click.command("kmeans")
def command():
    cd_back = os.system("cd ..")
    cd_back = os.system("cd ..")
    cd_install = os.system("wget https://mirrors.advancedhosters.com/apache//ignite/2.10.0/apache-ignite-2.10.0-bin.zip")
    cd_unzip = os.system("tar -xvf apache-ignite-2.10.0-bin.zip")
    cd_in = os.system("cd skopytest")
    cd_in = os.system("cd src")
    cd_in = os.system("cd main")
    cd_in = os.system("cd java")
    cd_in = os.system("cd kmeans")
    cd_compile = os.system("javac Client.java")
    cd_run = os.system("java Client")

if __name__ == '__main__':
    command()
