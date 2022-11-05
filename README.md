[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
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

## Execution

client
```
w4m send --ip-address 192.168.1.199 --port-number 8080 --message 'ready to proceed'

2022-11-05 16:56:42,724: creating tcp/ip socket
2022-11-05 16:56:42,724: connecting to server 192.168.1.199:8080
2022-11-05 16:56:42,725: sending message 'ready'
2022-11-05 16:56:42,725: received acknowledgement: 'acknowledged - waiting'
2022-11-05 16:56:42,725: closing tcp/ip socket

w4m send --ip-address 192.168.1.199 --port-number 8080 --message 'ready2'
2022-11-05 16:56:54,014: creating tcp/ip socket
2022-11-05 16:56:54,014: connecting to server 192.168.1.199:8080
2022-11-05 16:56:54,014: sending message 'ready2'
2022-11-05 16:56:54,015: received acknowledgement: 'acknowledged - waiting'
2022-11-05 16:56:54,015: closing tcp/ip socket

w4m send --ip-address 192.168.1.199 --port-number 8080 --message 'ready to proceed'
2022-11-05 16:56:58,520: creating tcp/ip socket
2022-11-05 16:56:58,520: connecting to server 192.168.1.199:8080
2022-11-05 16:56:58,520: sending message 'ready to proceed'
2022-11-05 16:56:58,521: received acknowledgement: 'acknowledged - quitting'
2022-11-05 16:56:58,521: closing tcp/ip socket
```

server
```
w4m wait --port-number 8080 --message 'ready to proceed'

2022-11-05 16:56:33,717: creating tcp/ip socket
2022-11-05 16:56:33,717: binding and starting up on 652b723eb830:8080
2022-11-05 16:56:33,717: waiting for message
2022-11-05 16:56:42,725: accepted connection from ('172.17.0.1', 42148)
2022-11-05 16:56:42,725: message received: 'ready'
2022-11-05 16:56:42,725: sending acknowledgement message: 'acknowledged - waiting'
2022-11-05 16:56:42,725: shutting down and closing connection
2022-11-05 16:56:42,725: waiting for message
2022-11-05 16:56:54,015: accepted connection from ('172.17.0.1', 42152)
2022-11-05 16:56:54,015: message received: 'ready2'
2022-11-05 16:56:54,015: sending acknowledgement message: 'acknowledged - waiting'
2022-11-05 16:56:54,015: shutting down and closing connection
2022-11-05 16:56:54,015: waiting for message
2022-11-05 16:56:58,520: accepted connection from ('172.17.0.1', 42156)
2022-11-05 16:56:58,520: message received: 'ready to proceed'
2022-11-05 16:56:58,520: the message being waited for was received
2022-11-05 16:56:58,520: sending acknowledgement message: 'acknowledged - quitting'
2022-11-05 16:56:58,520: shutting down and closing connection
2022-11-05 16:56:58,520: closing tcp/ip socket
```

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