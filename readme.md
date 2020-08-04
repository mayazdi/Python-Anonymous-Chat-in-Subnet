# Seyyed & Amin Network local subnet anonymous chat
Computer Networking Project number 3 - Shahid Beheshti University - Summer 1399

Simple Anonymous Chat in local subnet with python

## Requirements
Any version of Python 3


## Discription
This program runs in a local network and mathes two peers to chat anonymously.


## Usage

To run:

`python main.py`

After running the program and matching two peers. you can send or receive messages through the CLI.

## How it Works

First of all you need to choose your netowork masking mode.
As default the masking is set to `/24` (which most of the networks are). but this value can be set manually by user.
In order to change this value, you can enter another valid value. like `25`


Because it's not possible to run two peers in the same computer you have to choose the mode you want the program to use.(It's obvious that on different clients it can run properly by adding couple of lines). The client who wants to initiate chat, sends the request to the broadcast IP of the local subnet on port `8080`. This means that every member of that local subnet will receive the message on that port. then the other peers will send the UDP message containing a random port (which the chat will be held on that port) to that sender peer. in some cases the port might be occupied by one of the peers. this process goes on until both peers be OK with the agreed port number.
receiving peer initiates listening on that announced port in TCP mode. Then sending peer will initiate a TCP connection to the receiver. if no error occures the chat begins. each peer now can send and receive messages.

### Received messages

When a client receive a message, message won't show until that peer sends the current message. But will be notified by alalrm of th systm. All of the incomming messages will be cached and shown after message get sent.

* empty messages won't be sen't

* long messages also will be dropped.
