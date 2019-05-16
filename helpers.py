import httplib
import sys
import socket


def split_list(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def print_message(message):
    sys.stdout.write(message)
    sys.stdout.flush()


def is_online(host):
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return False
    return True


def is_path_available(host, url_path="/", port=80, http=True, validation=None):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/70.0.3538.77 Safari/537.36 '
    valid = False
    conn = httplib.HTTPConnection(host=host, port=port) if http else httplib.HTTPSConnection(host=host, port=port)
    method = 'HEAD' if not validation else 'GET'
    protocol = 'http' if http else 'https'
    full_url = "{}://{}:{}/{}".format(protocol, host, port, url_path)
    conn.request(method=method, url=full_url, headers={'User-Agent': user_agent})
    response = conn.getresponse()
    if response.status in [200, 401, 403, 302]:
        if method == 'HEAD':
            valid = True
        elif method == 'GET':
            content = response.read()
            if validation not in content:
                valid = True
    conn.close()
    return valid
