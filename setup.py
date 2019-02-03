import os

from setuptools import setup, Command
import subprocess
import sys


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
                'org.example.korred.agent.plist',
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
