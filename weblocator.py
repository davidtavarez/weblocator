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
    if len(path) > 0:
        try:
            conn = httplib.HTTPConnection(host,80,10)
            conn.request("HEAD", path)
            status = conn.getresponse().status
            if status == 200 or status == 401 or status == 403:
                conn.close()
                if (len(validation) > 0):
                    http = httplib.HTTPConnection(host,80,10)
                    http.request("GET", route)
                    response = http.getresponse()
                    if response.status == 200:
                        if validation not in response.read():
                            http.close()
                            return True
                    else:
                        return False
                else:
                    return True
        except Exception as e:
            return None
    return None


def worker(host, words, validation=""):
    for word in words:
        route = word
        if not route.startswith('/'):
            route = '/' + route
        if not word.endswith('/'):
            name, extension = os.path.splitext(word)
            if len(extension) == 0:
                route = route + '/'
        if route != "/./" :
            if is_path_available(host=host, path=route, validation=validation):
                print_message("\t[+] http://" + host  + route + "\n")
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
    parser.add_argument("--extension", help="Add an extension.", required=False)
    parser.add_argument("--threads", help="Number of threads [default=10].", required=False)
    parser.add_argument("--tor-host", help="Tor server.", required=False)
    parser.add_argument("--tor-port", help="Tor port server.", required=False)

    args = parser.parse_args()

    if args.tor_host:
        print_message("Opening Tor socket... ")
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.tor_host, int(args.tor_port), True)
        socket.socket = socks.socksocket
        socket.create_connection = create_tor_connection
        print_message("OK (" + urlopen('http://ip.42.pl/raw').read() + ").\n")

    if args.target and args.wordlist:
        if (os.path.isfile(args.wordlist)):
            words = []
            print_message("Reading the list... ")
            file = open(args.wordlist)
            for line in file.readlines():
                words.append(line.strip())
            file.close()
            count_paths = locale.format("%d", len(words), grouping=True)
            print_message("OK.\n\tThe selected file contains " + count_paths + " paths.\n")
            final_list = words;
            if args.extension:
                print_message("\tAdding extension " + args.extension + " ... ")
                for path in words:
                    name, extension = os.path.splitext(path)
                    if len(extension) == 0 and not name.startswith('.') and not name.endswith('.'):
                        final_list.append(path + args.extension)
                count_paths = locale.format("%d", len(final_list), grouping=True)
                print_message("OK, now the list is of " + count_paths + " paths.\n")
            print_message("Checking if " + args.target + " is online... ")
            if (is_online(args.target)):
                print_message("OK.\n")
                threads = 10
                if args.threads:
                    threads = args.threads
                print_message("Hunting using " + str(threads) + " threads!\n")
                validation_string = ""
                if args.validation:
                    validation_string = args.validation
                for portion in split_list(final_list, threads):
                    threading.Thread(target=worker, args=(args.target, portion, validation_string)).start()
            else:
                print_message("ERROR: host is down.\n")
                sys.exit()

        else:
            print_message("ERROR: wordlist can't be found.\n")
            sys.exit()

    else:
        parser.print_help()
        sys.exit()
