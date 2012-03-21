from .config import resource_spec
from .config import yml_load
from .devinst import devinstall
import argparse
import sys


def main(argv=None):
    if argv is None: #pragma: no cover
        argv = sys.argv[1:] 
    parser = argparse.ArgumentParser()    
    subparsers = parser.add_subparsers(help='commands')

    devinst_parser = subparsers.add_parser('devinst', help='Create a development environment')
    devinst_parser.add_argument('-c', '--config', action='store',
                                default='egg:doulado#doulado/devinst.yml',
                                help='config file for running devinst')
    devinst_parser.add_argument('-r', '--read-only', 
                                default=False,
                                action='store_true',
                                help='use git readonly dependencies')
    
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
    config = resource_spec(args.config)
    with open(config) as conf_file:
        depinfo = next(yml_load(conf_file))
    deps = depinfo['dependencies'].copy()
    if args.read_only:
        deps.update(depinfo['readonly'])
    return devinstall(deps)
 

def deploy(args):
    return True


def create(args):
    return True
