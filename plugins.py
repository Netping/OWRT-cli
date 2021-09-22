import os
import click




cmd_folder = "/root/"

class PluginParser(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []

        #TODO generate cmd folders dependent on plugin folders in other modules
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])

        rv.sort()

        return rv

    def get_command(self, ctx, cmd_name):
        ns = {}
        #TODO generate command search dependent on plugin folders
        fn = os.path.join(cmd_folder, 'cmd_{}.py'.format(cmd_name))

        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)

        return ns['cli']