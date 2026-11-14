# Builds kfnxt.com into ./site from data/catalog.json (KF Ledger) + data/site.json
import json, os, re, html, shutil, datetime
E = html.escape
BASE = 'https://kfnxt.com'
OUT = 'site'
WA = '919633444789'
LEGAL = 'KF Integrated Energy Private Limited'
GST = '32AANCK0193J2ZE'
REG = '12/325, Puthuval House, Rajiv Gandhi Nagar, Pallithura, Thiruvananthapuram, Kerala 695586, India'
OFFICE = 'Al-Falah Tower, Menamkulam, Kazhakkoottam P.O., Trivandrum, Kerala 695582, India'
DEFAULT_ICON = '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'
def slug(x): return re.sub(r'[^a-z0-9]+', '-', x.lower().replace('&', 'and')).strip('-')
from urllib.parse import quote
def wa(msg): return f'https://wa.me/{WA}?text=' + quote(msg)

# ---------- data ----------
shutil.rmtree(OUT, ignore_errors=True); shutil.copytree('src/assets', OUT)
open(OUT + '/CNAME', 'w').write('kfnxt.com\n')
CAT = json.load(open('data/catalog.json')); SITE = json.load(open('data/site.json'))
hide = set(SITE.get('hide_services', []))
cats = []
for c in CAT['categories']:
    sv = [s['name'] for s in CAT['services'] if s['category_id'] == c['id'] and s['id'] not in hide]
    if not sv: continue
    o = SITE['categories'].get(c['id']) or SITE['categories'].get(c['name'], {})
    cats.append({'id': c['id'], 'name': c['name'], 'slug': slug(c['name']), 'services': sv,
                 'blurb': o.get('blurb', ', '.join(sv[:3]) + '.'), 'seo': o.get('seo_name', c['name']),
                 'icon': o.get('icon', DEFAULT_ICON)})
order = SITE.get('order', [])
cats.sort(key=lambda c: order.index(c['name']) if c['name'] in order else (order.index(c['id']) if c['id'] in order else 99))
N = len(cats)
WORDS = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve']
NW = WORDS[N] if N < len(WORDS) else str(N)

ORG = {"@context": "https://schema.org", "@type": ["LocalBusiness", "Organization"], "@id": BASE + "/#org", "name": "KFNXT",
       "legalName": LEGAL, "url": BASE + "/", "logo": BASE + "/kfnxt-logo.png", "image": BASE + "/kfnxt-logo.png",
       "telephone": "+91-9633444789", "email": "office@kfnxt.com", "taxID": GST,
       "address": {"@type": "PostalAddress", "streetAddress": "12/325, Puthuval House, Rajiv Gandhi Nagar, Pallithura", "addressLocality": "Thiruvananthapuram", "addressRegion": "Kerala", "postalCode": "695586", "addressCountry": "IN"},
       "areaServed": {"@type": "Country", "name": "India"}, "sameAs": ["https://www.linkedin.com/company/kfnxt"],
       "parentOrganization": {"@type": "Organization", "name": "KF Group"},
       "knowsAbout": [c['seo'] for c in cats],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Energy services", "itemListElement": [
           {"@type": "OfferCatalog", "name": c['seo'], "url": f"{BASE}/services/{c['slug']}",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in c['services']]} for c in cats]}}
SITEMAP = []

def head(title, desc, canon, ld):
    lds = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE}{canon}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#030B1E"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{canon}"><meta property="og:image" content="{BASE}/kfnxt-logo.png"><meta property="og:site_name" content="KFNXT"><meta property="og:locale" content="en_IN"><meta name="twitter:card" content="summary">{lds}<link rel="icon" href="/favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Exo+2:wght@600;700&family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css"></head><body>
