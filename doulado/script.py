from path import path
import argparse
import sys



def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()    
    subparsers = parser.add_subparsers(help='commands')
    devinst_parser = subparsers.add_parser('devinst', help='Create a development environment')
    devinst_parser.add_argument('virtualenv', action='store',
                                help='name of virtualenv to createor to which to install doula')

    deploy_parser = subparsers.add_parser('deploy', help='Deploy doula')
    deploy_parser.add_argument('config', action='store',
                               help='path to deployment config')
    create_parser = subparsers.add_parser('create', help='scaffolding for various bits of doula')
    create_parser.add_argument('what', action='store',
                               help='thing to use scaffold to create')
    
    parser.parse_args(args=argv)
