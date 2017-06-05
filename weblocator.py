#!/usr/bin/env python
import httplib, socket, threading, sys, argparse
import os
import locale
from urllib import urlopen

import socks


def create_tor_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    try:
        sock.connect(address)
    except Exception as e:
        sys.stdout.write(e.message)
        sys.stdout.flush()
        sys.exit()
    return sock


def is_online(host):
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return False
    else:
        return True


def is_path_available(host, path="/", validation=""):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        if conn.getresponse().status != 404:
            if (len(validation) > 0):
                http = httplib.HTTPConnection(host)
                http.request("GET", "/" + path)
                response = http.getresponse()
                if response.status == 200:
                    if validation not in response.read():
                        return True
                else:
                    return False
            else:
                return True
    except StandardError:
        return None


def worker(host, words, validation=""):
    for word in words:
        if (is_path_available(host=host, path=word, validation=validation)):
            print_message("\t[+] http://" + host + "/" + word + "\n")
    return


def split_list(list, parts=1):
    length = len(list)
    if (length > list):
        return [list[i * length // parts: (i + 1) * length // parts]
                for i in range(parts)]
    else:
        return list


def print_message(message):
    sys.stdout.write(message)
    sys.stdout.flush()


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'en_US')

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="The URL of the TARGET to scan.", required=True)
    parser.add_argument("-w", "--wordlist", help="The paths to locate.", required=True)
    parser.add_argument("--validation", help="Try to find a string to validate the results.", required=False)
    parser.add_argument("--threads", help="Number of threads [default=10].", required=False)
    parser.add_argument("--tor-host", help="Tor server.", required=False)
    parser.add_argument("--tor-port", help="Tor port server.", required=False)

    args = parser.parse_args()

    if args.tor_host:
        print_message("Opening Tor socket... ")
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.tor_host, int(args.tor_port), True)
        socket.socket = socks.socksocket
        socket.create_connection = create_tor_connection
        print_message("OK [" + urlopen('http://ip.42.pl/raw').read() + "].\n")

    if args.target and args.wordlist:
        if (os.path.isfile(args.wordlist)):
            words = []
            print_message("Reading the list... ")
            file = open(args.wordlist)
            for line in file.readlines():
                words.append([value for value in line.split()])
            file.close()
            count_paths = locale.format("%d", len(words), grouping=True)
            print_message("OK.\n\tThe selected file contains " + count_paths + " paths.\n")
            print_message("Checking if " + args.target + " is online... ")
            if (is_online(args.target)):
                print_message("OK.\n")
                threads = 10
                if args.threads:
                    threads = args.threads
                print_message("Ready to hunt using " + str(threads) + " threads.\n")
                for list in split_list(words, threads):
                    threading.Thread(target=worker, args=(args.target, list, args.validation)).start()
            else:
                print_message("ERROR: host is down.\n")
                sys.exit()

        else:
            print_message("ERROR: wordlist can't be found.\n")
            sys.exit()

    else:
        parser.print_help()
        sys.exit()
