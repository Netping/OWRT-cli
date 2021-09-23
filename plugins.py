import os
import click




search_folder = "/etc/"

class PluginParser(click.MultiCommand):
    def __scandir(self, work_dir, prefix):
        ret = []

        for file in os.listdir(work_dir):
            if not file.startswith(prefix) or not os.path.isdir(work_dir + file):
                continue

            ret.append(file)

        return ret

    def list_commands(self, ctx):
        rv = []

        #generate cmd folders dependent on plugin folders in other modules
        folders = self.__scandir(search_folder, "netping_")
        for folder in folders:
            try:
                cmd_folder = search_folder + folder + "/commands"
                for filename in os.listdir(cmd_folder):
                    if filename.endswith('.py') and filename.startswith('cmd_'):
                        rv.append(filename[4:-3])
            except:
                continue

        rv.sort()

        return rv

    def get_command(self, ctx, cmd_name):
        ns = {}
        #generate command search dependent on plugin folders
        folders = self.__scandir(search_folder, "netping_")
        for folder in folders:
            try:
                cmd_folder = search_folder + folder + "/commands"
                fn = os.path.join(cmd_folder, 'cmd_{}.py'.format(cmd_name))
                if os.path.exists(fn):
                    with open(fn) as f:
                        code = compile(f.read(), fn, 'exec')
                        eval(code, ns, ns)
            except:
                continue

        return ns['main']
        