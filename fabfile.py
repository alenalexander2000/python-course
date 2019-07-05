"""Fabfile for remote server deployment."""
import os
import json
import getpass
import keyring
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from fabric.api import (
    run, sudo, env, local, prompt, cd, task,
    hosts, put, warn_only, prefix,
    execute)
from fabric.colors import green, blue
from fabric.contrib import files


env.use_ssh_config = True

PROJECT_NAME = 'pythoncourse'
PROJECT_DIR = '$PROJECT_HOME/%s' % PROJECT_NAME
print 'PROJECT_DIR', PROJECT_DIR
PROJECT_GIT_DIR = '$PROJECT_HOME/%s/.git' % PROJECT_NAME
VIRUTLAL_ENV_DIR = '$WORKON_HOME/%s' % PROJECT_NAME

BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0'
BITBUCKET_REPOSITORY_OWNER = 'auditordesk'
PULL_REQUEST_URL = '%s/repositories/%s/uebt/pullrequests' % (
    BITBUCKET_API_BASE_URL, BITBUCKET_REPOSITORY_OWNER)

GIT_STASH_NO_CHANGE_MSG = 'No local changes to save'

DB_NAME = 'pythoncourse'
DB_USERNAME = 'pythoncourse'
DB_PASSWORD = 'pythoncourse'
DB_PACKAGES = [
    'postgresql', 'postgresql-contrib', 'postgresql-10.4-postgis-2.4.4',
    'libpq-dev']

SUPERVISOR_CONF_DIR = '/etc/supervisor/conf.d'
MONIT_CONF_DIR = '/etc/monit/conf.d'

DEVELOPMENT_HOST = '%s-dev' % PROJECT_NAME
PRODUCTION_HOST = '%s-prod' % PROJECT_NAME

HOST_SETTINGS = {
    DEVELOPMENT_HOST: {
        'branch': 'development',
        'environment': 'development',
    },
    PRODUCTION_HOST: {
        'branch': 'master',
        'environment': 'production',
    },
}


def deploy():
    """For deploying changes to remote."""
    branch = HOST_SETTINGS[env.host_string]['branch']
    environment = HOST_SETTINGS[env.host_string]['environment']

    with cd(PROJECT_DIR):
        print(green('Fetching from remote origin repository ...'))
        sudo('git checkout -f %s' % branch)
        sudo('git fetch origin')
        sudo('git merge origin/%s --ff-only' % branch)
    with prefix('workon %s' % PROJECT_NAME):
        print(green('Installing requirements ...'))
        sudo('pip install -r requirements/%s.txt' % environment)
    with prefix('workon %s' % PROJECT_NAME):
        print(green('Collecting static files ...'))
        sudo('python %s/manage.py collectstatic --noinput' % PROJECT_NAME)
    with prefix('workon %s' % PROJECT_NAME):
        print(green('Migrate database ...'))
        run('python %s/manage.py migrate' % PROJECT_NAME)
    sudo('supervisorctl update')
    sudo('service nginx restart')
    sudo('supervisorctl restart gunicorn')


def upload_file(local_path=None, remote_path=None, mode=0664):
    """For uploading file."""
    if local_path is None:
        local_path = prompt('Source file (relative path): ')
    if remote_path is None:
        remote_path = prompt('Destination file (with absolute path): ')

    put(
        local_path=local_path, remote_path=remote_path, use_sudo=True,
        mode=mode)


def install(package):
    """For installing packages."""
    print 'Installing %s' % package
    sudo('aptitude install -y %s' % package)


def install_essentials():
    """For setting up essentials for the environment."""
    install('python-dev')
    install('python-pip')
    install('git')


def setup_supervisor():
    """For setting up supervisor."""
    install('supervisor')


def setup_nginx():
    """For setting up ngnix."""
    install('nginx')


def setup_virtualenwrapper(environment):
    """For setting up virtual environment."""
    sudo('pip install virtualenvwrapper')
    upload_file(
        'configs/%s/virtualenvwrapper/bash_profile' % environment,
        '~/.bash_profile', 0664)
    run('source ~/.bash_profile')


def setup_db(environment):
    """For setting up database."""
    install(' '.join(DB_PACKAGES))
    create_user_cmd = 'CREATE USER %s WITH PASSWORD \'%s\';' % (
        DB_USERNAME, DB_PASSWORD)
    with warn_only():
        run('sudo -u postgres psql -c "%s"' % create_user_cmd)
        run('sudo -u postgres createdb -O %s %s' % (DB_USERNAME, DB_NAME))


