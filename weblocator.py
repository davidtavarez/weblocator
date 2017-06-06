#!/usr/bin/env python
import httplib, socket, threading, sys, argparse, traceback
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
    if len(validation) == 0:
        try:
            conn = httplib.HTTPConnection(host,80,30)
            conn.request("HEAD", path)
            status = conn.getresponse().status
            if status == 200 or status == 401 or status == 403 or status == 302:
                conn.close()
                return True
            else :
                return False
        except Exception as e:
            return None
    else :
        try:
            conn = httplib.HTTPConnection(host,80,30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                content = response.read()
                if validation not in content:
                    conn.close()
                    return True
                else :
                   return False
        except :
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


def split_list(arr, parts=1):
    return [arr[i::parts] for i in range(parts)]


def print_message(message):
    sys.stdout.write(message)
    sys.stdout.flush()


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'en_US')

    print_message(" __          __  _     _                     _              \n")
    print_message(" \ \        / / | |   | |                   | |             \n")
    print_message("  \ \  /\  / /__| |__ | |     ___   ___ __ _| |_ ___  _ __  \n")
    print_message("   \ \/  \/ / _ \ '_ \| |    / _ \ / __/ _` | __/ _ \| '__| \n")
    print_message("    \  /\  /  __/ |_) | |___| (_) | (_| (_| | || (_) | |    \n")
    print_message("     \/  \/ \___|_.__/|______\___/ \___\__,_|\__\___/|_|    \n")
    print_message("                                                            \n") 
    print_message("weblocator.py - Just a better dirbuster\n")
    print_message("Version 0.9.1\n")
    print_message("David Tavarez (davidtavarez)\n")
    print_message("https://github.com/davidtavarez/weblocator\n\n")
    
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
        print_message(" Opening Tor socket... ")
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.tor_host, int(args.tor_port), True)
        socket.socket = socks.socksocket
        socket.create_connection = create_tor_connection
        print_message("OK (" + urlopen('http://ip.42.pl/raw').read() + ").\n")

    if args.target and args.wordlist:
        if (os.path.isfile(args.wordlist)):
            words = []
            print_message(" Reading the list... ")
            file = open(args.wordlist)
            for line in file.readlines():
                words.append(line.strip())
            file.close()
            count_paths = locale.format("%d", len(words), grouping=True)
            print_message("OK.\n\tThe selected file contains " + count_paths + " paths.\n")
            final_list = words;
            if args.extension:
                print_message("\t Adding extension " + args.extension + " ... ")
                for path in words:
                    name, extension = os.path.splitext(path)
                    if len(extension) == 0 and not name.startswith('.') and not name.endswith('.'):
                        final_list.append(path + args.extension)
                count_paths = locale.format("%d", len(final_list), grouping=True)
                print_message("OK, now the list is of " + count_paths + " paths.\n")
            print_message(" Checking if " + args.target + " is online... ")
            if (is_online(args.target)):
                print_message("OK.\n")
                threads = 1
                if args.threads:
                    threads = int(args.threads)
                print_message("\n Hunting paths using " + str(threads) + " threads... just wait...\n")
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
