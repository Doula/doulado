from .fabfile import sh, devinstall
from path import path
import argparse
import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()    
    subparsers = parser.add_subparsers(help='commands')
    devinst_parser = subparsers.add_parser('devinst', help='Create a development environment')
    ## devinst_parser.add_argument('virtualenv', action='store',
    ##                             help='name of virtualenv to create or into which to install doula')
    
    devinst_parser.set_defaults(func=devinst)
    deploy_parser = subparsers.add_parser('deploy', help='Deploy doula')
    deploy_parser.add_argument('config', action='store',
                               help='path to deployment config')

    deploy_parser.set_defaults(func=deploy)
    create_parser = subparsers.add_parser('create', help='scaffolding for various bits of doula')
    create_parser.add_argument('what', action='store',
                               help='thing to use scaffold to create')

    create_parser.set_defaults(func=create)
    args = parser.parse_args(args=argv)
    return args.func(args)


def devinst(args):
    devinstall()

def deploy(args):
    pass

def create(args):
    pass
