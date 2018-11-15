import click

with click.progressbar(range(100000)) as bar:
    for i in bar:
        pass 
