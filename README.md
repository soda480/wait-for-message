[![build](https://github.com/soda480/wait-for-message/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/wait-for-message/actions/workflows/main.yml)
[![Code Grade](https://api.codiga.io/project/34932/status/svg)](https://app.codiga.io/hub/project/34932/wait-for-message)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![PyPI version](https://badge.fury.io/py/wait-for-message.svg)](https://badge.fury.io/py/wait-for-message)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)
# wait-for-message

A simple client server utility that blocks until a message is received on a TCP/IP socket connection; useful for synchronizing interdependent networked jobs.

## Installation
```bash
pip install wait-for-message
```

## `w4m` Usage
```bash
usage: w4m [-h] {send,wait} ...

A simple client server utility that blocks until a message is received on a TCP/IP socket connection

positional arguments:
  {send,wait}
    send       send message to tcp/ip connection until acknowledged or maximum attempts
    wait       wait for message on tcp/ip connection until received or timeout

optional arguments:
  -h, --help   show this help message and exit
```

### `w4m send`

send message to tcp/ip connection until acknowledged or maximum attempts

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

wait for message on tcp/ip connection until received or timeout - if message received and if it contains a body print it to stdout

```bash
usage: w4m wait [-h] [--ip-address IP_ADDRESS] --port-number PORT_NUMBER --message MESSAGE_TO_WAIT_FOR [--timeout TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --ip-address IP_ADDRESS
                        the ip address to bind to; default 0.0.0.0
  --port-number PORT_NUMBER
                        the port number to listen on
  --message MESSAGE_TO_WAIT_FOR
                        the message to wait for
  --timeout TIMEOUT     number of seconds to wait for message; default 900 (i.e. 15 minutes)
```

## Example

### wait

On a Linux machine, start tcp/ip socket listening on port 8080 and wait for message. Note the script blocks until the expected message is received. If the message is not received a timeout error will be thrown. The message received contains a body it is printed to stdout.

```
w4m wait --port-number 8080 --message "ready to proceed"
```

### send

On an other machine (this example we used a Windows machine), connect tcip/ip socket to the ip:port for the server and send several messages. Send will resend message until an acknowledgement is received. If no acknowledgement is received after max attempts a MaxAttemptsError is thrown.

```
w4m send --ip-address 192.168.1.199 --port-number 8080 --message "a message"
w4m send --ip-address 192.168.1.199 --port-number 8080 --message "another message"
w4m send --ip-address 192.168.1.199 --port-number 8080 --message "ready to proceed:message body"
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