from flask import Flask, request, render_template_string
import scraper

app = Flask(__name__)

TRENDING = [
    "Jio Fiber",
    "boAt Airdopes",
    "Zomato",
    "BYJU'S",
    "OYO Rooms",
    "Redmi",
    "Ola"
]

CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0b0b0c;
    color: #ffffff;
    line-height: 1.6;
}

a {
    color: inherit;
}

.wrap {
    max-width: 1020px;
    margin: 0 auto;
    padding: 32px 20px 70px;
}

.home-wrap {
    min-height: 100vh;
    display: flex;
    align-items: center;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    gap: 16px;
    flex-wrap: wrap;
}

.nav-left {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.logo {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -1px;
    text-decoration: none;
}

.tagline {
    color: #7a7a7a;
    font-size: 14px;
}

.top-links {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.top-link {
    display: inline-block;
    padding: 8px 12px;
    border-radius: 999px;
    border: 1px solid #242424;
    background: #121214;
    color: #d8d8d8;
    text-decoration: none;
    font-size: 12px;
}

.top-link:hover {
    border-color: #4a4a4a;
    color: #fff;
}

.hero-title {
    font-size: 46px;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 12px;
}

.hero-sub {
    color: #b0b0b0;
    font-size: 16px;
    line-height: 1.8;
    max-width: 760px;
    margin-bottom: 26px;
}

.search-form {
    display: flex;
    gap: 10px;
    width: 100%;
    margin: 24px 0 14px;
}

.search-form input {
    flex: 1;
    padding: 15px 18px;
    border-radius: 14px;
    border: 1px solid #232323;
    background: #151517;
    color: #fff;
    font-size: 15px;
    outline: none;
}

.search-form input:focus {
    border-color: #4a4a4a;
}

.btn {
    padding: 15px 20px;
    border-radius: 14px;
    border: none;
    background: #ffffff;
    color: #000000;
    font-weight: 700;
    cursor: pointer;
    font-size: 14px;
    white-space: nowrap;
    text-decoration: none;
    display: inline-block;
}

.btn:hover {
    background: #e9e9e9;
}

.hint {
    color: #555;
    font-size: 13px;
    margin-bottom: 26px;
}

.loc-row {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #666;
    font-size: 13px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.loc-btn {
    background: transparent;
    border: 1px solid #2a2a2a;
    color: #aaa;
    border-radius: 999px;
    padding: 7px 12px;
    cursor: pointer;
    font-size: 12px;
}

.loc-btn:hover {
    border-color: #555;
    color: #fff;
}

.trending-title {
    color: #666;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tag {
    display: inline-block;
    padding: 8px 14px;
    border: 1px solid #242424;
    border-radius: 999px;
    color: #cfcfcf;
    text-decoration: none;
    font-size: 13px;
    background: #121214;
}

.tag:hover {
    border-color: #4a4a4a;
    color: #fff;
}

.card {
    background: #141416;
    border: 1px solid #242424;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.product-name {
    font-size: 36px;
    font-weight: 900;
    margin-bottom: 8px;
    letter-spacing: -1px;
}

.subtle {
    color: #777;
    font-size: 13px;
}

.score-row {
    display: flex;
    gap: 24px;
    align-items: center;
}

.score-circle {
    width: 130px;
    height: 130px;
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
}

.score-num {
    font-size: 44px;
    font-weight: 900;
    line-height: 1;
}

.score-out-of {
    font-size: 12px;
    color: #888;
    margin-top: 6px;
    letter-spacing: 1px;
}

.verdict-label {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 10px;
}

.verdict-big {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}

.based-on {
    color: #b8b8b8;
    font-size: 15px;
    margin-bottom: 14px;
    line-height: 1.7;
}

.meter {
    width: 100%;
    max-width: 360px;
    height: 10px;
    background: #1f1f1f;
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 8px;
}

.meter-fill {
    height: 100%;
    border-radius: 999px;
}

.meter-labels {
    display: flex;
    justify-content: space-between;
    max-width: 360px;
    font-size: 11px;
    color: #555;
    margin-bottom: 14px;
}

.signal-pill {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

.stats-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 14px;
}

.stat-card {
    background: #101113;
    border: 1px solid #202225;
    border-radius: 16px;
    padding: 20px;
}

.stat-num {
    font-size: 28px;
    font-weight: 900;
    margin-bottom: 6px;
}

.stat-label {
    color: #666;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}

.grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 18px;
}

.section-title {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8a8a8a;
    margin-bottom: 14px;
}

.list-item {
    padding: 10px 0;
    border-bottom: 1px solid #232323;
    color: #d7d7d7;
    font-size: 14px;
}

.list-item:last-child {
    border-bottom: none;
}

.voice {
    padding: 12px 0;
    border-bottom: 1px solid #232323;
    color: #c2c2c2;
    font-size: 14px;
    font-style: italic;
}

.voice:last-child {
    border-bottom: none;
}

.reco-box {
    display: grid;
    grid-template-columns: 180px 1fr;
    gap: 20px;
    align-items: start;
}

.reco-label {
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #777;
    margin-bottom: 10px;
}

.reco-badge {
    display: inline-block;
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 14px;
    font-weight: 800;
}

.reco-text {
    color: #bcbcbc;
    font-size: 14px;
    line-height: 1.8;
}

.alt-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}

.alt-name {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.alt-score {
    background: #17361d;
    color: #6ef08c;
    border: 1px solid #255130;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
}

.alt-reason {
    color: #b7b7b7;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 20px;
}

.compare-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 18px;
}

.compare-card {
    background: #101113;
    border: 1px solid #202225;
    border-radius: 16px;
    padding: 18px;
}

.compare-card.good {
    border-color: #29402d;
}

.compare-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.compare-name {
    font-size: 17px;
    font-weight: 800;
}

.compare-pill {
    font-size: 12px;
    font-weight: 800;
    padding: 5px 12px;
    border-radius: 999px;
}

.buy-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 14px;
}

.buy-btn {
    display: inline-block;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 800;
    text-decoration: none;
}

.amazon {
    background: #FF9900;
    color: #000;
}

.flipkart {
    background: #2874F0;
    color: #fff;
}

.neutral-btn {
    background: #1b1b1d;
    color: #fff;
    border: 1px solid #2a2a2a;
}

.disclosure {
    color: #666;
    font-size: 12px;
    margin-top: 12px;
}

.source-links {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}

.source-link {
    display: inline-block;
    padding: 10px 14px;
    border-radius: 10px;
    background: #1b1b1d;
    color: #fff;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid #2a2a2a;
}

.source-link:hover {
    border-color: #4a4a4a;
}

.monetize-box {
    background: linear-gradient(135deg, #141416 0%, #101012 100%);
    border: 1px solid #2a2a2a;
}

.monetize-title {
    font-size: 16px;
    font-weight: 800;
    color: #fff;
    margin-bottom: 8px;
}

.monetize-sub {
    color: #aaa;
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 14px;
}

.ad-slot {
    background: #101113;
    border: 1px dashed #313131;
    border-radius: 14px;
    padding: 18px;
    color: #666;
    font-size: 13px;
    text-align: center;
}

.faq-q {
    color: #fff;
    font-weight: 700;
    margin-bottom: 8px;
    font-size: 14px;
}

.faq-a {
    color: #9f9f9f;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 18px;
}

.page-title {
    font-size: 34px;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 10px;
}

.page-sub {
    color: #a9a9a9;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 24px;
    max-width: 780px;
}

.footer {
    margin-top: 28px;
    color: #555;
    font-size: 12px;
    text-align: center;
}

@media (max-width: 900px) {
    .grid-3 {
        grid-template-columns: 1fr;
    }

    .stats-row {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 700px) {
    .grid-2,
    .compare-grid {
        grid-template-columns: 1fr;
    }

    .score-row {
        flex-direction: column;
        align-items: flex-start;
    }

    .reco-box {
        grid-template-columns: 1fr;
    }

    .product-name {
        font-size: 28px;
    }

    .logo {
        font-size: 34px;
    }

    .hero-title {
        font-size: 34px;
    }

    .search-form {
        flex-direction: column;
    }

    .score-circle {
        width: 110px;
        height: 110px;
    }

    .score-num {
        font-size: 38px;
    }
}
"""

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>VETO — Your Final Say Before Buying</title>
    <meta name="description" content="Check structured product truth before buying. See complaints, positives, alternatives, and decision guidance.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{{ css|safe }}</style>
</head>
<body>
<div class="wrap home-wrap">
    <div style="width:100%;">
        <div class="nav" style="margin-bottom:36px;">
            <div class="nav-left">
                <div class="logo">VETO</div>
                <div class="tagline">Your Final Say Before Buying</div>
            </div>
            <div class="top-links">
                <a class="top-link" href="/about">About</a>
                <a class="top-link" href="/methodology">Methodology</a>
                <a class="top-link" href="/faq">FAQ</a>
                <a class="top-link" href="/privacy">Privacy</a>
                <a class="top-link" href="/disclaimer">Disclaimer</a>
            </div>
        </div>

        <div class="hero-title">
            Check the truth before you spend money.
        </div>
        <div class="hero-sub">
            VETO turns scattered complaints, praise signals, and public sentiment into a simple buying decision:
            buy, buy with caution, avoid, or wait.
        </div>

        <form action="/check" method="get" class="search-form">
            <input
                type="text"
                name="q"
                placeholder="Type product or service name..."
                autocomplete="off"
                autofocus
            >
            <button type="submit" class="btn">Check Truth →</button>
        </form>

        <div class="hint">
            Try: Jio Fiber · boAt Airdopes · Zomato · BYJU'S · OYO Rooms · Redmi · Ola
        </div>

        <div class="loc-row">
            <span>📍</span>
            <span id="locText">Location not set</span>
            <button class="loc-btn" onclick="getLoc()">Allow Location</button>
        </div>

        <div class="grid-3" style="margin-bottom:24px;">
            <div class="card" style="margin-bottom:0;">
                <div class="section-title">Trust Signal</div>
                <div class="monetize-title">Decisive Recommendation</div>
                <div class="monetize-sub">
                    You don’t just get random opinions — you get a clear buying recommendation.
                </div>
            </div>
            <div class="card" style="margin-bottom:0;">
                <div class="section-title">Comparison</div>
                <div class="monetize-title">Better Alternative</div>
                <div class="monetize-sub">
                    If what you searched looks weak, VETO immediately shows a cleaner option.
                </div>
            </div>
            <div class="card" style="margin-bottom:0;">
                <div class="section-title">Verification</div>
                <div class="monetize-title">Source Check</div>
                <div class="monetize-sub">
                    Public verification links let users cross-check the wider internet conversation.
                </div>
            </div>
        </div>

        <div class="trending-title">Trending</div>
        <div class="tags">
            {% for item in trending %}
                <a class="tag" href="/check?q={{ item }}">{{ item }}</a>
            {% endfor %}
        </div>

        <div class="footer">
            No Signup · No Tracking · No BS · Made in Odisha 🇮🇳
        </div>
    </div>
</div>

<script>
function getLoc() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(pos) {
                fetch(
                    'https://nominatim.openstreetmap.org/reverse?format=json&lat='
                    + pos.coords.latitude +
                    '&lon=' + pos.coords.longitude
                )
                .then(r => r.json())
                .then(d => {
                    var city = d.address.city || d.address.town || d.address.village || 'Your area';
                    var state = d.address.state || '';
                    localStorage.setItem('city', city);
                    localStorage.setItem('state', state);
                    document.getElementById('locText').textContent = city + ', ' + state;
                });
            },
            function() {
                document.getElementById('locText').textContent = 'Location denied';
            }
        );
    }
}

window.onload = function() {
    var city = localStorage.getItem('city');
    var state = localStorage.getItem('state');
    if (city) {
        document.getElementById('locText').textContent = city + ', ' + state;
    }
}
</script>
</body>
</html>
"""

RESULT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ name }} — VETO Truth Report</title>
    <meta name="description" content="Truth report for {{ name }}. See complaint signals, positives, alternatives, and source verification before buying.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{{ css|safe }}</style>
</head>
<body>
<div class="wrap">

    <div class="nav">
        <div class="nav-left">
            <a href="/" class="logo" style="font-size:30px;">VETO</a>
            <div class="tagline">Your Final Say Before Buying</div>
        </div>
        <div class="top-links">
            <a class="top-link" href="/about">About</a>
            <a class="top-link" href="/methodology">Methodology</a>
            <a class="top-link" href="/faq">FAQ</a>
            <a class="top-link" href="/privacy">Privacy</a>
            <a class="top-link" href="/disclaimer">Disclaimer</a>
        </div>
    </div>

    <div class="card">
        <div class="product-name">{{ name }}</div>
        <div class="subtle" id="resultLoc">Independent truth report.</div>
    </div>

    <div class="card" style="background: linear-gradient(135deg, #151517 0%, #101012 100%); border: 1px solid #2a2a2a;">
        <div class="score-row">
            <div class="score-circle" style="border:3px solid {{ color }}; background: {{ color }}12; box-shadow: 0 0 30px {{ color }}18;">
                <div class="score-num" style="color: {{ color }};">{{ score }}</div>
                <div class="score-out-of">OUT OF 100</div>
            </div>

            <div style="flex:1;">
                <div class="verdict-label">Verdict Summary</div>
                <div class="verdict-big" style="color: {{ color }};">
                    {{ emoji }} {{ verdict }}
                </div>

                <div class="based-on">
                    Based on <strong style="color:#fff;">{{ complaints }}</strong> complaint signals
                    and <strong style="color:#fff;">{{ praises }}</strong> positive signals collected from structured user feedback.
                </div>

                <div class="meter">
                    <div class="meter-fill" style="width: {{ score }}%; background: {{ color }};"></div>
                </div>

                <div class="meter-labels">
                    <span>Risky</span>
                    <span>Average</span>
                    <span>Safe</span>
                </div>

                <div class="signal-pill" style="background: {{ color }}18; color: {{ color }}; border:1px solid {{ color }}33;">
                    {% if score >= 70 %}
                        Strong Buy Signal
                    {% elif score >= 40 %}
                        Mixed Public Sentiment
                    {% elif score > 0 %}
                        High Risk Choice
                    {% else %}
                        Data Not Strong Enough Yet
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-num" style="color:#ff7d7d;">{{ complaints }}</div>
            <div class="stat-label">Complaint Signals</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#79e09a;">{{ praises }}</div>
            <div class="stat-label">Positive Signals</div>
        </div>
        <div class="stat-card">
            <div class="stat-num" style="color:#d4d4d4;">{{ source_count }}</div>
            <div class="stat-label">Source Buckets</div>
        </div>
    </div>

    <div class="card">
        <div class="section-title">🎯 Final Recommendation</div>

        <div class="reco-box">
            <div>
                {% if score >= 70 %}
                    <div class="reco-label">Decision</div>
                    <div class="reco-badge" style="background:#17361d; color:#6ef08c; border:1px solid #255130;">
                        ✅ BUY
                    </div>
                {% elif score >= 40 %}
                    <div class="reco-label">Decision</div>
                    <div class="reco-badge" style="background:#3a2d12; color:#ffcc66; border:1px solid #5a4318;">
                        ⚠ BUY WITH CAUTION
                    </div>
                {% elif score > 0 %}
                    <div class="reco-label">Decision</div>
                    <div class="reco-badge" style="background:#3a1616; color:#ff7d7d; border:1px solid #5a2323;">
                        ❌ AVOID
                    </div>
                {% else %}
                    <div class="reco-label">Decision</div>
                    <div class="reco-badge" style="background:#232323; color:#bbb; border:1px solid #3a3a3a;">
                        ⏳ WAIT
                    </div>
                {% endif %}
            </div>

            <div class="reco-text">
                {% if score >= 70 %}
                    This product currently shows a strong trust signal. Public sentiment is mostly positive, complaint intensity is comparatively lower, and there is no major red-flag pattern visible in the current data.
                {% elif score >= 40 %}
                    This product has mixed public sentiment. It is not an automatic reject, but there are enough repeat complaints that you should read the pros and cons carefully before buying.
                {% elif score > 0 %}
                    This product shows a weak trust signal. Repeat complaints are strong enough that most buyers should avoid it unless they have a very specific reason to choose it.
                {% else %}
                    VETO does not yet have enough structured data to make a strong recommendation. For now, do more manual checking before spending money.
                {% endif %}
            </div>
        </div>
    </div>

    <div class="card monetize-box">
        <div class="section-title">⚡ Next Best Action</div>

        <div class="grid-3">
            <div>
                <div class="monetize-title">Check Better Option</div>
                <div class="monetize-sub">
                    If this score is weak, move directly to the recommended alternative instead of wasting more time.
                </div>
            </div>

            <div>
                <div class="monetize-title">Compare Wider Market</div>
                <div class="monetize-sub">
                    Use VETO as the first filter, then compare multiple stores and market discussions before spending.
                </div>
            </div>

            <div>
                <div class="monetize-title">Verify Public Discussion</div>
                <div class="monetize-sub">
                    Cross-check the wider internet using the source links below if you want more confidence.
                </div>
            </div>
        </div>

        <div class="buy-row">
            {% if alt_name %}
            <a class="buy-btn neutral-btn" href="#better-alternative">Jump to Better Alternative</a>
            {% endif %}
            <a class="buy-btn neutral-btn" target="_blank" href="https://www.google.com/search?q={{ name }}+best+alternative+india">Search Wider Alternatives</a>
            <a class="buy-btn neutral-btn" href="#verify-sources">Verify Sources</a>
        </div>

        <div class="disclosure">
            This block is also where future monetization can fit naturally: affiliate links, CPA offers, switch offers, and sponsored deal cards.
        </div>
    </div>

    {% if bad_points or good_points %}
    <div class="grid-2">
        {% if bad_points %}
        <div class="card">
            <div class="section-title">❌ What People Complain About</div>
            {% for point in bad_points %}
                <div class="list-item">{{ point }}</div>
            {% endfor %}
        </div>
        {% endif %}

        {% if good_points %}
        <div class="card">
            <div class="section-title">✅ What People Like</div>
            {% for point in good_points %}
                <div class="list-item">{{ point }}</div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    {% endif %}

    {% if voices %}
    <div class="card">
        <div class="section-title">🗣️ Real Voices From The Internet</div>
        {% for voice in voices %}
            <div class="voice">"{{ voice }}"</div>
        {% endfor %}
    </div>
    {% endif %}

    {% if alt_name %}
    <div class="card" id="better-alternative" style="background: linear-gradient(135deg, #141416 0%, #101012 100%); border: 1px solid #2a2a2a;">
        <div class="section-title">Better Alternative</div>

        <div class="alt-header">
            <div class="alt-name">✅ {{ alt_name }}</div>
            <div class="alt-score">{{ alt_score }}/100</div>
        </div>

        <div class="alt-reason">{{ alt_reason }}</div>

        <div class="compare-grid">
            <div class="compare-card">
                <div class="compare-top">
                    <div class="compare-name">{{ name }}</div>
                    <div class="compare-pill" style="background:#3a1616; color:#ff8a8a;">{{ score }}/100</div>
                </div>
                <div class="subtle" style="line-height:1.8;">
                    Lower trust score, heavier complaint load, and weaker public sentiment.
                </div>
            </div>

            <div class="compare-card good">
                <div class="compare-top">
                    <div class="compare-name">{{ alt_name }}</div>
                    <div class="compare-pill" style="background:#17361d; color:#6ef08c;">{{ alt_score }}/100</div>
                </div>
                <div class="subtle" style="line-height:1.8;">
                    Better public sentiment, fewer critical repeat complaints, and a cleaner recommendation profile.
                </div>
            </div>
        </div>

        <div class="grid-2" style="margin-bottom:20px;">
            {% if alt_good %}
            <div class="card" style="margin-bottom:0; background:#101113; border:1px solid #202225;">
                <div class="section-title" style="color:#56d47a;">Why It Is Better</div>
                {% for point in alt_good %}
                    <div class="list-item">{{ point }}</div>
                {% endfor %}
            </div>
            {% endif %}

            {% if alt_bad %}
            <div class="card" style="margin-bottom:0; background:#101113; border:1px solid #202225;">
                <div class="section-title" style="color:#ff6a6a;">Known Drawbacks</div>
                {% for point in alt_bad %}
                    <div class="list-item">{{ point }}</div>
                {% endfor %}
            </div>
            {% endif %}
        </div>

        <div class="buy-row">
            {% if amazon %}
            <a class="buy-btn amazon" target="_blank" href="https://www.amazon.in/s?k={{ amazon }}">Open on Amazon</a>
            {% endif %}
            {% if flipkart %}
            <a class="buy-btn flipkart" target="_blank" href="https://www.flipkart.com/search?q={{ flipkart }}">Open on Flipkart</a>
            {% endif %}
            <a class="buy-btn neutral-btn" target="_blank" href="https://www.google.com/search?q={{ alt_name }}+price+india">Check Wider Prices</a>
        </div>

        <div class="disclosure">
            * Affiliate tags can be inserted here later. For now these are clean outgoing search links.
        </div>
    </div>
    {% endif %}

    <div class="card" id="verify-sources">
        <div class="section-title">📎 Verify Sources</div>

        <div class="source-links">
            <a class="source-link" target="_blank" href="https://www.google.com/search?q={{ name }}+reviews+india">Google</a>
            <a class="source-link" target="_blank" href="https://www.google.com/search?q=site:youtube.com+{{ name }}+review">YouTube</a>
            <a class="source-link" target="_blank" href="https://www.google.com/search?q=site:reddit.com+{{ name }}+india">Reddit</a>
            <a class="source-link" target="_blank" href="https://www.google.com/search?q={{ name }}+mouthshut">Mouthshut</a>
            <a class="source-link" target="_blank" href="https://www.google.com/search?q={{ name }}+trustpilot">Trustpilot</a>
        </div>

        <div class="disclosure">
            Cross-check the public discussion yourself. VETO gives a structured summary — these links help users verify the wider internet conversation.
        </div>
    </div>

    <div class="card monetize-box">
        <div class="section-title">💰 Monetization Ready Section</div>

        <div class="grid-3">
            <div class="ad-slot">
                Future AdSense / native ad slot
            </div>
            <div class="ad-slot">
                Future CPA offer / switch offer block
            </div>
            <div class="ad-slot">
                Future sponsored comparison slot
            </div>
        </div>

        <div class="disclosure">
            Realistic money channels here are: ad views/clicks, CPA actions, installs, signups, or purchases.
            You generally do not get meaningful money only because someone merely visits a normal affiliate link.
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <div class="section-title">🔬 How VETO Works</div>
            <div class="subtle" style="line-height:1.9;">
                VETO turns scattered user sentiment into a structured decision view.
                We do not take money from brands to boost scores.
                If we recommend poorly, users stop trusting us — so honesty is the core business model.
            </div>
        </div>

        <div class="card">
            <div class="section-title">❓ FAQ</div>
            <div class="faq-q">Can I trust this score blindly?</div>
            <div class="faq-a">Use it as a decision shortcut, then verify using the source links if the purchase is expensive.</div>

            <div class="faq-q">Does VETO get paid to praise brands?</div>
            <div class="faq-a">No. The design is built so monetization works through traffic, deals, CPA, and affiliate systems — not score manipulation.</div>

            <div class="faq-q">Why show a better alternative?</div>
            <div class="faq-a">Because people don’t just want complaints — they want the next best move.</div>
        </div>
    </div>

    <div class="footer">
        VETO — Your Final Say Before Buying · Made in Odisha 🇮🇳
        <br><br>
        <a href="/" style="color:#777; text-decoration:none;">← Back to Home</a>
    </div>
</div>

<script>
window.onload = function() {
    var city = localStorage.getItem('city');
    var state = localStorage.getItem('state');
    if (city) {
        document.getElementById('resultLoc').textContent =
            'Independent truth report for ' + city + ', ' + state + '.';
    }
}
</script>
</body>
</html>
"""

SIMPLE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} — VETO</title>
    <meta name="description" content="{{ desc }}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{{ css|safe }}</style>
</head>
<body>
<div class="wrap">
    <div class="nav">
        <div class="nav-left">
            <a href="/" class="logo" style="font-size:30px;">VETO</a>
            <div class="tagline">Your Final Say Before Buying</div>
        </div>
        <div class="top-links">
            <a class="top-link" href="/about">About</a>
            <a class="top-link" href="/methodology">Methodology</a>
            <a class="top-link" href="/faq">FAQ</a>
            <a class="top-link" href="/privacy">Privacy</a>
            <a class="top-link" href="/disclaimer">Disclaimer</a>
        </div>
    </div>

    <div class="card">
        <div class="page-title">{{ title }}</div>
        <div class="page-sub">{{ desc }}</div>
    </div>

    <div class="card">
        {{ content|safe }}
    </div>

    <div class="footer">
        VETO — Your Final Say Before Buying · Made in Odisha 🇮🇳
        <br><br>
        <a href="/" style="color:#777; text-decoration:none;">← Back to Home</a>
    </div>
</div>
</body>
</html>
"""

def render_simple_page(title, desc, content):
    return render_template_string(
        SIMPLE_PAGE,
        css=CSS,
        title=title,
        desc=desc,
        content=content
    )

@app.route("/")
def home():
    return render_template_string(
        HOME_HTML,
        css=CSS,
        trending=TRENDING
    )

@app.route("/check")
def check():
    q = request.args.get("q", "").strip()
    if not q:
        return home()

    data = scraper.analyze(q)
    sources = data.get("sources", [])

    return render_template_string(
        RESULT_HTML,
        css=CSS,
        name=data.get("name", q.title()),
        score=data.get("score", 0),
        verdict=data.get("verdict", "NO DATA"),
        emoji=data.get("emoji", "⚪"),
        color=data.get("color", "#666666"),
        complaints=data.get("complaints", 0),
        praises=data.get("praises", 0),
        bad_points=data.get("bad_points", []),
        good_points=data.get("good_points", []),
        voices=data.get("voices", []),
        alt_name=data.get("alt_name", ""),
        alt_score=data.get("alt_score", 0),
        alt_reason=data.get("alt_reason", ""),
        alt_good=data.get("alt_good", []),
        alt_bad=data.get("alt_bad", []),
        amazon=data.get("amazon", ""),
        flipkart=data.get("flipkart", ""),
        source_count=len(sources)
    )

@app.route("/about")
def about():
    content = """
    <div class="faq-q">What is VETO?</div>
    <div class="faq-a">
        VETO is a decision-support platform for buyers. It turns scattered public complaints and positive signals
        into a simple outcome: buy, buy with caution, avoid, or wait.
    </div>

    <div class="faq-q">Why does VETO exist?</div>
    <div class="faq-a">
        Most people do not want to read hundreds of reviews. They want clarity. VETO is built to reduce buying regret.
    </div>

    <div class="faq-q">Who is it for?</div>
    <div class="faq-a">
        Anyone who wants a faster and cleaner decision before spending money on a product or service.
    </div>
    """
    return render_simple_page(
        "About VETO",
        "Why VETO exists and what problem it solves.",
        content
    )

@app.route("/methodology")
def methodology():
    content = """
    <div class="faq-q">How does VETO create a result?</div>
    <div class="faq-a">
        VETO uses structured complaint and praise patterns stored in a decision-ready format.
        The goal is not to replace full manual research, but to compress it into a strong first decision layer.
    </div>

    <div class="faq-q">Does a brand pay to increase its score?</div>
    <div class="faq-a">
        No. The model is designed so monetization comes from traffic, ads, CPA, and affiliate systems — not score manipulation.
    </div>

    <div class="faq-q">Should expensive purchases still be manually verified?</div>
    <div class="faq-a">
        Yes. That is why source verification links are included on result pages.
    </div>
    """
    return render_simple_page(
        "Methodology",
        "How VETO forms structured verdicts.",
        content
    )

@app.route("/privacy")
def privacy():
    content = """
    <div class="faq-q">Do we store your searches?</div>
    <div class="faq-a">
        This local version of VETO does not require signup and does not ask for personal identity information.
    </div>

    <div class="faq-q">What about location?</div>
    <div class="faq-a">
        Location is optional and handled in your browser for display personalization. It is not required to use the tool.
    </div>

    <div class="faq-q">Do we sell personal user data?</div>
    <div class="faq-a">
        No personal data sales are part of the intended trust model.
    </div>
    """
    return render_simple_page(
        "Privacy",
        "How VETO thinks about user privacy.",
        content
    )

@app.route("/disclaimer")
def disclaimer():
    content = """
    <div class="faq-q">Important Notice</div>
    <div class="faq-a">
        VETO is a structured decision-support tool, not a legal guarantee, financial advisor, or official certification authority.
    </div>

    <div class="faq-q">What should users do?</div>
    <div class="faq-a">
        Use VETO as a smart shortcut, then verify manually for high-value purchases using the public source links.
    </div>

    <div class="faq-q">What about pricing and stock?</div>
    <div class="faq-a">
        External store links can change prices, stock, or offers without notice.
    </div>
    """
    return render_simple_page(
        "Disclaimer",
        "Important limitations and practical use guidance.",
        content
    )

@app.route("/faq")
def faq():
    content = """
    <div class="faq-q">Can I trust the score blindly?</div>
    <div class="faq-a">
        Not blindly. Use it as a decision shortcut, especially for fast filtering. For expensive purchases, verify manually too.
    </div>

    <div class="faq-q">Why does VETO show alternatives?</div>
    <div class="faq-a">
        Because users do not just want to know what is bad — they want to know what to do next.
    </div>

    <div class="faq-q">Can VETO earn money later?</div>
    <div class="faq-a">
        Yes. Through ads, CPA, deal widgets, and affiliate systems — without needing to sell scores.
    </div>
    """
    return render_simple_page(
        "FAQ",
        "Quick answers about VETO usage and trust.",
        content
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)