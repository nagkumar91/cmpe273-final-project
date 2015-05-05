from fabric.colors import red, green, cyan, magenta
from fabric.context_managers import cd, shell_env
from fabric.operations import run, sudo, local
from fabric.state import env

env.hosts = ["cmpe273.nagkumar.com"]
env.user = 'cmpe273'
dir_in_server = '/home/cmpe273/cmpe273-final-project/'


def deploy():
    print(cyan("Enter your git commit message"))
    msg = raw_input()
    local('git add .')
    local('git commit -am "%s"' % msg)
    print(green("Listing Branches"))
    local('git branch -a')
    print(cyan("Enter a branch name to push:"))
    branch = raw_input()
    local('git push origin %s' % branch)
    print(green("Deployment complete"))
    with cd(dir_in_server):
        print(magenta("Inside server"))
        run("git reset --hard || true", user=env.user)
        run("git pull", user=env.user)
        run("source /home/cmpe273/env/bin/activate && pip install -r requirements.txt", user=env.user)
        with shell_env(DJANGO_SETTINGS_MODULE='twitter_analytics.settings.production'):
            run("source /home/cmpe273/env/bin/activate && ./manage.py collectstatic --noinput", user=env.user)
            run("source /home/cmpe273/env/bin/activate && ./manage.py migrate --no-initial-data", user=env.user)
        sudo("service apache2 restart")
    print(green("Deployment complete"))