<header class="site"><div class="wrap"><a href="/"><img src="/kfnxt-logo.png" alt="KFNXT – KF Integrated Energy Private Limited"></a>
<nav><a href="/#services">Services</a><a href="/#about">About</a><a href="/#contact">Contact</a><a class="cta" href="https://wa.me/{WA}">WhatsApp us</a></nav></div></header>
'''

FOOT = f'''<footer class="site"><div class="wrap"><div class="row">
<div><strong>{LEGAL}</strong><br>KFNXT is a brand of {LEGAL}, part of KF Group.<br>GSTIN {GST}</div>
<div><strong>Services</strong><br>{'<br>'.join(f'<a href="/services/{c["slug"]}">{E(c["name"])}</a>' for c in cats)}</div>
<div>12/325, Puthuval House, Rajiv Gandhi Nagar, Pallithura,<br>Thiruvananthapuram, Kerala 695586, India<br>Office: Al-Falah Tower, Menamkulam, Kazhakkoottam P.O., Trivandrum, Kerala 695582<br><a href="tel:+919633444789">+91 96334 44789</a> · <a href="mailto:office@kfnxt.com">office@kfnxt.com</a></div>
</div><div class="row copy"><div>© {datetime.date.today().year} {LEGAL}. All rights reserved.</div>
<div class="links"><a href="/privacy-policy">Privacy Policy</a><a href="/terms">Terms of Use</a></div></div></div></footer></body></html>
'''

def page(path, title, desc, body, ld=(), pri='0.6'):
    canon = '/' if path == 'index.html' else '/' + path[:-5]
    fn = os.path.join(OUT, path); os.makedirs(os.path.dirname(fn) or '.', exist_ok=True)
    open(fn, 'w').write(head(title, desc, canon, list(ld)) + body + FOOT)
    SITEMAP.append((canon, pri))

def card(c):
    return (f'<a class="card" href="/services/{c["slug"]}"><div class="ic"><svg viewBox="0 0 24 24">{c["icon"]}</svg></div>'
            f'<h3>{E(c["name"])}</h3><p>{E(c["blurb"])}</p><span class="more">{len(c["services"])} service{"s" if len(c["services"]) != 1 else ""} →</span></a>')

CONTACT = f'''<section id="contact"><div class="wrap"><div class="eyebrow d">Contact us</div><h2>Talk to us about <span>your energy needs</span></h2>
<div class="contact"><div class="cbox"><h3>{LEGAL}</h3><div class="legal">Brand: KFNXT · GSTIN {GST}</div><dl>
<dt>Registered office</dt><dd>{REG}</dd>
<dt>Office</dt><dd>{OFFICE}</dd>
<dt>Phone / WhatsApp</dt><dd><a href="tel:+919633444789">+91 96334 44789</a></dd>
<dt>Email</dt><dd><a href="mailto:office@kfnxt.com">office@kfnxt.com</a></dd></dl></div>
<div class="side"><p>Planning rooftop solar, a home battery or EV charging? Send us a message with your location and what you need, and our team will get back to you.</p>
<p>We work with homes, apartments, businesses and institutions across India.</p>
<div class="btns"><a class="btn primary" href="https://wa.me/{WA}">WhatsApp +91 96334 44789</a></div></div></div></div></section>
'''

# ---------- home ----------
chips = ''.join(f'<span class="chip{" l" if i % 2 else ""}">{E(c["name"])}</span>' for i, c in enumerate(cats))
home = f'''<section class="hero"><div class="wrap"><div class="eyebrow">KF Group · Integrated Energy</div>
<h1>Powering <span>What's Next</span></h1>
<p class="lead">Solar, battery storage, EV charging and smart energy solutions for homes and businesses across India.</p>
<div class="chips">{chips}</div>
<div class="btns"><a class="btn primary" href="https://wa.me/{WA}">Talk to us on WhatsApp</a><a class="btn ghost" href="#services">Our services</a></div></div></section>
<section id="about"><div class="wrap"><div class="eyebrow d">About KFNXT</div><h2>Cleaner, smarter, <span>more reliable</span> energy</h2>
<p class="sub">KFNXT is the energy brand of {LEGAL}, part of KF Group. We help homes, businesses and institutions across India move to cleaner, smarter and more reliable energy, from first assessment to installation and after-sales support.</p></div></section>
<section id="services" class="alt"><div class="wrap"><div class="eyebrow d">What we do</div><h2>{NW} ways we <span>power what's next</span></h2><div class="grid">{''.join(card(c) for c in cats)}</div></div></section>
{CONTACT}'''
page('index.html', 'KFNXT | Rooftop Solar, Battery Storage & EV Charging in Kerala – KF Integrated Energy',
     'KFNXT, the energy brand of KF Integrated Energy Private Limited: solar, battery storage, EV charging and smart energy solutions for homes and businesses across India.',
     home, [ORG], '1.0')

# ---------- one page per service category ----------
for c in cats:
    others = ' · '.join(f'<a href="/services/{o["slug"]}">{E(o["name"])}</a>' for o in cats if o is not c)
    items = ''.join(f'<li><span>{E(s)}</span><a class="btn primary sm" href="{wa("Hi KFNXT, I would like a quote for " + s + ". My location: ")}">Get a quote</a></li>' for s in c['services'])
    lead = f'{c["blurb"]} KFNXT plans, installs and supports {c["seo"].lower()} for homes, apartments, businesses and institutions in Trivandrum, across Kerala and India.'
    body = f'''<div class="page-hero"><div class="wrap"><nav class="crumbs"><a href="/">Home</a> › <a href="/#services">Services</a> › {E(c["name"])}</nav>
