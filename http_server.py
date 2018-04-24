import socket
import sys
import os
from urllib.parse import urlparse
import mimetypes


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->
        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body,
    ])


def parse_request(request):

    method, uri, version = request.split("\r\n")[0].split(" ")

    if method != "GET":
        raise NotImplementedError

    return uri


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""
    return b"\r\n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"",
        b"You can't do that on this server!",
    ])


def response_not_found():
    """Returns a 404 Not Found response"""

    return b"\r\n".join([
        b"HTTP/1.1 404 Not Found",
        b"",
        b"The server can not find the requested URL",
    ])


def resolve_uri(uri):
    """
    This method should return appropriate content and a mime type.

    If the requested URI is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the URI is a file, it should return the contents of that file
    and its correct mimetype.

    If the URI does not map to a real location, it should raise a
    NameError that the server can catch to return a 404 response.

    Ex:
        resolve_uri('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        resolve_uri('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        resolve_uri('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        resolve_uri('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """

    webroot = 'webroot'
    resource_requested = urlparse(uri).path
    file_path = webroot + resource_requested

    # if file requested is a directory list the files in the directory
    # and append a '/' to any files listed that are directories
    if os.path.isdir(file_path):
        listing = os.listdir(file_path)
        content = []
        for name in listing:
            if os.path.isdir(webroot + '/' + name):
                name += '/'
            content.append(name)
        content1 = ', '.join(content)
        mime_type = 'text/plain'
        return content1.encode('utf8'), mime_type.encode('utf8')

    # if file requested is a file list the contents of the file
    if os.path.isfile(file_path):
        if "text" not in mimetypes.guess_type(file_path)[0]:
            # print('file_path = ', file_path)
            with open(file_path, 'rb') as fd:
                content = fd.readlines()
            mime_type = mimetypes.guess_type(file_path)[0]
            return str(content).encode('utf8'), mime_type.encode('utf8')
        else:
            with open(file_path, 'r') as fd:
                content = fd.readlines()
            # print("content = ", content)
            content1 = ' '.join(content)
            mime_type = mimetypes.guess_type(file_path)[0]
            return content1.encode('utf8'), mime_type.encode('utf8')
    # If file can not be found
    else:
        raise NameError


def server(log_buffer=sys.stderr):
    address = ('0.0.0.0', int(os.environ.get('PORT', 10000)))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if b'\r\n\r\n' in data:
                        break
                try:
                    uri = parse_request(request)
                    # print("uri is = ", uri, file=sys.stderr)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        body, mimetype = resolve_uri(uri)
                    # print("body ", body, file=sys.stderr)
                    except NameError:
                        response = response_not_found()
                    else:
                        response = response_ok(body=body, mimetype=mimetype)
                    # print("response = ", response)
                    # except NameError:
                    #     response = response_not_found()

                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