def setup_project(environment):
    """For setting up the project in environment."""
    if not files.exists(PROJECT_DIR):
        sudo('mkproject %s' % PROJECT_NAME)

    if not files.exists(PROJECT_GIT_DIR):
        with cd(PROJECT_DIR):
            sudo('git clone https://sudeeshn@bitbucket.org/auditordesk/uebt.git .')
            sudo('git checkout %s' % HOST_SETTINGS[env.host_string]['branch'])

    upload_file(
        'configs/%s/virtualenvwrapper/postactivate' % environment,
        '%s/bin/postactivate' % VIRUTLAL_ENV_DIR, 0664)
    upload_file(
        'configs/%s/virtualenvwrapper/postdeactivate' % environment,
        '%s/bin/postdeactivate' % VIRUTLAL_ENV_DIR, 0664)

    with prefix('workon %s' % PROJECT_NAME):
        sudo('pip install -r requirements/%s.txt' % environment)
    with prefix('workon %s && cd %s' % (PROJECT_NAME, PROJECT_NAME)):
        sudo('python manage.py collectstatic --noinput')
        sudo('python manage.py migrate')
        create_superuser = prompt('Create superuser? [y/n] : ')
        if create_superuser.lower() in ['y', 'yes']:
            run('python manage.py createsuperuser')

    upload_file(
        'configs/%s/supervisor/conf.d/*.conf' % environment,
        '/etc/supervisor/conf.d/', 0600)
    sudo('supervisorctl update')

    upload_file(
        'configs/%s/nginx/%s' % (environment, PROJECT_NAME),
        '/etc/nginx/sites-available/%s' % PROJECT_NAME, 0600)
    sudo('ln -sf /etc/nginx/sites-available/%s /etc/nginx/sites-enabled' % (
        PROJECT_NAME))
    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('service nginx restart')


@task
def setup_server():
    """For setting up server in the needed environment."""
    print 'env.host_string', env

    environment = HOST_SETTINGS[env.host_string]['environment']
    sudo('apt-get update')
    install_essentials()
    setup_db(environment)
    setup_virtualenwrapper(environment)
    setup_nginx()
    setup_supervisor()
    setup_project(environment)
    print(blue('Successful!!'))


@hosts(DEVELOPMENT_HOST)
@task
def setup_development_server():
    """For setting up development server."""
    setup_server()


@hosts(PRODUCTION_HOST)
@task
def setup_production_server():
    """For setting up production server."""
    setup_server()


#  works
def get_bitbucket_credentials():
    """For getting bitbucket credentials from keyring."""
    credentials_file_path = os.path.expanduser('~/.bitbucketcredentials')
    try:
        with open(credentials_file_path, 'r') as credentials_file:
            credentials = json.loads(credentials_file.read())
    except (IOError, ValueError):
        username = prompt('Enter bitbucket username: ')
        password = getpass.getpass('Enter bitbucket password: ')
        namespace = prompt(
            'Enter namespace for bitbucket: ', default='bitbucket')

        credentials = {'username': username, 'namespace': namespace}
        with open(credentials_file_path, 'w') as credentials_file:
            credentials_file.write(json.dumps(credentials) + '\n')

        keyring.set_password(namespace, username, password)
    else:
        username = credentials['username']
        namespace = credentials['namespace']
        password = keyring.get_password(namespace, username)
    return HTTPBasicAuth(username, password)


def create_pr(destination_branch=None, title=None):
    """For creating pull request to the bitbucket repo."""
    current_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
    source_branch = prompt('Enter source branch:', default=current_branch)
    local('git push origin %s' % source_branch)

    if not destination_branch:
        destination_branch = prompt(
            'Enter destination branch:', default='development')
    if not title:
        title = prompt('Enter title for pull request:', default=current_branch)
    close_source_branch = prompt(
        'Close source branch? [y/n]: ', default='n').lower()
    close_source_branch = True if close_source_branch == 'y' else False

    print(blue('Creating pull request'))
    payload = {
        'title': title,
        'description': '',
        'source': {'branch': {'name': source_branch}},
        'destination': {'branch': {'name': destination_branch}},
        'close_source_branch': close_source_branch}
    credentials = get_bitbucket_credentials()
    response = requests.post(PULL_REQUEST_URL, json=payload, auth=credentials)

    response.raise_for_status()


@task
def create_pr_to_development():
    """For creating pull request to development branch."""
    create_pr('development')
    print(blue('Successful!!'))


def accept_pr(destination_branch=None):
    """For accepting pull request."""
    print(blue('Fetcing pull requests'))

    credentials = get_bitbucket_credentials()
    response = requests.get(PULL_REQUEST_URL, auth=credentials)

    response.raise_for_status()

    prs = response.json()['values']
    current_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
    source_branch = prompt('Enter source branch:', default=current_branch)
    if not destination_branch:
        destination_branch = prompt(
            'Enter destination branch:', default='development')

    accept_pr_url = None
    for pr in prs:
        pr_branch = pr['source']['branch']['name']
        pr_destination_branch = pr['destination']['branch']['name']
        if pr_branch == source_branch:
            if pr_destination_branch == destination_branch:
                accept_pr_url = pr['links']['merge']['href']
                break

    if not accept_pr_url:
        raise HTTPError('No matching pull request found')

    close_source_branch = pr['close_source_branch']

    print(blue('Accepting pull request'))
    response = requests.post(accept_pr_url, auth=credentials)

    response.raise_for_status()

    local('git fetch origin')
    no_stash = GIT_STASH_NO_CHANGE_MSG in local('git stash', capture=True)
    local('git checkout %s' % destination_branch)
    local('git merge origin/%s' % destination_branch)

    if close_source_branch and current_branch is source_branch:
        local('git checkout development')
    else:
        local('git checkout %s' % current_branch)
        if not no_stash:
            local('git stash pop')

    if close_source_branch:
        with warn_only():
            local('git branch -D %s' % source_branch)
        local('git push origin :%s' % source_branch)


