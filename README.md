[![build](https://github.com/soda480/wait-for-message/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/wait-for-message/actions/workflows/main.yml)
[![Code Grade](https://api.codiga.io/project/34932/status/svg)](https://app.codiga.io/hub/project/34932/wait-for-message)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![PyPI version](https://badge.fury.io/py/wait-for-message.svg)](https://badge.fury.io/py/wait-for-message)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)
# wait-for-message

A simple client server utility that blocks until a message is received on a TCP/IP socket connection; useful for synchronizing interdependent networked jobs.

## `w4m` Usage
```bash
usage: w4m [-h] {send,wait} ...

A simple client server utility that blocks until a message is received on a TCP/IP socket connection

positional arguments:
  {send,wait}
    send       send message to server
    wait       wait for message from client

optional arguments:
  -h, --help   show this help message and exit
```

### `w4m send`
```bash
usage: w4m send [-h] --ip-address IP_ADDRESS --port-number PORT_NUMBER --message MESSAGE_TO_SEND [--delay DELAY] [--attempts MAX_ATTEMPTS]

optional arguments:
  -h, --help            show this help message and exit
  --ip-address IP_ADDRESS
                        the ip address of the server
  --port-number PORT_NUMBER
                        the port number the server is listening on
  --message MESSAGE_TO_SEND
                        the message to send
  --delay DELAY         number of seconds to delay between retries; default 10
  --attempts MAX_ATTEMPTS
                        maximum retry attempts; default 6
```

### `w4m wait`
```bash
usage: w4m wait [-h] --port-number PORT_NUMBER --message MESSAGE_TO_WAIT_FOR [--timeout TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --port-number PORT_NUMBER
                        the port number the server is listening on
  --message MESSAGE_TO_WAIT_FOR
                        the message to wait for
  --timeout TIMEOUT     number of seconds to wait for message; default 900 (i.e. 15 minutes)
```

## Example

client
```
w4m send --ip-address 192.168.1.199 --port-number 8080 --message 'a message'
w4m send --ip-address 192.168.1.199 --port-number 8080 --message 'another message'
w4m send --ip-address 192.168.1.199 --port-number 8080 --message 'ready to proceed'
```

server
```
w4m wait --port-number 8080 --message 'ready to proceed'
```

![example1](https://raw.githubusercontent.com/soda480/wait-for-message/main/docs/images/execution.gif)

## Development

Build the Docker image:
```
docker image build \
-t \
w4m:latest .
```

Run the Docker container:
```
docker container run \
--rm \
-it \
-v $PWD:/code \
-p:8080:8080 \
w4m:latest \
bash
```