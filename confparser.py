import click
import sys
import ubus
import os
import json




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
@click.argument('values', required=True)
@click.pass_context
#def set(ctx, section, option, value):
def set(ctx, section, values):
    """Setting parameters to UCI config\n
    SECTION - section name in UCI config\n
    VALUES - json object with parameters like in section with name SECTION
    """

    values = json.loads(values)

    element = None
    for e in ctx.obj:
        if e['exec']:
            element = e
            break

    try:
        ubus.connect()

        #validate values
        if element['types']:
            data = element['types']
            for e in data:
                if e['section_name'] == section:
                    for key, value in values.items():
                        option = key
                        types = e['types']

                        result = ubus.call("input", "validate", { "value" : value, "lang" : "en", "datatype" : types[option] })
                        result = result[0]

                        if 'error' in list(result.keys()):
                            ubus.disconnect()
                            raise ValueError("Valid checking error: " + result['error'])
                        
                    break
            
        ubus.call("uci", "set", { "config" : element['config'], "section" : section, "values" : values })
        ubus.call("uci", "commit", { "config" : element['config'] })

        #send commit signal
        ubus.send("commit", {"config" : element['config']})

        ubus.disconnect()
    except Exception as ex:
        print("Can't set parameter")
        print(str(ex))

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
