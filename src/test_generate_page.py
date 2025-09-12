import unittest
from markdown_blocks import markdown_to_blocks
from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is the title of the page

## This is not the title

- This is a list
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is the title of the page",
        )

    
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
