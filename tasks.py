# scp -r -P 14076 dist /srv/kairly/kairly-client
#
# ./manage.py collectstatic --settings='kairly.settings_prod'

from invoke import task, Collection

# Production
PY_HOST = 'app@node-13.rosti.cz'
PY_PORT = 14076

JS_HOST = 'app@node-13.rosti.cz'
JS_PORT = 14930


# It would be better compile app on server, but current plab
# is not sufficient (no enough RAM)

@task
def compile_js(ctx):
    print("Deleting previous nuxt build...")
    ctx.run("cd client && rm -rf .nuxt")
    print("Running nuxt build...")
    ctx.run("cd client && npm run build")


@task
def upload_js(ctx):
    print("Uploading nuxt build...")
    ctx.run("scp -r -P {} client/.nuxt {}:/tmp/.nuxt".format(JS_PORT, JS_HOST))


@task
def promote_js(ctx):
    print("Promoting nuxt build...")
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'cd /srv/kairly',
        'git pull',
        'cd /srv/app',
        'rm -rf /srv/kairly/client/.nuxt',
        'mv /tmp/.nuxt /srv/kairly/client/.nuxt',
        'cd /srv/app',
        "supervisorctl restart app",
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(JS_PORT, JS_HOST, ' && '.join(remote_commands)))


@task(compile_js, upload_js, promote_js)
def deploy_js(ctx):
    pass


@task
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
    ctx.run("ssh -T -p {} {} '{}'".format(PY_PORT, PY_HOST, ' && '.join(remote_commands)))


@task(compile_js, upload_js, deploy_py, promote_js)
def deploy_all(ctx):
    pass


@task()
def dump_prod(ctx):
    import os
    import sys
    server_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'kairly-server')
    sys.path.append(server_root)

    from kairly import settings_prod as settings
    dbconf = settings.DATABASES['default']
    tmp_file = '/tmp/kairly.sql.gz'

    dump_cmd = 'mysqldump --user="{}" --password="{}" -h {} --default-character-set=utf8mb4 {} | gzip > {}'.format(
        dbconf['USER'], dbconf['PASSWORD'], dbconf['HOST'], dbconf['NAME'], tmp_file
    )
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        dump_cmd
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PY_PORT, PY_HOST, ' && '.join(remote_commands)))
    ctx.run("scp -r -P {} {}:{} .".format(PY_PORT, PY_HOST, tmp_file))
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'rm ' + tmp_file
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PY_PORT, PY_HOST, ' && '.join(remote_commands)))
    # to import
    # Drop schema and recreate database with utf8mb4
    # CREATE SCHEMA `kairly` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci


deploy_ns = Collection('deploy')
deploy_ns.add_task(deploy_all, 'all', default=True)
deploy_ns.add_task(deploy_js, 'js')
deploy_ns.add_task(deploy_py, 'py')

dbdump_ns = Collection('dbdump')
dbdump_ns.add_task(dump_prod, 'prod')

ns = Collection()
ns.add_collection(deploy_ns)
ns.add_collection(dbdump_ns)
