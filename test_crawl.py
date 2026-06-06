import unittest
from crawl import normalize_url, get_h1_from_html


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def get_h1_from_html(self):
        html = """
        <html>
            <body>
                <h1>Test</h1>
            </body>
        </html>
        """
        actual = get_h1_from_html(html)
        expected = "Test"
        self.assertEqual(actual, expected)

        html = """
        <html>
            <body>
                <p>Test</p>
            </body>
        </html>
        """
        actual = get_h1_from_html(html)
        expected = None
        self.assertEqual(actual, expected)

        html = """
        <html>
            <body>
                <h1>Test1</h1>
                <h1>Test2</h1>
            </body>
        </html>
        """
        actual = get_h1_from_html(html)
        expected = "Test1"
        self.assertEqual(actual, expected)
    

if __name__ == "__main__":
    unittest.main()