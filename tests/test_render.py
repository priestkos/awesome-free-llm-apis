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


class TableTests(unittest.TestCase):
    def test_only_first_table_in_block(self):
        lines = ['| A | B |', '| --- | --- |', '| 1 | 2 |', '', 'note', '',
                 '| X | Y |', '| --- | --- |', '| 3 | 4 |']
        head, body = build.parse_table(lines)
        self.assertEqual(head, ['A', 'B'])
        self.assertEqual(body, [['1', '2']])

    def test_escaped_pipe_stays_in_cell(self):
        _, body = build.parse_table(['| A | B |', '| --- | --- |', r'| `a\|b` | 2 |'])
        self.assertEqual(body, [['`a|b`', '2']])


if __name__ == '__main__':
    unittest.main()
