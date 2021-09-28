#!/usr/bin/python3
import click
from netpingcli import *




search_folder = "/etc/"
prefix = "netping_"
commands = []
conf_file = "Configname"

#build right list with commands
for file in os.listdir(search_folder):
    if not file.startswith(prefix) or not os.path.isdir(search_folder + file):
        continue

    cmd_path = search_folder + file + "/commands"

    value = {}

    if os.path.exists(cmd_path) and os.path.isdir(cmd_path):
        value['name'] = file.replace(prefix, "")
        value['files'] = os.listdir(cmd_path)
        value['config'] = ""
        value['exec'] = False
        if os.path.exists(search_folder + file + "/" + conf_file):
            with open(search_folder + file + "/" + conf_file) as f:
                value['config'] = f.readline().strip()

        commands.append(value)

@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(list)
    ctx.obj = commands

for cmd in commands:
    cmd_name = cmd['name']
    cmd_config = cmd['config']

    @main.command(cmd_name, cls=PluginParser)
    def cmd_group():
        pass        

if __name__ == "__main__":
    main()
