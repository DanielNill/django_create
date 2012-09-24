import subprocess, os, sys, re
from random import choice
from git import *
from django_create import *

def main():
    #variable declarations
    starting_path = os.getcwd()
    templates_path = os.path.abspath(os.path.dirname(__file__)) + '/templates'
    project_name = sys.argv[1]

    create_virtualenv(project_name)
    create_django_project(project_name, starting_path)
    create_settings_file(project_name, starting_path, templates_path)
    create_secret_key()
    create_local_settings_file(project_name, templates_path)
    create_other_files(project_name, starting_path)
    create_git_repo(project_name, starting_path, templates_path)
    create_deploy_script(project_name, starting_path, templates_path)

def create_virtualenv(project_name):
    subprocess.call(['virtualenv', project_name])

def create_django_project(project_name, starting_path):
    os.chdir('/'.join([starting_path, project_name]))
    subprocess.call(['source', 'bin/activate'])
    subprocess.call(['bin/pip', 'install', 'django'])
    subprocess.call(['django-admin.py', 'startproject', project_name])

def create_settings_file(project_name, starting_path, templates_path):
    print 'Creating custom settings.py file'
    os.chdir(starting_path + '/' + project_name + '/' + project_name)
    settings_file = open('settings.py', 'w')
    settings_template = open(templates_path + '/settings.py')
    settings_file.write(settings_template.read().replace('{{ project_name }}', project_name))
    settings_file.close()

def create_secret_key():
    print'Creating secret key'
    settings_contents = open('settings.py', 'r').read()
    fp = open('settings.py', 'w')
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    settings_contents = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_contents)
    fp.write(settings_contents)
    fp.close()

def create_local_settings_file(project_name, templates_path):
    print 'Creating custom settings_local.py file'
    settings_local_file = open('settings_local.py', 'w')
    settings_local_template = open(templates_path + '/settings_local.py')
    settings_local_file.write(settings_local_template.read().replace('{{ project_name }}', project_name))
    settings_local_file.close()

def create_other_files(project_name, starting_path):
    print 'Creating Sublime Text project files'
    os.chdir(starting_path + '/' + project_name)
    sublimetext_project = open(project_name + '.sublime-project', 'w').write('{"folders": [{"path": "' + project_name + '"}]}')

def create_git_repo(project_name, starting_path, templates_path):
    repo = Repo.init(''.join([starting_path, '/', project_name, '/', project_name]))
    git_ignore = open(starting_path + '/' + project_name + '/' + project_name + '/.gitignore', 'w')
    git_ignore_contents = open(templates_path + '/.gitignore').read()
    git_ignore.write(git_ignore_contents)
    git_ignore.close()

def create_deploy_script(project_name, starting_path, templates_path):
    print 'Creating remote deploy script'
    os.chdir(starting_path + '/' + project_name + '/' + project_name)
    deploy_script = open('deploy.sh', 'w')
    deploy_contents = open(templates_path + '/deploy.sh', 'r').read().replace('{{ project_name }}', project_name)
    deploy_script.write(deploy_contents)
    deploy_script.close()
    subprocess.call('chmod 700 deploy.sh')

if __name__ == '__main__':
    main()
