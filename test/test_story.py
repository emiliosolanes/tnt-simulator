"""Invariants of the storyline and guards on what the public page may contain. Run: python3 test/test_story.py"""
import json, pathlib, re
R = pathlib.Path(__file__).resolve().parents[1]
s = json.loads((R / 'data' / 'story.json').read_text(encoding='utf-8'))
page = (R / 'index.html').read_text(encoding='utf-8')
readme = (R / 'README.md').read_text(encoding='utf-8')
FAMS = {'Shipment', 'Transport', 'Equipment', 'IoT', 'Reefer'}

assert len(s) == 132, len(s)
assert [e['seq'] for e in s] == list(range(1, 133)), 'events numbered in page order'
assert {e['family'] for e in s} == FAMS
assert {e['status'] for e in s} <= {'Planned', 'Estimated', 'Actual'}
assert all(b['utc'] >= a['utc'] for a, b in zip(s, s[1:])), 'events in time order'
assert all(e['laden'] in (True, False, None) for e in s)
# the ten key moments in the page point at real events
moments = [int(x) for x in re.findall(r"\{ seq: (\d+), title:", page)]
assert len(moments) == 10 and all(any(e['xl'] == m for e in s) for m in moments), moments
# manifest filed 24 h or more before loading in Rotterdam
X = lambda xl: next(e for e in s if e['xl'] == xl)
assert X(56)['utc'] - X(52)['utc'] >= 24 * 3600
# the page must not carry company names, message payloads or API field names
for txt, name in ((page, 'index.html'), (json.dumps(s, ensure_ascii=False), 'story.json'), (readme, 'README.md')):
    for w in ('Maersk', 'APM', 'Walmart', 'CSX', 'Hutchison', 'ExpressRail'):
        assert w not in txt, f'{w} in {name}'
    for f in ('eventRouting', 'eventClassifierCode', 'transportCall', 'equipmentReference', 'carrierBookingReference', 'transportDocumentReference', 'shipmentDetails', 'reeferDetails', 'iotDetails'):
        assert f not in txt, f'{f} in {name}'
    assert '—' not in txt, f'em dash in {name}'
assert 'Simulated data. Personal project, not affiliated with the companies shown.' in page
assert 'by emilio.solanes' in page
print('ok:', len(s), 'events,', len(moments), 'moments')