@task
@hosts(DEVELOPMENT_HOST)
def accept_pr_to_development():
    """For accepting pull request to development branch."""
    accept_pr('development')
    deploy()
    print(blue('Successful!!'))


@task
@hosts(PRODUCTION_HOST)
def release():
    """For releasing the changes to the production server."""
    current_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)

    print(blue('Fetching from remote origin repository ...'))
    local('git fetch origin')
    local('git checkout development')
    local('git merge origin/development')
    local('git checkout master')
    local('git merge origin/master')
    local('git merge development')

    print(blue('Pushing master to remote origin repository ...'))
    local('git push origin master')
    deploy()

    local('git checkout %s' % current_branch)
    print(blue('Successful!!'))


@task
def create_hotfix():
    """For creating hot fix to the bugs founded."""
    name = prompt('Bug name :')
    local('git checkout master')
    local('git checkout -b hotfix-%s' % name)


def apply_hotfix_to_host(hotfix_branch):
    """Apply hotfix to host."""
    branch = HOST_SETTINGS[env.host_string]['branch']
    local('git checkout %s' % branch)
    local('git merge %s' % hotfix_branch)
    local('git push origin %s' % branch)
    deploy()
    local('git checkout %s' % hotfix_branch)


@task
def apply_hotfix():
    """For applying hotfix."""
    current_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)

    if 'hotfix' in current_branch:
        hotfix_branch = current_branch
    else:
        hotfix_branch = 'hotfix-' + prompt('Specify hotfix :')

    host_list = [PRODUCTION_HOST, DEVELOPMENT_HOST]
    execute(apply_hotfix_to_host, hotfix_branch, hosts=host_list)

    branches = local('git branch', capture=True)
    branches = [
        branch.replace('*', '').strip() for branch in branches.split('\n')]
    branches.remove('master')
    branches.remove('development')
    for branch in branches:
        local('git checkout %s' % branch)
        local('git merge %s' % hotfix_branch)

    if hotfix_branch is current_branch:
        local('git checkout development')
    else:
        local('git checkout %s' % current_branch)

    local('git branch -d %s' % hotfix_branch)
    print(blue('Successful!!'))


@task
@hosts(PRODUCTION_HOST)
def backup_production_db():
    """For backing up production db to local."""
    print(green('Creating db dump ...'))
    run('sudo -u postgres pg_dump -Fc %s > ~/db.dump' % DB_NAME)
    print(blue('Fetching dump from remote to local ..'))
    local('scp %s:~/db.dump .' % PRODUCTION_HOST)
    sudo('rm -rf ~/db.dump')
    db_user = prompt(
        'Enter local posgresql superuser: ', default='postgres')
    db_name = '%s_prod' % PROJECT_NAME
    with warn_only():
        local('sudo -u %s dropdb %s' % (db_user, db_name))
    local('sudo -u %s createdb -O %s %s' % (db_user, DB_USERNAME, db_name))
    revoke_cmd = 'REVOKE CONNECT ON DATABASE %s FROM PUBLIC' % db_name
    local('sudo -u %s psql -c "%s"' % (db_user, revoke_cmd))
    with warn_only():
        local('sudo -u %s pg_restore -d %s db.dump' % (db_user, db_name))
    local('rm db.dump')
    print(blue('Successful!!'))


@task
@hosts(DEVELOPMENT_HOST)
def backup_development_db():
    """For backing up development db to local."""
    print(green('Creating db dump ...'))
    run('sudo -u postgres pg_dump -Fc %s > ~/db.dump' % DB_NAME)
    print(blue('Fetching dump from remote to local ..'))
    local('scp %s:~/db.dump .' % DEVELOPMENT_HOST)
    sudo('rm -rf ~/db.dump')
    db_user = prompt(
        'Enter local posgresql superuser: ', default='postgres')
    db_name = '%s_dev' % PROJECT_NAME
    with warn_only():
        local('sudo -u %s dropdb %s' % (db_user, db_name))
    local('sudo -u %s createdb -O %s %s' % (db_user, DB_USERNAME, db_name))
    revoke_cmd = 'REVOKE CONNECT ON DATABASE %s FROM PUBLIC' % db_name
    local('sudo -u %s psql -c "%s"' % (db_user, revoke_cmd))
    with warn_only():
        local('sudo -u %s pg_restore -d %s db.dump' % (db_user, db_name))
    local('rm db.dump')
    print(blue('Successful!!'))



#sudo -u postgres dropdb pythoncourse
#sudo service postgresql restart
#sudo -u postgres createdb -O pythoncourse pythoncourse
#sudo -u postgres pg_restore -d pythoncourse localdb/uebtlocal
