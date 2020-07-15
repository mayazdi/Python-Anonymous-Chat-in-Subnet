# Seyyed & Amin Network Simulator
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

First of all, the client who wants to initiate chat, sends the request to the broadcast ip of the local subnet on port `8080`. This means that every member of that local subnet will receive the message on that port. then the other peers will send the UDP message containing a random port (which the chat will be held on that port) to that sender peer.
receiving peer initiates listening on that announced port in TCP mode. Then sending peer will initiate a TCP connection to the receiver. if no error occures the chat begins. each peer now can send and receive messages.
