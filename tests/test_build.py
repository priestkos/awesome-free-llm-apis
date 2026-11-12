import io
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import build


README = '''<p align="center">LLM APIs with permanent free tiers for text inference.</p>
<p align="center"><sub>Most providers offer an OpenAI-compatible endpoint.</sub></p>
<p align="center"><sub>Unrelated promotional text.</sub></p>
## Provider APIs
### [Cohere](https://example.com/keys) 🇨🇦
Free trial.

Native API base URL: `https://example.com/native`

OpenAI-compatible base URL: `https://example.com/openai`

| Model | Context |
| --- | --- |
| sample | 128K |
## Inference providers
### [Example](https://example.org/keys) 🇺🇸
Free tier.

Base URL: `https://example.org/v1`
## Glossary
| Term | Meaning |
| --- | --- |
| RPM | Requests per minute |
## Contributing
Contribute here.
'''


class BuildTests(unittest.TestCase):
    def build(self, readme):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            (root / 'template.html').write_text('%%COVER%%\n%%BODY%%\n%%FOOTNOTES%%', encoding='utf-8')
            with patch.object(build, 'HERE', root), patch.object(
                build.urllib.request, 'urlopen', return_value=io.BytesIO(readme.encode('utf-8'))
            ):
                build.main()
            return (root / 'index.html').read_text(encoding='utf-8')

    def test_current_source_preamble_and_both_base_urls_are_rendered(self):
        output = self.build(README.replace('\n', '\r\n'))
        self.assertIn('Most providers offer an OpenAI-compatible endpoint.', output)
        self.assertNotIn('Unrelated promotional text.', output)
        self.assertIn('Native API base URL', output)
        self.assertIn('OpenAI-compatible base URL', output)
        self.assertIn('data-url>https://example.com/native</code>', output)
        self.assertIn('data-url>https://example.com/openai</code>', output)
        self.assertIn('data-url>https://example.org/v1</code>', output)

    def test_missing_base_url_fails_loudly(self):
        without_urls = README.replace('Base URL: `https://example.org/v1`', 'No endpoint available.')
        with self.assertRaisesRegex(AssertionError, 'no Base URL in Example'):
            self.build(without_urls)

    def test_previous_preamble_still_works(self):
        old = README.replace('Most providers offer an OpenAI-compatible endpoint.',
                             'All endpoints are OpenAI SDK-compatible unless noted.')
        old = old.replace('Native API base URL: `https://example.com/native`\n\n'
                          'OpenAI-compatible base URL: `https://example.com/openai`',
                          'Base URL: `https://example.com/native`')
        output = self.build(old)
        self.assertIn('All endpoints are OpenAI SDK-compatible unless noted.', output)
        self.assertIn('data-url>https://example.com/native</code>', output)

    def test_footnotes_rendered_and_referenced(self):
        readme = README.replace('Free trial.', 'Free trial.[^1]') + '[^1]: Needs a card.\n'
        out = self.build(readme)
        self.assertIn('href="#fn-1"', out)
        self.assertIn('id="fn-1"', out)
        self.assertIn('Needs a card.', out)

    def test_glossary_table_rendered(self):
        out = self.build(README)
        self.assertIn('<td>RPM</td><td>Requests per minute</td>', out)

    def test_colliding_provider_slugs_get_unique_ids(self):
        out = self.build(README.replace('[Example]', '[Cohere]'))
        self.assertEqual(out.count('id="p-cohere"'), 1)
        self.assertIn('id="p-cohere-2"', out)


if __name__ == '__main__':
    unittest.main()
