import os
from urllib.parse import urlparse
import mimetypes


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
            return content, mime_type.encode('utf8')
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


    # if file requested can not be found

# if __name__ == '__main__':
#     print(resolve_uri('/sample.txt'))
