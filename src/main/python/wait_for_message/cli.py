import sys
import time
import socket
import logging
import argparse

logger = logging.getLogger(__name__)


class MaxAttemptsError(Exception):
    """ maximum number of attempts
    """
    pass


def get_parser():
    """ return argument parser
    """
    parser = argparse.ArgumentParser(
        description='A simple client server utility that blocks until a message is received on a TCP/IP socket connection')
    subparser = parser.add_subparsers(dest='command')

    send_parser = subparser.add_parser('send', help='send message to tcp/ip connection until acknowledged or maximum attempts')
    send_parser.set_defaults(subcmd=send)
    send_parser.add_argument(
        '--ip-address',
        dest='ip_address',
        type=str,
        required=True,
        help='the ip address of the server')
    send_parser.add_argument(
        '--port-number',
        dest='port_number',
        type=int,
        required=True,
        help='the port number the server is listening on')
    send_parser.add_argument(
        '--message',
        dest='message_to_send',
        type=str,
        required=True,
        help='the message to send')
    send_parser.add_argument(
        '--delay',
        dest='delay',
        type=int,
        default=10,
        help='number of seconds to delay between retries; default 10')
    send_parser.add_argument(
        '--attempts',
        dest='max_attempts',
        type=int,
        default=6,
        help='maximum retry attempts; default 6')

    wait_parser = subparser.add_parser('wait', help="wait for message on tcp/ip connection until received or timeout")
    wait_parser.set_defaults(subcmd=wait)
    wait_parser.add_argument(
        '--ip-address',
        dest='ip_address',
        type=str,
        required=False,
        default='0.0.0.0',
        help='the ip address to bind to; default 0.0.0.0')
    wait_parser.add_argument(
        '--port-number',
        dest='port_number',
        type=int,
        required=True,
        help='the port number to listen on')
    wait_parser.add_argument(
        '--message',
        dest='message_to_wait_for',
        type=str,
        required=True,
        help='the message to wait for')
    wait_parser.add_argument(
        '--timeout',
        dest='timeout',
        type=int,
        default=60 * 15,
        help='number of seconds to wait for message; default 900 (i.e. 15 minutes)')

    return parser


def send(ip_address, port_number, message_to_send, delay, max_attempts):
    """ send message to server at ip_address:port_number
    """
    ip_address = ip_address.strip()
    logger.debug('creating tcp/ip socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    attempts = 0
    while True:
        if attempts >= max_attempts:
            error_message = f'exceeded maximum wait of {max_attempts * delay} seconds'
            logger.debug(error_message)
            raise MaxAttemptsError(error_message)
        try:
            logger.debug(f'connecting to server {ip_address}:{port_number}')
            s.connect((ip_address, port_number))

            logger.debug(f"sending message '{message_to_send}'")
            s.send(message_to_send.encode())

            # acknowledge the message was received
            # if no acknowledgement then connect and resend
            acknowledgement = s.recv(10000).decode()
            logger.debug(f"received acknowledgement: '{acknowledgement}'")
            if acknowledgement:
                break

        except socket.error as error:
            logger.debug(f'socket.error: {error}')
            logger.debug(f'retrying in {delay} seconds')
            time.sleep(delay)
            attempts += 1

    logger.debug('closing tcp/ip socket')
    s.close()


def wait(ip_address, port_number, message_to_wait_for, timeout):
    """ setup socket on port_number and wait for message
    """
    logger.debug('creating tcp/ip socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # PREVENT FROM "ADDRESS ALREADY IN USE" UPON restart
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(timeout)

    if ip_address == 'discover':
        server_name = socket.gethostname().lower()
        ip_address = socket.gethostbyname(server_name)
        logger.debug(f'ip address discovered for {server_name} is {ip_address}')

    logger.debug(f'binding and starting up on {ip_address}:{port_number}')
    server_address = (ip_address, port_number)
    s.bind(server_address)

    s.listen(5)

    while True:
        logger.debug('waiting for message')
        connection, _ = s.accept()
        logger.debug(f'accepted connection from {connection.getpeername()}')

        data = connection.recv(10000).decode()
        logger.debug(f"message received: '{data}'")

        message_received = False
        if data == message_to_wait_for:
            logger.debug('the message being waited for was received')
            message_received = True

        status = 'quitting' if message_received else 'waiting'
        acknowledgement = f'acknowledged - {status}'
        logger.debug(f"sending acknowledgement message: '{acknowledgement}'")
        connection.send(acknowledgement.encode())

        logger.debug('shutting down and closing connection')
        connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
        connection.close()

        if message_received:
            break

    logger.debug('closing tcp/ip socket')
    s.close()


def run(options):
    """ run subcmd
    """
    options.pop('command', None)
    subcmd = options.pop('subcmd', None)
    subcmd(**options)


def configure_logging():
    """ configure logging
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def main():
    """ main program
    """
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    configure_logging()
    args = get_parser().parse_args()
    run(vars(args))


if __name__ == '__main__':  # pragma: no cover
    main()
