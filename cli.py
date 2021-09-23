#!/usr/bin/python3
import click
from plugins import PluginParser




#TODO generate options from file
#@click.command(cls=PluginParser)
#def main():
#	pass
cli = PluginParser()

if __name__ == "__main__":
    #main()
    cli()
