from arctasks import *


@arctask(configured='dev', timed=True)
def init(ctx, overwrite=False, drop_db=False):
    npm_install(ctx)
    virtualenv(ctx, overwrite=overwrite)
    install(ctx)
    createdb(ctx, drop=drop_db)
    migrate(ctx)
