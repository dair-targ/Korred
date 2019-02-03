import json
import logging
import multiprocessing
import os
import signal
import subprocess
import traceback
import rumps
import common


def open_in_app(*args, app='Terminal', new_instance=True):
    try:
        args = ['/usr/bin/open'] + (['-n'] if new_instance else []) + ['-a', app] + list(args)
        logging.info('Executing: %s' % ' '.join(args))
        return subprocess.check_output(args)
    except Exception as exception:
        logging.exception('Signal processing failure', exception)


class Daemon(object):
    """
    Handles the SIGUSR2 and opens a Terminal upon receiving it.

    AppKit handles signals itself, so instead of hacking it we just spawn a child daemon to handle the signals.
    """
    def __init__(self, data):
        self._subprocess = multiprocessing.Process(
            name='KorredDaemon',
            target=self.run,
            daemon=True,
        )
        self._data = data
        del self._data.agent_pid

    def __enter__(self):
        self._subprocess.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.error('Error occurred, stopping the daemon', traceback.format_exc())
        self._subprocess.join(timeout=0.1)

    def run(self):
        agent_pid = os.getpid()
        logging.info('Running Korred daemon with PID=%s' % agent_pid)
        signal.signal(signal.SIGUSR2, self.handle)
        self._data.agent_pid = agent_pid
        try:
            while True:
                signal.pause()
        except KeyboardInterrupt:
            pass
        finally:
            del self._data.agent_pid

    # noinspection PyUnusedLocal,PyShadowingNames
    def handle(self, signal, frame):
        open_in_app(self._data.temp_script_path)


class NativeMessagingConfiguration(object):
    """
    Writes Native Messaging manifest.
    """
    @staticmethod
    def get_path():
        return os.path.expanduser('~/Library/Application Support/Mozilla/NativeMessagingHosts/korred.json')

    @staticmethod
    def build():
        return dict(
            name='korred',
            description='Script to dump arguments into a file',
            path=os.path.join(os.getcwd(), 'korred.py'),
            type='stdio',
            allowed_extensions=[
                'korred@example.org',
            ],
        )

    def write(self):
        native_messaging_config_path = self.get_path()
        os.makedirs(os.path.dirname(native_messaging_config_path), exist_ok=True)
        with open(native_messaging_config_path, 'w') as f:
            configuration = self.build()
            json.dump(configuration, f, indent=2)


class LaunchctlManager(object):
    @property
    def source_path(self):
        return os.path.abspath(os.path.join('.', 'org.example.korred.agent.plist'))

    @property
    def target_path(self):
        return os.path.expanduser(os.path.join('~', 'Library', 'LaunchAgents', 'org.example.korred.agent.plist'))

    def is_loaded(self):
        try:
            return os.path.samefile(self.source_path, self.target_path)
        except IOError:
            return False

    def switch(self):
        if self.is_loaded():
            os.remove(self.target_path)
            return False
        else:
            if os.path.exists(self.target_path):
                os.remove(self.target_path)
            os.link(self.source_path, self.target_path)
            return True


class App(rumps.App):
    def __init__(self, launchctl_manager):
        super(App, self).__init__(name='Korred')
        self._launchctl_manager = launchctl_manager

    @rumps.clicked('Install Firefox Extension...')
    def install_firefox_extension(self, _):
        os.system('open http://google.com')

    @rumps.clicked('Launch at Login')
    def launch_at_login(self, sender):
        sender.state = self._launchctl_manager.switch()

    @rumps.clicked('View Logs')
    def view_logs_of_native_messaging_handler(self, _):
        open_in_app(
            *filter(os.path.isfile, [
                os.path.expanduser('~/Library/Logs/Korred/%s.log' % log_name)
                for log_name in ['korredd', 'korred']
            ]),
            app='Console',
            new_instance=False,
        )


def main():
    data = common.Data()
    with Daemon(data):
        # TODO: Check for configuration validity and ask user if the old configuration should be kept
        NativeMessagingConfiguration().write()
        launchctl_manager = LaunchctlManager()
        app = App(launchctl_manager)
        menu_item = rumps.MenuItem(title='Launch at Login')
        menu_item.state = launchctl_manager.is_loaded()
        app.menu = [
            'Install Firefox Extension...',
            menu_item,
            'View Logs',
        ]
        app.run()


if __name__ == "__main__":
    common.configure_logging('korredd')
    try:
        main()
    except Exception as e:
        logging.critical('Critical error', e)
    logging.info('Quit korredd')
