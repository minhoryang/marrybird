import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "eventlet"
reload = True

try:
    from dulwich.repo import Repo
    r = Repo('.')
    # gittle
    def active_branch(repo, SYMREF=b'ref: ', REFS_BRANCHES=b'refs/heads/'):
        """Returns the name of the active branch, or None, if HEAD is detached
        """
        x = repo.refs.read_ref('HEAD')
        if not x.startswith(SYMREF):
            return b''
        else:
            symref = x[len(SYMREF):]
            if not symref.startswith(REFS_BRANCHES):
                return b''
            else:
                return symref[len(REFS_BRANCHES):]
    import gunicorn
    gunicorn.SERVER_SOFTWARE = 'MarryBird %s(%s)' % (active_branch(r).decode('ascii'), r.head().decode('ascii')[:11])
except:
    pass
