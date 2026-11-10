"""Builds index.html: the page template in src/ with the event data from data/ inlined."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent
story = json.loads((R / 'data' / 'story.json').read_text(encoding='utf-8'))
page = (R / 'src' / 'page.html').read_text(encoding='utf-8')
assert '/*DATA*/' in page
(R / 'index.html').write_text(page.replace('/*DATA*/', json.dumps(story, ensure_ascii=False, separators=(',', ':'))), encoding='utf-8')
print('index.html', round((R / 'index.html').stat().st_size / 1024), 'KB')
