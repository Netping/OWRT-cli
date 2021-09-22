#!/usr/bin/python3
import click
from plugins import PluginParser




#TODO generate options from file
@click.command(cls=PluginParser)
def main():
	pass

if __name__ == "__main__":
    main()
