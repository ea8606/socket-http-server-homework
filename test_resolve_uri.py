import unittest
from resolve_uri import resolve_uri


class Test_uri(unittest.TestCase):
    def test_resolve_uri_directory(self):
        """
        Use a directory as an input to resolve_uri()
        """
        result = resolve_uri('/')
        assert 'images/' in result[0].decode('utf8')
        assert result[1].decode() == 'text/plain'

    def test_resolve_uri_binary_file(self):
        """
        Use a binary file as an input to resolve_uri
        """
        result = resolve_uri('/images/JPEG_example.jpg')
        assert type(result[0]) == list
        assert result[1].decode() == 'image/jpeg'

    def test_resolve_uri_text_file(self):
        """
        Use a text file as input to resolve_uri
        """
        result = resolve_uri('/sample.txt')
        assert 'This is a very' in result[0].decode('utf8')
        assert result[1].decode() == 'text/plain'

    def test_resolve_uri_file_not_found(self):
        with self.assertRaises(NameError):
            resolve_uri('file_not_found')


if __name__ == '__main__':
    unittest.main()
