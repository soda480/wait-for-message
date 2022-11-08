#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin
from pybuilder.core import init
from pybuilder.core import Author

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('pypi:pybuilder_radon')
use_plugin('pypi:pybuilder_bandit')
use_plugin('pypi:pybuilder_anybadge')

name = 'wait-for-message'
authors = [Author('Emilio Reyes', 'soda480@gmail.com')]
summary = 'A simple client server utility that blocks until a message is received on a TCP/IP socket connection'
url = 'https://github.com/soda480/wait-for-message'
version = '0.1.4'
default_task = [
    'clean',
    'analyze',
    'publish',
    'radon',
    'bandit',
    'anybadge']
license = 'Apache License, Version 2.0'
description = summary


@init
def set_properties(project):
    project.set_property('unittest_module_glob', 'test_*.py')
    project.set_property('coverage_break_build', False)
    project.set_property('flake8_max_line_length', 120)
    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_scripts', True)
    project.set_property('flake8_include_test_sources', True)
    project.set_property('flake8_ignore', 'F401, E501')
    project.build_depends_on('mock')
    project.depends_on_requirements('requirements.txt')
    project.set_property('distutils_console_scripts', ['w4m = wait_for_message.cli:main'])
    project.set_property('distutils_readme_description', True)
    project.set_property('distutils_description_overwrite', True)
    project.set_property('distutils_upload_skip_existing', True)
    project.set_property('distutils_classifiers', [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'])
    project.set_property('radon_break_build_average_complexity_threshold', 6)
    project.set_property('radon_break_build_complexity_threshold', 10)
    project.set_property('bandit_break_build', True)
    project.set_property('bandit_skip_ids', 'B104')
    project.set_property('anybadge_exclude', 'complexity, coverage')
