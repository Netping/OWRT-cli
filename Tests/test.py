#!/usr/bin/python3
import ubus
import os
import time
import subprocess

# config
config = "testconf"
config_path = "/etc/config/"

# ash cli comand
ashcmd = 'netping'
section = 'info'
section_name = 'testsection'
option_name = 'name'

def test_install():
    ret = False

    res = os.system(f"{ashcmd}")
    assert res == 0

def test_commands():
    ret = False

    # get first command (module) to test commands
    p = subprocess.Popen('netping', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = p.stdout.readline()
        if not line:
            print('No module to test commands')
            break
        if line == b'Commands:\n':
            break
    module = p.stdout.readline()
    if module:
        module = module.decode("utf-8").strip().split(' ')[0]

        try:
            res = os.system(f"{ashcmd} {module} config addsection {section} {section_name}")
            assert res == 0

            res = os.system(ashcmd + ' ' + module + ' config set ' + section_name + ' \'{"name": "testname"}\'')
            assert res == 0

            res = os.system(f"{ashcmd} {module} config delete {section_name} {option_name}")
            assert res == 0

            res = os.system(f"{ashcmd} {module} config delete {section_name}")
            assert res == 0

        except:
            assert ret

    else:
        print('No module to test commands')