<div class="eyebrow" style="margin-top:14px">KFNXT · {E(c["seo"])}</div><h1>{E(c["name"])}</h1><p class="lead2">{E(lead)}</p>
<div class="btns"><a class="btn primary" href="{wa("Hi KFNXT, I am interested in " + c["name"] + ". My location: ")}">Get a free consultation</a><a class="btn ghost" href="tel:+919633444789">Call +91 96334 44789</a></div></div></div>
<section><div class="wrap"><div class="eyebrow d">What we offer</div><h2>{E(c["name"])} <span>services</span></h2>
<ul class="svc-list">{items}</ul>
<div class="steps"><div><b>1. Tell us your need</b><p>Location, building type and what you want to power.</p></div><div><b>2. Site visit &amp; design</b><p>We assess the site and share a written proposal.</p></div><div><b>3. Installation</b><p>Our team installs and commissions the system.</p></div><div><b>4. Support</b><p>After-sales support from the same team.</p></div></div>
<p class="others"><b>Other services:</b> {others}</p></div></section>
{CONTACT}'''
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": c['seo'], "serviceType": c['name'], "description": lead,
           "provider": {"@type": "LocalBusiness", "@id": BASE + "/#org", "name": "KFNXT", "telephone": "+91-9633444789", "address": ORG['address']},
           "areaServed": {"@type": "Country", "name": "India"},
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": c['name'], "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in c['services']]}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Services", "item": BASE + "/#services"},
              {"@type": "ListItem", "position": 3, "name": c['name']}]}]
    page(f'services/{c["slug"]}.html', f'{c["seo"]} in Trivandrum, Kerala & India | KFNXT', lead[:300], body, ld, '0.8')

# ---------- legal ----------
for path, title, src in [('privacy-policy.html', 'Privacy Policy', 'privacy.html'), ('terms.html', 'Terms of Use', 'terms.html')]:
    body = f'<div class="page-hero"><div class="wrap"><div class="eyebrow">KFNXT · {LEGAL}</div><h1>{title}</h1><p>Last updated: 13 November 2026</p></div></div><article class="legal">{open("src/content/" + src).read()}</article>'
    page(path, f'{title} | KFNXT – KF Integrated Energy Pvt Ltd', f'{title} of {LEGAL} (KFNXT).', body, [], '0.3')

today = datetime.date.today().isoformat()
open(OUT + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n' for u, p in SITEMAP) + '</urlset>\n')
open(OUT + '/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
print('kfnxt built:', len(cats), 'categories,', sum(len(c['services']) for c in cats), 'services,', len(SITEMAP), 'urls')
