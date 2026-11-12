import unittest

import build


class InlineTests(unittest.TestCase):
    def test_inline_link_with_url_text_not_nested(self):
        out = build.inline('[https://a.com](https://a.com)')
        self.assertEqual(out.count('<a '), 1, out)

    def test_inline_code_url_not_linked(self):
        self.assertEqual(build.inline('`https://api.z.ai/api/paas/v4`'),
                         '<code>https://api.z.ai/api/paas/v4</code>')

    def test_inline_bare_url_still_linked(self):
        self.assertEqual(build.inline('see https://a.com now'),
                         'see <a href="https://a.com">https://a.com</a> now')

    def test_inline_link_with_parens(self):
        out = build.inline('[w](https://en.wikipedia.org/wiki/A_(b)).')
        self.assertIn('href="https://en.wikipedia.org/wiki/A_(b)"', out)
        self.assertTrue(out.endswith('>w</a>.'), out)


if __name__ == '__main__':
    unittest.main()
