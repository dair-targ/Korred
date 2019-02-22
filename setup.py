import json
import os

from setuptools import setup, Command
import subprocess
import sys
import glob
import shutil


class BuildWebExtensionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(
            args=['npm', 'run', 'build'],
            cwd=os.path.join('.', 'extension'),
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        with open(os.path.join('.', 'extension', 'local', 'credentials.json')) as f:
            credentials = json.load(f)
        subprocess.run(
            args=[
                './node_modules/.bin/web-ext',
                'sign',
                '--api-key', credentials['apiKey'],
                '--api-secret', credentials['apiSecret']
            ],
            cwd=os.path.join('.', 'extension'),
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        shutil.copyfile(
            max(
                glob.glob('./extension/build/korred-*.xpi'),
                key=os.path.getctime,
            ),
            './extension/build/korred.xpi'
        )


setup(
    name='Korred',
    app=['korredd.py'],
    data_files=[],
    options=dict(
        py2app=dict(
            plist=dict(
                Label='org.example.korred',
                LSUIElement=True,
                RunAtLoad=True,
                LaunchOnlyOnce=True,
                ProgramArguments=['Contents/MacOS/Korred'],
                Disabled=False,
                ProcessType='Interactive',
            ),
            resources=[
                'korred.py',
                'common.py',
                'extension/build/korred.xpi'
            ]
        )
    ),
    setup_requires=[
        'py2app',
    ],
    install_requires=[
        'rumps',
    ],
    cmdclass={
        'build_webextension': BuildWebExtensionCommand,
    }
)
