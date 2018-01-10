from setuptools import setup
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('scicolpick/scicolpick.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))

setup(
    name='scicolpick',
    version=version,
    packages=['scicolpick'],
    install_requires=['click', 'colormath', 'matplotlib'],
    entry_points={
        'console_scripts': 'scicolpick = scicolpick.scicolpick:scicolpick_main'
    },
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
    ],
)
