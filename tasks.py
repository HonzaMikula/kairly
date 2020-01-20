# scp -r -P 14076 dist /srv/kairly/kairly-client
#
# ./manage.py collectstatic --settings='kairly.settings_prod'

from invoke import task, Collection

# Production
PY_HOST = 'app@node-13.rosti.cz'
PY_PORT = 14076

CRON_HOST = 'app@node-14.rosti.cz'
CRON_PORT = 15218

JS_HOST = 'app@node-13.rosti.cz'
JS_PORT = 14930


# It would be better compile app on server, but current plab
# is not sufficient (no enough RAM)

@task
def compile_js(ctx):
    print("Deleting previous nuxt build...")
    ctx.run("cd client && rm -rf .nuxt")
    print("Compiling messages...")
    ctx.run("cd client && npm run compilemessages")
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
        'git fetch',
        'git checkout production',
        'cd /srv/app',
        'rm -rf /srv/kairly/client/.nuxt',
        'mv /tmp/.nuxt /srv/kairly/client/.nuxt',
        'cd /srv/app',
        'npm install',
        'git reset --hard',  # reset package-lock.json back, workaround to unsupported npm ci
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
        'git fetch',
        'git checkout production',
        'cd /srv/app',
        "./manage.py migrate --settings='kairly.settings_prod'",
        "./manage.py collectstatic --noinput --settings='kairly.settings_prod'",
        'supervisorctl restart app',
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(PY_PORT, PY_HOST, ' && '.join(remote_commands)))


@task(compile_js, upload_js, deploy_py, promote_js)
def deploy_app(ctx):
    pass


@task
def deploy_cron(ctx):
    remote_commands = [
        'export TERM=xterm',
        'source /srv/.bashrc',
        'cd /srv/kairly',
        'git fetch',
        'git checkout production',
        'cp /srv/kairly/server/cron/crontab /srv/conf',
        'crontab /srv/conf/crontab'
    ]
    ctx.run("ssh -T -p {} {} '{}'".format(CRON_PORT, CRON_HOST, ' && '.join(remote_commands)))


@task()
def dbdump_prod(ctx):
    import os
    import sys
    server_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server')
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
    # ctx.run("gunzip kairly.sql.gz")
    # to import
    # Drop schema and recreate database with utf8mb4
    # CREATE SCHEMA `kairly` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci


@task()
def dbdump_import(ctx):
    print("Removing kairly schema...")
    ctx.run('mysql -h 127.0.0.1 -u root -e "DROP SCHEMA IF EXISTS kairly"')
    print("Recreating kairly schema...")
    ctx.run('mysql -h 127.0.0.1 -u root -e "CREATE SCHEMA kairly DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"')
    print("Importing db dump...")
    ctx.run('zcat kairly.sql.gz | mysql -h 127.0.0.1 -u root --default-character-set=utf8mb4 kairly')


@task()
def download_media(ctx):
    ctx.run("rsync -chavzP -e 'ssh -p {}' --stats {}:/srv/app/media server".format(PY_PORT, PY_HOST))


deploy_ns = Collection('deploy')
deploy_ns.add_task(deploy_app, 'app', default=True)
deploy_ns.add_task(deploy_js, 'js')
deploy_ns.add_task(deploy_py, 'py')
deploy_ns.add_task(deploy_cron, 'cron')

dbdump_ns = Collection('dbdump')
dbdump_ns.add_task(dbdump_prod, 'prod')
dbdump_ns.add_task(dbdump_import, 'import')

ns = Collection()
ns.add_collection(deploy_ns)
ns.add_collection(dbdump_ns)
ns.add_task(download_media)
