import logging
import plistlib
import os
import stat


def configure_logging(target: str):
    log_dir = os.path.join(os.path.expanduser('~'), 'Library', 'Logs', 'Korred')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler(os.path.join(log_dir, '%s.log' % target))
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s:%(message)s'))
    logging.root.addHandler(handler)


def write_script(path, content):
    with open(path, 'w') as script_file:
        script_file.write(content)
    os.chmod(script_file.name, stat.S_IREAD | stat.S_IEXEC | stat.S_IWRITE)


class Data(object):
    """
    Handles the data common for `korred` and `korredd`.

    >>> data = Data('/tmp/Korred')
    >>> data.agent_pid = 42
    >>> data.agent_pid
    42
    >>> del data.agent_pid
    >>> data.agent_pid
    -1
    """
    def __init__(self, application_support_path='~/Library/Application Support/Korred'):
        self._path = os.path.expanduser(application_support_path)
        os.makedirs(self._path, exist_ok=True)

    @property
    def temp_script_path(self) -> str:
        return os.path.join(self._path, 'temp.sh')

    @property
    def agent_pid_path(self):
        return os.path.join(self._path, 'agent.pid')

    @property
    def agent_pid(self) -> int:
        try:
            with open(self.agent_pid_path) as f:
                return int(f.read())
        except FileNotFoundError:
            return -1

    @agent_pid.setter
    def agent_pid(self, value: int):
        with open(self.agent_pid_path, 'w') as f:
            f.write(str(value) + '\n')

    @agent_pid.deleter
    def agent_pid(self):
        try:
            os.remove(self.agent_pid_path)
        except FileNotFoundError:
            pass


__all__ = [
    'configure_logging',
    'write_script',
    'Data',
]
