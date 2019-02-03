#!../MacOS/python -u
"""
This script handles Firefox Native Messaging.
"""

import json
import logging
import os
import struct
import subprocess
import sys
import traceback

import common


class NativeMessageInterface(object):
    """
    Provides a Native Messaging interface,
    or its interactive mock-up.
    """
    def __init__(self, callback, interactive=False):
        """
        :param callback: A function to handle the message i.e. process a Native Messaging request.
        It would take a JSON-like structure and return another JSON-like structure which would be passed
        to the requester.
        Upon any failure, the error message along with the stacktrace would be passed to the requester.
        :param interactive: If set to `True`, would make the interface to be a command-line interface
        that reads messages from stdin and writes them back to stdout.
        """
        self._callback = callback
        self._interactive = interactive
        logging.info('PWD: %s' % os.getcwd())

    def get_message(self):
        """
        Read a message from stdin and decode it.
        """
        if self._interactive:
            raw_message = input('IN(json)> ')
            if raw_message == 'quit':
                print('Bye!')
                sys.exit(0)
        else:
            raw_length = sys.stdin.buffer.read(4)
            if not raw_length:
                sys.exit(0)
            message_length = struct.unpack('=I', raw_length)[0]
            raw_message = sys.stdin.read(message_length)
        message = json.loads(raw_message)
        logging.info('Request:\n%s' % json.dumps(message, indent=2))
        return message

    def send_message(self, message):
        """
        Send an encoded message to stdout.
        """
        logging.info('Response:\n%s' % json.dumps(message, indent=2))
        if self._interactive:
            print('OUT(json)> %s' % json.dumps(message, indent=2))
        else:
            encoded_content = json.dumps(message)
            encoded_length = struct.pack('=I', len(encoded_content))
            sys.stdout.buffer.write(encoded_length)
            sys.stdout.write(encoded_content)
            sys.stdout.flush()

    def run(self):
        while True:
            try:
                message = self.get_message()
                output = self._callback(message)
            except (KeyboardInterrupt, SystemExit):
                break
            except Exception as e:
                estr = traceback.format_exc()
                response = dict(error=str(e), trace=estr.split('\n'))
            else:
                response = dict(output=output)
            self.send_message(response)


class Handler(object):
    def __init__(self, data):
        self._data = data

    def handle(self, message):
        script_content = self.build_script_content(message)
        common.write_script(self._data.temp_script_path, script_content)
        return self.notify_agent()

    @staticmethod
    def build_script_content(message):
        """
        >>> print(Handler.build_script_content(dict(args=['app'])))
        #!/bin/bash
        app
        >>> print(Handler.build_script_content(dict(env=dict(A='A'), args=['app'])))
        #!/bin/bash
        A=A app
        >>> print(Handler.build_script_content(dict(args=['app', 'b'])))
        #!/bin/bash
        app b
        """
        env = ' '.join(['%s=%s' % (key, value)for key, value in message.get('env', {}).items()] + [''])
        args = ' '.join(['%s' % value for value in message['args']])
        return '\n'.join([
            '#!/bin/bash',
            '%s%s' % (env, args),
        ])

    def notify_agent(self):
        return str(subprocess.check_output(['/bin/kill', '-SIGUSR2', str(self._data.agent_pid)]))


def main():
    common.configure_logging('korred')
    data = common.Data()
    handler = Handler(data=data)
    NativeMessageInterface(
        callback=handler.handle,
        interactive=os.getenv('INTERACTIVE', False),
    ).run()


if __name__ == '__main__':
    main()
