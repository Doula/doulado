from contextlib import contextmanager
from fabric import api as fab
from path import path
import stuf
import os
import subprocess


pushd = fab.lcd
venv = path(os.environ['VIRTUAL_ENV'])

def ppid():
    print os.getpid()

def not_on_path(pkg):
    try:
        __import__(pkg)
        return False
    except ImportError:
        return True


def check_and_install(pkg, cmd, runner='local', test=not_on_path, **kw):
    if test(pkg):
        if isinstance(cmd, basestring):
            run = getattr(fab, runner)
            return run(cmd)
        return cmd()


def sh(cmd, pre=ppid, **addenv):
    env = os.environ.copy()
    env.update(addenv)
    return subprocess.check_output(cmd, env=env, preexec_fn=pre, shell=True)


@fab.task
def clone_develop(pkg, repo):
    srcdir = venv / 'src'
    with pushd(srcdir):
        if not path(pkg).exists():
            fab.local('git clone %s %s' %(repo, pkg))
            fab.local('pip install -r %s/develop.txt' %pkg)
            fab.local('pip install -e ./%s' %pkg)


@fab.task
def install_zmq(version=None):
    srcdir = venv / 'src'
    if not (srcdir / version).exists():
        with pushd(srcdir):
            fab.local('wget -O - "http://download.zeromq.org/%s.tar.gz" | tar -xzf -' %version)
        
    with pushd(srcdir / version):
        if not path('config.status').exists():
            fab.local("./configure --prefix %s" %venv)
            fab.local('make')
            fab.local('make install')


@fab.task
def devinstall(deps=None):
    deps = stuf.fixedstuf(deps)
    venv = path(os.environ['VIRTUAL_ENV'])
    srcdir = venv / 'src'
    if not srcdir.exists():
        srcdir.mkdir()
    with pushd(srcdir):
        install_zmq(deps.zmq)
        fab.local('pip install distribute==0.6.14')
        check_and_install('cython', 'pip install Cython')
        check_and_install('gevent', 'pip install -e git+%s#egg=gevent' %deps.gevent)
        check_and_install('zmq', "pip install pyzmq --install-option='--zmq=%s'" %venv)
        check_and_install('gevent_zmq', install_gz, repo=deps.gevent_zmq)
        clone_develop(repo=deps.doula)
        clone_develop(repo=deps.bambino)


@fab.task
def install_gz(repo='git@github.com:whitmo/gevent-zeromq.git'):
    srcdir = venv / 'src'
    with pushd(srcdir):
        with fab.settings(warn_only=True):
            if not path('gevent-zeromq').exists():
                fab.local('git clone %s' %repo)
        with pushd('gevent-zeromq'):
            fab.local("python setup.py build_ext -I$VIRTUAL_ENV/include install")


@contextmanager
def pushd(dir):
    old_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield old_dir
    finally:
        os.chdir(old_dir)
