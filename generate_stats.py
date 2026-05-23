import json
import urllib.request

NS = 'my-geocache-series-2025'

def fetch(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())

found_data  = fetch(f'https://api.counterapi.dev/v1/{NS}/found')
failed_data = fetch(f'https://api.counterapi.dev/v1/{NS}/failed')

found  = found_data.get('count', 0)
failed = failed_data.get('count', 0)
total  = found + failed
rate   = round(found / total * 100) if total > 0 else 0
bar_w  = round(312 * rate / 100)

bar_fill = f'<rect x="24" y="132" width="{bar_w}" height="4" rx="2" fill="url(#barGrad)"/>' if bar_w > 0 else ''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="160">
  <defs>
    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#4ade80" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#4ade80" stop-opacity="1"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="360" height="160" rx="18" fill="#080f0c"/>
  <rect x="0.5" y="0.5" width="359" height="159" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.09" stroke-width="1"/>

  <!-- Title -->
  <text x="24" y="36" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#4b7a62" letter-spacing="1.5">&#x1F512; BONUS CACHE CHECKER  &#x2192;</text>

  <!-- Found number -->
  <text x="24" y="90" font-family="Courier New, Courier, monospace" font-size="42" font-weight="700" fill="#4ade80">{found}</text>

  <!-- Failed number -->
  <text x="188" y="90" font-family="Courier New, Courier, monospace" font-size="42" font-weight="700" fill="#f87171">{failed}</text>

  <!-- Labels -->
  <text x="24" y="106" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#4ade80" fill-opacity="0.55" letter-spacing="1">&#x2713; SOLVED</text>
  <text x="188" y="106" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#f87171" fill-opacity="0.5" letter-spacing="1">&#x2717; FAILED</text>

  <!-- Bar meta -->
  <text x="24" y="126" font-family="Courier New, Courier, monospace" font-size="9" fill="#2e5540" letter-spacing="0.5">SUCCESS RATE</text>
  <text x="336" y="126" font-family="Courier New, Courier, monospace" font-size="9" fill="#4ade80" text-anchor="end">{rate}%</text>

  <!-- Bar track -->
  <rect x="24" y="132" width="312" height="4" rx="2" fill="#ffffff" fill-opacity="0.05"/>

  <!-- Bar fill -->
  {bar_fill}
</svg>'''

with open('stats.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print(f'Done: {found} found, {failed} failed, {rate}% success rate')
