#!/usr/bin/env python
import argparse
import os
import socket
import threading
from urllib import urlopen

import socks

from helpers import print_message, is_online, split_list, is_path_available


def create_tor_connection(address):
    sock = socks.socksocket()
    sock.connect(address)
    return sock


def worker(host, words_list, port=80, http=True, validation=None):
    protocol = 'http' if http else 'https'
    for word in words_list:
        if '.' not in word:
            word = '{}/'.format(word)
        if is_path_available(host=host, url_path=word, validation=validation, http=http, port=port):
            print_message("\t[+] {}://{}/{}\n".format(protocol, host, word))
    return


if __name__ == '__main__':
    print_message(" __          __  _     _                     _              \n")
    print_message(" \ \        / / | |   | |                   | |             \n")
    print_message("  \ \  /\  / /__| |__ | |     ___   ___ __ _| |_ ___  _ __  \n")
    print_message("   \ \/  \/ / _ \ '_ \| |    / _ \ / __/ _` | __/ _ \| '__| \n")
    print_message("    \  /\  /  __/ |_) | |___| (_) | (_| (_| | || (_) | |    \n")
    print_message("     \/  \/ \___|_.__/|______\___/ \___\__,_|\__\___/|_|    \n")
    print_message("                                                            \n")
    print_message("weblocator.py - Just another DirBuster\n")
    print_message("Version 1.0\n")
    print_message("David Tavarez (davidtavarez)\n")
    print_message("https://github.com/davidtavarez/weblocator\n\n")

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", help="The URL of the TARGET to scan.", required=True)
    parser.add_argument("-w", "--wordslist", help="The words list path.", required=True)
    parser.add_argument("-p", "--port", help="The words list path.", required=True)
    parser.add_argument("-o", "--protocol", help="Protocol (http or https).", required=True)

    parser.add_argument("--validation", help="Try to find a string to validate the results.", required=False)
    parser.add_argument("--extension", help="Add an extension.", required=False)
    parser.add_argument("--threads", help="Number of threads [default=10].", required=False)
    parser.add_argument("--tor-host", help="Tor server.", required=False)
    parser.add_argument("--tor-port", help="Tor port server.", required=False)

    args = parser.parse_args()

    protocol = 'http' if not args.protocol else args.protocol
    if protocol not in ['http', 'https']:
        print_message("ERROR: Invalid protocol.\n")
        exit(-1)
    http = True
    if protocol == 'https':
        http = False

    if args.tor_host:
        try:
            print_message("Opening Tor socket... ")
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.tor_host, int(args.tor_port), True)
            socket.socket = socks.socksocket
            socket.create_connection = create_tor_connection
            print_message("OK (" + urlopen('http://ip.42.pl/raw').read() + ").\n")
        except Exception as e:
            print_message(e.message)
            exit(-1)

    if not args.target or not args.wordslist:
        print_message("ERROR: missing arguments.\n")
        exit(-1)

    if not os.path.isfile(args.wordslist):
        print_message("ERROR: words list can't be found.\n")
        exit(-1)

    print_message("Checking if " + args.target + " is online... ")
    if not is_online(args.target):
        print_message("ERROR: host is down.\n")
        exit(-1)
    print_message("OK.\n")

    words = []
    print_message("Reading the words list... ")
    word_list = open(args.wordslist)
    for line in word_list.readlines():
        word = line.strip()
        if args.extension:
            word = "{}.{}".format(word, args.extension)
        words.append(word)
    word_list.close()

    print_message("OK.\n\tThe selected file contains " + str(len(words)) + " paths.\n")

    threads = 10
    if args.threads:
        threads = int(args.threads)
    print_message("Hunting paths using " + str(threads) + " threads... just wait...\n")

    port = 80
    if args.port:
        port = int(args.port)

    for portion in split_list(words, threads):
        threading.Thread(target=worker, args=(args.target, portion, port, http, args.validation)).start()
