import os
import click




search_folder = "/etc/"

class PluginParser(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []

        for e in ctx.obj:
            if ctx.info_name == e['name']:
                for file in e['files']:
                    rv.append(file[4:-3])

        rv.sort()

        return rv

    def get_command(self, ctx, cmd_name):
        ns = {}

        #generate command search dependent on plugin folder
        for e in ctx.obj:
            if ctx.info_name == e['name']:
                for file in e['files']:
                    cmd_folder = search_folder + "netping_" + e['name'] + "/commands"
                    fn = os.path.join(cmd_folder, 'cmd_{}.py'.format(cmd_name))
                    if os.path.exists(fn):
                        with open(fn) as f:
                            code = compile(f.read(), fn, 'exec')
                            eval(code, ns, ns)

        return ns['main']  
