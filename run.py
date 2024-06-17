import json
import sys
import os
import os.path
import subprocess
import configparser

CONFIG_DIR = 'cfg/';

def open_json(file):
    with open(file, 'r') as f:
        return json.loads(f.read())

def open_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    result = {}
    if config.has_section('default'):
        for (key, value) in config['default'].items():
            result[key] = value
    for section in config.sections():
        if section != 'default':
            result[section] = dict(config[section])
    return result

def run_config_file(config_file):
    file = CONFIG_DIR + str(config_file)
    options = None
    if file.endswith('.ini') or file.endswith('.cfg'):
        options = open_config(file)
    elif file.endswith('.json'):
        options = open_json(file)
    else:
        try:
            if os.path.isfile(file):
                options = open_config(file)
            elif os.path.isfile(file + '.ini'):
                file = file + '.ini'
                options = open_config(file)
            elif os.path.isfile(file + '.cfg'):
                file = file + '.cfg'
                options = open_config(file)
        except configparser.Error:
            pass
        if options == None:
            file = str(config_file)
            if os.path.isfile(file):
                options = open_json(file)
            if os.path.isfile(file + '.json'):
                file = file + '.json'
                options = open_json(file)
    if options == None:
        raise Exception(f'File `{file}` not found')

    print(options)

    if 'dir' in options:
        os.chdir(options['dir'])

    if 'env' in options:
        for key, value in options['env'].items():
            os.environ[key] = str(value)

    script = str(options['run'])
    program = str(options['program']) if 'program' in options else 'node'
    arguments = options['arg'] if 'arg' in options else []
    if not (type(arguments) is list):
        if isinstance(arguments, str):
            arguments = arguments.split()
        else:
            arguments = [arguments]

    commands = [program, script, *(str(x) for x in arguments)]
    print(commands)
    subprocess.run(commands)

def run_config_or_script(file, args):
    run_file = f"run-{file}"
    if os.path.isfile(run_file):
        subprocess.run([run_file] + args)
    elif os.path.isfile(run_file + '.cmd'):
        subprocess.run([run_file + '.cmd'] + args)
    elif os.path.isfile(run_file + '.bat'):
        subprocess.run([run_file + '.bat'] + args)
    else:
        run_config_file(file)

def main():
    try:
        run_config_or_script(sys.argv[1], sys.argv[2:])
    except subprocess.CalledProcessError as e:
        print("Error:")
        print(e.stderr)

if __name__ == '__main__':
    main()
