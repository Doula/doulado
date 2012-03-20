from contextlib import contextmanager
from fabric import api as fab
from path import path
import os
import subprocess

pushd = fab.lcd

GEVENT = 'git@github.com:whitmo/gevent.git'
GEVENT_ZMQ = 'git@github.com:whitmo/gevent-zeromq.git'
DOULA = 'git@github.com:SurveyMonkey/Doula.git'
BAMBINO = 'git@github.com:SurveyMonkey/Bambino.git'
ZMQ = 'zeromq-2.1.11'
venv = path(os.environ['VIRTUAL_ENV'])

def ppid():
    print os.getpid()

def not_on_path(pkg):
    try:
        __import__(pkg)
        return False
    except ImportError:
        return True


def check_and_install(pkg, cmd, runner='local', test=not_on_path):
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
def install_doula(repo=DOULA):
    clone_develop('doula', repo)


@fab.task
def install_bambino(repo=BAMBINO):
    clone_develop('bambino', repo)


@fab.task
def install_zmq(version=ZMQ):
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
def devinstall():
    venv = path(os.environ['VIRTUAL_ENV'])
    srcdir = venv / 'src'
    with pushd(srcdir):
        fab.execute(install_zmq)
        fab.local('pip install distribute==0.6.14')
        check_and_install('cython', 'pip install Cython')
        check_and_install('gevent', 'pip install -e git+%s#egg=gevent' %GEVENT)
        check_and_install('zmq', "pip install pyzmq --install-option='--zmq=%s'" %venv)
        check_and_install('gevent_zmq', install_gz)
        install_doula()
        install_bambino()


@fab.task
def install_gz():
    srcdir = venv / 'src'
    with pushd(srcdir):
        with fab.settings(warn_only=True):
            if not path('gevent-zeromq').exists():
                fab.local('git clone %s' %GEVENT_ZMQ)
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
