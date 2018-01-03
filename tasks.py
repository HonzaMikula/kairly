# scp -r -P 14076 dist /srv/kairly/kairly-client
#
# ./manage.py collectstatic --settings='kairly.settings_prod'

from invoke import task, Collection

# Production
HOST = 'app@alpha-node-6.rosti.cz'
PORT = 14076


# # QA
# HOST = 'app@alpha-node-2.rosti.cz'
# PORT = 11357
# CELERY = False


@task
def compile_js(ctx):
    print("Deleting previous webpack build...")
    ctx.run("cd kairly-client && rm -rf dist")
    print("Running webpack...")
    ctx.run("cd kairly-client && webpack --config build/webpack.prod.conf.js")


@task
def upload_js(ctx):
    ctx.run("scp -r -P {} kairly-client/dist {}:/tmp/dist".format(PORT, HOST))


@task(compile_js, upload_js)
def deploy_js(ctx):
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'rm -rf /srv/kairly/kairly-client/dist',
        'mv /tmp/dist /srv/kairly/kairly-client/dist',
        'cd /srv/app',
        "./manage.py collectstatic --noinput --settings='kairly.settings_prod'",
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PORT, HOST, ' && '.join(remote_commands)))


@task()
def deploy_py(ctx):
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'cd /srv/kairly',
        'git pull',
        'cd /srv/app',
        "./manage.py migrate --settings='kairly.settings_prod'",
        "./manage.py collectstatic --noinput --settings='kairly.settings_prod'",
        'supervisorctl restart app',
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PORT, HOST, ' && '.join(remote_commands)))


@task(compile_js, upload_js)
def deploy_all(ctx):
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'cd /srv/kairly',
        'git pull',
        'rm -rf /srv/kairly/kairly-client/dist',
        'mv /tmp/dist /srv/kairly/kairly-client/dist',
        'cd /srv/app',
        "./manage.py migrate --settings='kairly.settings_prod'",
        "./manage.py collectstatic --noinput --settings='kairly.settings_prod'",
        'supervisorctl restart app',
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PORT, HOST, ' && '.join(remote_commands)))


deploy_ns = Collection('deploy')
deploy_ns.add_task(deploy_all, 'all', default=True)
deploy_ns.add_task(deploy_js, 'js')
deploy_ns.add_task(deploy_py, 'py')

ns = Collection()
ns.add_collection(deploy_ns)
