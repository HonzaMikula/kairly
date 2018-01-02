# scp -r -P 14076 dist /srv/kairly/kairly-client
#
# ./manage.py collectstatic --settings='kairly.settings_prod'

from invoke import task

# Production
HOST = 'app@alpha-node-6.rosti.cz'
PORT = 14076


# # QA
# HOST = 'app@alpha-node-2.rosti.cz'
# PORT = 11357
# CELERY = False


@task
def compile(ctx):
    ctx.run("cd kairly-client && rm -rf dist")
    ctx.run("cd kairly-client && webpack --config build/webpack.prod.conf.js")
    print("Webpack bundle created")


@task(compile)
def deploy(ctx):
    ctx.run("scp -r -P {} kairly-client/dist {}:/tmp/dist".format(PORT, HOST))
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'cd /srv/kairly',
        'git pull',
        'rm -rf /srv/kairly/kairly-client/dist'
        'mv /tmp/dist /srv/kairly/kairly-client/dist'
        'cd /srv/app',
        "./manage.py migrate --settings='kairly.settings_prod'",
        "./manage.py collectstatic --noinput --settings='kairly.settings_prod'",
        'supervisorctl restart app'
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PORT, HOST, ' && '.join(remote_commands)))
