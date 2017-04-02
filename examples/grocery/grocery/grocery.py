from __future__ import print_function
from socket import gethostname
import argparse
import datetime
import getpass
import os
import shlex
import sys

from desmod.config import (ConfigError,
                           apply_user_config,
                           apply_user_overrides,
                           parse_user_factors)
from desmod.simulation import simulate, simulate_factors, simulate_many
from pkg_resources import get_distribution
from setuptools_scm import get_version as get_git_version
from setuptools_scm.git import parse as git_parse
import yaml

from grocery.config import named
from grocery.env import Environment
from grocery.top import Top


def main(argv=None):
    """Command line interface for running grocery simulations.

    This function handles command line parsing, configuration setup, and
    launching simulations.

    """
    parser = argparse.ArgumentParser()
    version = get_version()
    parser.add_argument(
        '--version', '-V', action='version', version=version,
        help='Show version and exit.')
    parser.add_argument(
        '--named', '-n', metavar='GROUP', dest='named_configs',
        action='append', default=[],
        help='Use named configuration %(metavar)s.')
    parser.add_argument(
        '--set', '-s', nargs=2, metavar=('KEY', 'VALUE'),
        action='append', default=[], dest='config_overrides',
        help='Override configuration KEY with VALUE expression.')
    parser.add_argument(
        '--factor', '-f', nargs=2, metavar=('KEYS', 'VALUES'),
        action='append', default=[], dest='factors',
        help='Add factorial KEYS with VALUES list of value expressions.')
    parser.add_argument(
        '--config', '-c', metavar='YAML', type=argparse.FileType('r'),
        action='append', default=[], dest='config_files',
        help='Read configuration from YAML file.')
    parser.add_argument(
        '--print-config', action='store_true',
        help='Print configuration and exit.')
    parser.add_argument(
        '--print-named', action='store_true',
        help='Print named configuration groups and exit.')

    extra_argv = shlex.split(os.environ.get('SB_EXTRA', ''))

    if argv is None:
        argv = sys.argv[1:]

    args = parser.parse_args(extra_argv + argv)

    if len(args.config_files) > 1 and args.factors:
        parser.error('argument --factor/-f: not allowed with multiple '
                     '--config/-c arguments')

    if args.print_named:
        print_named(named, sys.stdout)
        parser.exit()

    configs = []

    try:
        if args.config_files:
            named_overrides = named.resolve(*args.named_configs)
            for config_file in args.config_files:
                config = named.resolve('default')
                apply_user_config(config, parse_config_file(config_file))
                config.update(named_overrides)
                apply_user_overrides(config, args.config_overrides)
                configs.append(config)
        else:
            config = named.resolve('default', *args.named_configs)
            apply_user_overrides(config, args.config_overrides)
            configs.append(config)

        factors = parse_user_factors(configs[0], args.factors)
    except ConfigError as e:
        parser.error(str(e))

    if args.print_config:
        yaml.safe_dump_all(configs, stream=sys.stdout)
        parser.exit()

    try:
        if len(configs) == 1:
            config = configs[0]
            if factors:
                results = simulate_factors(config, factors, Top, Environment)
                return check_errors(results)
            else:
                simulate(config, Top, Environment)
        else:
            results = simulate_many(configs, Top, Environment)
            return check_errors(results)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 1


def get_version():
    return '0.0.1'


def parse_config_file(config_file):
    loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
    doc = yaml.load(config_file, Loader=loader)
    if 'config' in doc:
        raw_config = doc['config']
    else:
        raw_config = doc
    return {k: v for k, v in raw_config.items()
            if not k.startswith('meta.')}


def check_errors(results):
    any_errors = False
    for result in results:
        exc = result.get('sim.exception')
        if exc:
            config = result['config']
            special = ('{' +
                       ', '.join('{k}: {v}'.format(k=k, v=v)
                                 for k, v in config['meta.sim.special']) +
                       '}')
            sim_index = config['meta.sim.index']
            logpath = os.path.join(config['meta.sim.workspace'],
                                   config['sim.log.file'])
            print('{} failed with {}. See {}. Special: {}'
                  .format(sim_index, exc, logpath, special))
            any_errors = True
    return any_errors


def print_named(named, file):
    name_w = max(len('NAME'), max(len(nc.name) for nc in named))
    cat_w = max(len('CATEGORY'), max(len(nc.category) for nc in named))
    print('{:{cat_w}} {:{name_w}} {}'.format('CATEGORY', 'NAME', 'DOC',
                                             cat_w=cat_w, name_w=name_w),
          file=file)
    for nc in sorted(named):
        doc_lines = nc.doc.splitlines()
        doc = doc_lines[0] if doc_lines else ''
        print('{nc.category:{cat_w}} {nc.name:{name_w}} {doc}'
              .format(nc=nc, doc=doc, cat_w=cat_w, name_w=name_w),
              file=file)


if __name__ == '__main__':
    sys.exit(main())
