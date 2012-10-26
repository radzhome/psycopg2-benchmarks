import time
from functools import wraps
import traceback


def print_time(*deco_args, **deco_kwargs):
    ''' Print function execution time.
    Supports additional profiling:
    profile = True  - using profilehooks (uses cProfile),
    stat_profile = True - using statprof
    '''
    def deco(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            if deco_kwargs.get('traceback'):
                traceback.print_stack()
            print 'starting %s' % fn.__name__
            start = time.time()
            stat_profile = deco_kwargs.get('stat_profile')
            if stat_profile:
                import statprof
                statprof.reset(frequency=10000)
                statprof.start()
            try:
                return fn(*args, **kwargs)
            finally:
                print 'finished %s in %s s' % \
                        (fn.__name__, time.time() - start)
                if stat_profile:
                    statprof.stop()
                    statprof.display()
        if deco_kwargs.get('profile'):
            import profilehooks
            inner = profilehooks.profile(immediate=True)(inner)
        return inner
    if deco_args:
        return deco(deco_args[0])
    else:
        return deco

def bulk_ids(model, n):
    from django.db import connection
    cursor = connection.cursor()
    sql = "select nextval('%s_id_seq') from generate_series(1,%d)" % \
            (model._meta.db_table, n)
    cursor.execute(sql)
    return [int(r[0]) for r in cursor]
