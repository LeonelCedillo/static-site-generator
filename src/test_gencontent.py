import unittest
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")


    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")


    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")


    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass


    def test_extract_title_fail(self):
        md = """
## This is the title of the page

## This is not the title
"""
        # Expecting an exception because there is no H1
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 found")



if __name__ == "__main__":
    unittest.main()



