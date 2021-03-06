import http_server as server
import unittest


class test_uri(unittest.TestCase):

    def test_resolve_uri_root_is_listing_of_webroot(self):
        result = server.resolve_uri('/')
        assert b'images/' in result[0]
        assert b'text/plain' in result[1]

    def test_resolve_uri_file(self):
        result = server.resolve_uri('/sample.txt')
        assert b'This is a very simple text file.\n' in result[0]

    def test_resolve_uri_directory(self):
        result = server.resolve_uri('/images')
        assert b'Sample_Scene_Balls.jpg' in result[0]

    def test_resolve_uri_file_not_found(self):
        with self.assertRaises(NameError):
            server.resolve_uri('/file_not_found')


if __name__ == '__main__':
    unittest.main()
