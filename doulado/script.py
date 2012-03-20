from .config import resource_spec 
from .devinst import devinstall
import argparse
import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()    
    subparsers = parser.add_subparsers(help='commands')
    devinst_parser = subparsers.add_parser('devinst', help='Create a development environment')
    devinst_parser.add_argument('-c', action='store', default=resource_spec('egg:DoulaDo#doulado/devinst.yml'),
                                help='config file for running devinst')
    
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
