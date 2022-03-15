#!/usr/bin/python3
import click
import json
from netpingcli import *




search_folder = "/etc/netping/"
#prefix = "netping_"
commands = []
conf_file = "Configname"
help_file = "Help"
types_file = "Types"

#build right list with commands
for file in os.listdir(search_folder):
    if not os.path.isdir(search_folder + file):
        continue

    cmd_path = search_folder + file + "/commands"

    value = {}

    if os.path.exists(cmd_path) and os.path.isdir(cmd_path):
        value['name'] = file
        value['files'] = os.listdir(cmd_path)
        value['config'] = ""
        value['exec'] = False
        value['help'] = ''
        value['types'] = {}

        if os.path.exists(search_folder + file + "/" + conf_file):
            with open(search_folder + file + "/" + conf_file) as f:
                value['config'] = f.readline().strip()

        if os.path.exists(search_folder + file + "/" + help_file):
            with open(search_folder + file + "/" + help_file) as f:
                value['help'] = f.read()

        if os.path.exists(search_folder + file + "/" + types_file):
            with open(search_folder + file + "/" + types_file) as json_file:
                data = json.load(json_file)
                value['types'] = data

        commands.append(value)

@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(list)
    ctx.obj = commands

for cmd in commands:
    @main.command(cmd['name'], cls=PluginParser, help=cmd['help'])
    def cmd_group():
        pass        

if __name__ == "__main__":
    main()
