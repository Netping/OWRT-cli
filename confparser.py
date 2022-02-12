import click
import sys
import ubus
import os




@click.group()
def main():
    """Setting parameters to UCI config"""
    pass

@main.command()
@click.pass_context
def show(ctx):
    """Show parameters of UCI config"""

    element = None
    for e in ctx.obj:
        if e['exec']:
            element = e
            break

    #ubus calling to config
    try:
        ubus.connect()
    except:
        print("Can't connect to ubus")

    confvalues = ubus.call("uci", "get", {"config": element['config']})
    for confdict in list(confvalues[0]['values'].values()):
        print("Section \"" + confdict['.name'] + "\":")
        for key, value in confdict.items():
            if type(value) == list:
                for v in value:
                    print("\t" + v)
                continue

            if not key.startswith('.'):
                print("\t" + key + ": " + value)

        print('\n')

    ubus.disconnect()

@main.command()
@click.argument('section', required=True)
@click.argument('option', required=True)
@click.argument('value', required=True)
@click.pass_context
def set(ctx, section, option, value):
    """Setting parameters to UCI config\n
    SECTION - section name in UCI config\n
    OPTION - option name of section in UCI config\n
    VALUE - value for option of section in UCI config\n
    """

    element = None
    for e in ctx.obj:
        if e['exec']:
            element = e
            break

    try:
        ubus.connect()

        ubus.call("uci", "set", {"config" : element['config'], "section" : section, "values" : { option : value }})
        ubus.call("uci", "commit", {"config" : element['config']})

        #send commit signal
        ubus.send("commit", {"config" : element['config']})

        ubus.disconnect()
    except:
        print("Can't set parameter")

@main.command()
@click.argument('sectiontype', required=True)
@click.argument('sectionname', required=False)
@click.pass_context
def addsection(ctx, sectionname, sectiontype):
    """Add new section to UCI config\n
    SECTIONNAME - section name in UCI config\n
    SECTIONTYPE - type of section\n
    """
    element = None
    for e in ctx.obj:
        if e['exec']:
            element = e
            break

    #via os because ubus doesn't work
    if sectionname:
        os.system("uci set " + element['config'] + "." + sectionname + "='" + sectiontype + "'")
    else:
        os.system("uci add " + element['config'] + " " + sectiontype)
    os.system("uci commit " + element['config'])

    #send commit signal
    try:
        ubus.connect()
        ubus.send("commit", {"config" : element['config']})
        ubus.disconnect()
    except:
        pass

@main.command()
@click.argument('section', required=True)
@click.argument('option', required=False)
@click.pass_context
def delete(ctx, section, option):
    """Delete parameters from UCI config\n
    SECTION - section name in UCI config\n
    OPTION - option name of section in UCI config\n
    """
    element = None
    for e in ctx.obj:
        if e['exec']:
            element = e
            break

    try:
        ubus.connect()

        if option:
            ubus.call("uci", "delete", {"config" : element['config'], "section" : section, "option" : option})
        else:
            ubus.call("uci", "delete", {"config" : element['config'], "section" : section})

        ubus.call("uci", "commit", {"config" : element['config']})
        #send commit signal
        ubus.send("commit", {"config" : element['config']})

        ubus.disconnect()
    except:
        print("Can't delete component")
