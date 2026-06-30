#!/usr/bin/env python3
"""
ITS Architecture Wiki Builder

Reads a processed_content.json file (from any ITS architecture produced by
content_processor.py or equivalent) and generates a set of markdown wiki pages
that an LLM can use as a pre-synthesized knowledge layer.

The output is a small collection of markdown files (~20-30 pages) organized by
ARC-IT service area. Each page summarizes what elements, stakeholders, service
packages, interfaces, and functional requirements exist in that domain —
relationships that would otherwise require the LLM to discover by searching
through thousands of raw chunks.

Usage:
    python build_wiki.py --input processed_content.json --output wiki/
"""

import json
import os
import re
import csv
import shutil
import argparse
import sys
from collections import defaultdict

# Pull defaults from config.py (one directory up) when available.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from config import DOT_NAME, ARCHITECTURE_BASE_URL
except ImportError:
    DOT_NAME = "ITS Architecture"
    ARCHITECTURE_BASE_URL = ""

# ---------------------------------------------------------------------------
# ARC-IT service package category definitions
# These are standard across all ITS architectures using the ARC-IT framework.
# Each category maps to a human-readable name and a brief description.
# ---------------------------------------------------------------------------

SP_CATEGORIES = {
    "TM": {
        "name": "Traffic Management",
        "desc": "Signal control, freeway management, traffic surveillance, incident detection, DMS, connected vehicle applications.",
        "subcategories": {
            "signal":   {"codes": ["TM01", "TM02", "TM03", "TM26"], "name": "Traffic Signal Control", "desc": "Signal timing, priority, preemption, adaptive control, signal enforcement"},
            "freeway":  {"codes": ["TM04", "TM05", "TM06"], "name": "Freeway Management", "desc": "Ramp metering, HOV/HOT, speed management, lane control"},
            "coord":    {"codes": ["TM07", "TM08"], "name": "Regional Coordination", "desc": "TMC-to-TMC coordination, cross-agency incident sharing"},
            "dissem":   {"codes": ["TM09", "TM10", "TM11", "TM13", "TM14", "TM15", "TM16"], "name": "Traffic Info Dissemination", "desc": "DMS, HAR, traveler alerts, parking info, road closure info, road use charging"},
            "cv":       {"codes": ["TM12", "TM17", "TM18", "TM19", "TM20", "TM21", "TM22", "TM23", "TM24", "TM25"], "name": "Connected Vehicle Applications", "desc": "V2I SPaT, MAP, curve warnings, work zone alerts, queue warnings, dynamic roadway warning"},
        },
    },
    "PT": {
        "name": "Public Transportation",
        "desc": "Transit vehicle tracking, scheduling, passenger info, fare collection, demand response.",
        "subcategories": {
            "ops":      {"codes": ["PT01", "PT02", "PT03", "PT04", "PT10", "PT11", "PT12", "PT13"], "name": "Transit Operations", "desc": "CAD/AVL, scheduling, passenger counting, fare collection, bus lanes, pedestrian indication, station warnings, turning warnings"},
            "info":     {"codes": ["PT05", "PT06", "PT07", "PT08", "PT09", "PT16"], "name": "Transit Traveler Info", "desc": "Real-time arrivals, trip planning, transfer coordination, route ID for visually impaired"},
            "demand":   {"codes": ["PT14", "PT15", "PT17"], "name": "Demand Response / MaaS", "desc": "Paratransit, ride-sharing, mobility-as-a-service"},
        },
    },
    "TI": {
        "name": "Traveler Information",
        "desc": "511 services, third-party apps, multimodal alerts, personalized traveler info.",
        "subcategories": {
            "all": {"codes": ["TI01", "TI02", "TI03", "TI04", "TI05", "TI06", "TI07", "TI08", "TI09"], "name": "Traveler Information Services", "desc": "511, third-party data feeds, multimodal alerts, personalized info, en-route guidance, electronic payment, personal wayfinding, travel services reservation"},
        },
    },
    "PS": {
        "name": "Public Safety",
        "desc": "Incident management, emergency response, HAZMAT, railroad crossings, security monitoring.",
        "subcategories": {
            "incident": {"codes": ["PS01", "PS02", "PS03", "PS07"], "name": "Incident & Emergency Management", "desc": "Incident detection, response coordination, HAZMAT routing, incident scene safety monitoring"},
            "safety":   {"codes": ["PS04", "PS05", "PS06", "PS08", "PS09", "PS10", "PS11", "PS12", "PS13", "PS14", "PS15"], "name": "Safety & Security Monitoring", "desc": "CCTV, wrong-way detection, bridge monitoring, rail crossings, mayday notification, vehicle emergency response, stolen vehicle recovery"},
        },
    },
    "MC": {
        "name": "Maintenance & Construction",
        "desc": "Road weather management, maintenance vehicle tracking, work zone management, infrastructure monitoring.",
        "subcategories": {
            "all": {"codes": ["MC01", "MC02", "MC03", "MC04", "MC05", "MC06", "MC07", "MC08", "MC09", "MC10", "MC11", "MC12"], "name": "Maintenance & Construction", "desc": "RWIS, AVL, work zones, infrastructure health monitoring, signal priority, one-way convoy driving"},
        },
    },
    "CVO": {
        "name": "Commercial Vehicle Operations",
        "desc": "Freight credentialing, electronic screening, HAZMAT tracking, oversize/overweight permits.",
        "subcategories": {
            "all": {"codes": ["CVO01", "CVO02", "CVO03", "CVO04", "CVO05", "CVO06", "CVO07", "CVO08", "CVO09", "CVO10", "CVO11", "CVO12", "CVO13", "CVO14", "CVO15", "CVO16", "CVO17", "CVO18", "CVO19", "CVO20", "CVO21", "CVO22"], "name": "Commercial Vehicle Operations", "desc": "Credentialing, screening, HAZMAT, fleet management, freight administration, road weather, drayage optimization, HAZMAT security, driver logs, intelligent access, speed compliance, international border"},
        },
    },
    "DM": {
        "name": "Data Management",
        "desc": "ITS data archiving, performance measurement, data warehousing.",
        "subcategories": {
            "all": {"codes": ["DM01", "DM02"], "name": "Data Management", "desc": "ITS data archiving, performance measurement, NPMRDS"},
        },
    },
    "PM": {
        "name": "Performance Management",
        "desc": "Regional planning data, scenario modeling, emissions monitoring.",
        "subcategories": {
            "all": {"codes": ["PM01", "PM02", "PM03", "PM04", "PM05", "PM06"], "name": "Performance Management", "desc": "Planning data, performance dashboards, emissions tracking, loading zone management"},
        },
    },
    "WX": {
        "name": "Weather",
        "desc": "Road weather information systems, mobile weather observations.",
        "subcategories": {
            "all": {"codes": ["WX01", "WX02", "WX03", "WX04"], "name": "Weather Services", "desc": "RWIS, mobile observations, weather alerts, spot weather impact warning, roadway micro-prediction"},
        },
    },
    "SU": {
        "name": "Support",
        "desc": "Device management, mapping, location services, communications infrastructure.",
        "subcategories": {
            "all": {"codes": ["SU01", "SU02", "SU03", "SU04", "SU05", "SU06", "SU08", "SU09", "SU10", "SU11", "SU12", "SU13", "SU14", "SU15"], "name": "Support Services", "desc": "Map management, device management, cybersecurity, communications, object registration, device certification, center/field/vehicle/personnel maintenance, remote access, VRU device transition"},
        },
    },
    "VS": {
        "name": "Vehicle Safety",
        "desc": "V2V safety, automated driving, platooning, collision avoidance.",
        "subcategories": {
            "all": {"codes": ["VS01", "VS02", "VS03", "VS04", "VS05", "VS06", "VS07", "VS08", "VS09", "VS10", "VS11", "VS12", "VS13", "VS14", "VS15", "VS16", "VS17", "VS18"], "name": "Vehicle Safety & Automation", "desc": "V2V, automated vehicles, platooning, collision avoidance, autonomous vehicle safety, basic safety, situational awareness, special vehicle alert, stop sign gap assist, road weather alert, restricted lane warnings, cooperative adaptive cruise control, METR, VRU clustering"},
        },
    },
    "ST": {
        "name": "Sustainable Transport",
        "desc": "Congestion pricing, transit incentives, emissions management.",
        "subcategories": {
            "all": {"codes": ["ST01", "ST02", "ST03", "ST04", "ST05", "ST06", "ST07", "ST08", "ST09", "ST10"], "name": "Sustainable Transport", "desc": "Congestion pricing, transit incentives, alternative fuel support, eco-traffic metering, roadside lighting, eco-lanes, eco-approach at signals, low emissions zone management"},
        },
    },
}


# ---------------------------------------------------------------------------
# ITS domain synonyms
# Common alternate terms used in the ITS industry. These are injected into
# wiki page descriptions so keyword searches match regardless of which
# terminology the user happens to use.
# ---------------------------------------------------------------------------

ITS_SYNONYMS = {
    # Sign technology
    "DMS":   ["VMS", "CMS", "dynamic message sign", "variable message sign",
              "changeable message sign", "electronic message sign", "message board"],
    "HAR":   ["highway advisory radio", "traveler advisory radio"],

    # Centers
    "TMC":   ["traffic management center", "traffic operations center", "TOC",
              "ATMS", "advanced traffic management system", "STMC",
              "transportation management center"],
    "EOC":   ["emergency operations center", "emergency management center"],
    "dispatch": ["dispatch center", "PSAP", "public safety answering point", "911 center"],

    # Signal systems
    "traffic signal": ["traffic light", "signal controller", "signal system",
                       "traffic control signal", "intersection control"],
    "TSP":   ["transit signal priority", "bus signal priority", "bus priority"],
    "EVP":   ["emergency vehicle preemption", "emergency preemption",
              "EV preemption", "fire preemption"],
    "adaptive signal": ["adaptive signal control", "ASCT", "adaptive control",
                        "real-time signal optimization", "SCOOT", "SCATS", "InSync",
                        "SynchroGreen", "Kadence"],

    # Freeway
    "ramp meter":    ["ramp metering", "ramp signal", "ramp control"],
    "HOV":           ["high occupancy vehicle", "carpool lane", "HOT",
                      "high occupancy toll", "managed lane", "express lane"],
    "speed management": ["variable speed limit", "VSL", "speed harmonization",
                         "dynamic speed", "speed advisory"],

    # Transit
    "CAD/AVL":  ["computer aided dispatch", "automatic vehicle location",
                 "AVL", "CAD", "vehicle tracking", "bus tracking", "GPS tracking"],
    "APC":      ["automatic passenger counter", "passenger counting",
                 "ridership counting"],
    "GTFS":     ["general transit feed specification", "transit feed",
                 "transit data feed", "transit schedule data"],
    "fare":     ["fare collection", "fare payment", "smartcard", "smart card",
                 "contactless payment", "fare card", "electronic fare", "AFC",
                 "automated fare collection"],
    "paratransit": ["demand response", "dial-a-ride", "microtransit",
                    "on-demand transit", "mobility on demand", "MaaS",
                    "mobility as a service"],

    # Traveler information
    "511":      ["traveler information system", "travel info", "road conditions",
                 "traffic conditions", "travel advisory"],
    "trip planning": ["journey planner", "route planner", "multimodal planner",
                      "trip planner", "itinerary"],
    "ATIS":     ["advanced traveler information system", "traveler information"],

    # Incident / emergency
    "incident management": ["incident response", "incident detection",
                            "traffic incident management", "TIM"],
    "HAZMAT":   ["hazardous material", "hazardous materials", "dangerous goods",
                 "HAZMAT routing"],

    # Maintenance
    "RWIS":     ["road weather information system", "ESS",
                 "environmental sensor station", "weather station",
                 "road weather station", "pavement sensor"],
    "work zone": ["construction zone", "road work", "lane closure",
                  "work zone management", "WZM", "smart work zone"],
    "AVL maintenance": ["maintenance vehicle tracking", "fleet tracking",
                        "snowplow tracking", "plow tracking", "fleet AVL"],

    # Commercial vehicles
    "CVO":      ["commercial vehicle operations", "freight operations",
                 "trucking", "commercial motor vehicle"],
    "CVISN":    ["commercial vehicle information systems and networks",
                 "electronic screening", "PrePass", "DriveWyze",
                 "weigh station bypass"],
    "oversize overweight": ["OS/OW", "oversize permit", "overweight permit",
                            "special hauling permit", "superload"],

    # Connected / automated vehicles
    "V2I":      ["vehicle to infrastructure", "V2X", "C-V2X", "DSRC",
                 "connected vehicle", "CV", "roadside unit", "RSU", "OBU",
                 "onboard unit"],
    "V2V":      ["vehicle to vehicle", "V2X"],
    "SPaT":     ["signal phase and timing", "MAP message", "intersection geometry"],
    "automated vehicle": ["autonomous vehicle", "AV", "self-driving",
                          "automated driving", "ADS", "ADAS",
                          "advanced driver assistance"],

    # Standards
    "NTCIP":    ["national transportation communications for ITS protocol",
                 "NTCIP 1203", "NTCIP 1201", "NTCIP 1202", "NTCIP 1204",
                 "SNMP", "STMP", "center to field"],
    "TMDD":     ["traffic management data dictionary", "center to center",
                 "C2C", "NTCIP 2306"],
    "SAE J2735": ["BSM", "basic safety message", "connected vehicle message set"],

    # Data / performance
    "NPMRDS":   ["national performance management research data set",
                 "probe data", "travel time data", "speed data"],
    "data archive": ["data warehouse", "data archiving", "ITS data",
                     "performance data", "archived data"],

    # Weather
    "road weather": ["winter maintenance", "anti-icing", "de-icing",
                     "snow removal", "weather responsive management",
                     "MDSS", "maintenance decision support"],

    # Tolling
    "ETC":      ["electronic toll collection", "E-ZPass", "toll tag",
                 "toll transponder", "toll gantry", "open road tolling",
                 "all electronic tolling", "cashless tolling"],

    # Surveillance
    "CCTV":     ["closed circuit television", "traffic camera", "video surveillance",
                 "traffic monitoring camera", "PTZ camera", "video management"],
    "detector":  ["loop detector", "vehicle detector", "traffic detector",
                  "radar detector", "microwave detector", "video detection",
                  "RTMS", "Wavetronix", "inductive loop"],

    # Parking
    "parking management": ["smart parking", "parking guidance", "parking availability",
                           "parking information", "PGI", "parking sensor"],

    # Sustainability
    "congestion pricing": ["road pricing", "cordon pricing", "value pricing",
                           "dynamic pricing", "tolling for congestion",
                           "congestion charge", "mobility pricing"],
}


def expand_desc_with_synonyms(desc):
    """Append relevant synonyms to a description string for better keyword matching.

    Scans the description for any terms that appear as keys in ITS_SYNONYMS
    and appends the alternate terms in parentheses.  This makes wiki pages
    match user queries regardless of which terminology they use.
    """
    desc_lower = desc.lower()
    additions = []

    for canonical, alts in ITS_SYNONYMS.items():
        # Check if the canonical term appears in the description
        if canonical.lower() in desc_lower:
            # Pick synonyms that aren't already in the description
            new_alts = [a for a in alts if a.lower() not in desc_lower]
            if new_alts:
                additions.append(f"also: {', '.join(new_alts[:5])}")

    if additions:
        return desc + " (" + '; '.join(additions) + ")"
    return desc


# ---------------------------------------------------------------------------
# Content classification
# ---------------------------------------------------------------------------

def classify_url(url):
    """Return content type string from a URL."""
    if '/bundle.htm?' in url: return 'bundle'
    if '/element.htm?' in url or url.endswith('/element.htm'): return 'element'
    if '/stakeholder.htm?' in url or url.endswith('/stakeholder.htm'): return 'stakeholder'
    if '/funreq.htm?' in url: return 'funreq'
    if '/plandetail.htm?' in url: return 'plan'
    if '/flow.htm?' in url: return 'flow'
    if '/interface.htm?' in url: return 'interface'
    if '/projdetail.htm?' in url or url.endswith('/projects.htm'): return 'project'
    if '/solution.htm?' in url: return 'solution'
    if '/spinstance.htm?' in url: return 'service_package'
    return 'other'


def extract_sp_code(title):
    """Extract the base service package code (e.g. 'TM01') from a title."""
    m = re.search(r'(?:^|_)([A-Z]{2,4}\d{2})', title)
    if m:
        code = m.group(1)
        if not code.startswith('SH'):
            return code
    return None


def extract_sp_category(code):
    """Return the 2-3 letter category prefix from a code like 'TM01'."""
    m = re.match(r'^([A-Z]{2,4})', code)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Data analysis
# ---------------------------------------------------------------------------

def analyze_architecture(data):
    """Analyze processed_content.json and return structured summaries."""
    analysis = {
        'elements': [],
        'stakeholders': [],
        'service_packages': defaultdict(list),   # code -> [instances]
        'funreqs': [],
        'interfaces': [],
        'flows': [],
        'plans': [],
        'bundles': [],
        'solutions': [],
        'projects': [],
        'sp_codes': set(),
        'sp_categories': defaultdict(set),       # category -> {codes}
    }

    for doc in data:
        ctype = classify_url(doc['url'])
        entry = {
            'title': doc['title'],
            'url': doc['url'],
            'content_preview': doc['content'][:500],
            'content_length': len(doc['content']),
        }

        if ctype == 'element':
            # Parse key fields from element content
            content = doc['content']
            desc_match = re.search(r'Description:\s*(.+?)(?:Status:|Element Functions:|$)', content)
            status_match = re.search(r'Status:\s*(\w+)', content)
            stakeholder_match = re.search(r'Stakeholder:\s*(.+?)(?:Element Functions:|$)', content)

            entry['description'] = desc_match.group(1).strip() if desc_match else ''
            entry['status'] = status_match.group(1).strip() if status_match else ''
            entry['stakeholder'] = stakeholder_match.group(1).strip() if stakeholder_match else ''

            # Extract service packages this element participates in
            sp_codes_in_content = re.findall(r'([A-Z]{2,4}\d{2})', content)
            entry['service_packages'] = list(set(c for c in sp_codes_in_content if not c.startswith('SH')))

            analysis['elements'].append(entry)

        elif ctype == 'stakeholder':
            # Skip template/placeholder pages that have no ?id= parameter
            if '?id=' not in entry.get('url', ''):
                continue
            name_match = re.search(r'Name:\s*(.+?)(?:Description:|Elements|$)', doc['content'])
            entry['name'] = name_match.group(1).strip() if name_match else doc['title']
            analysis['stakeholders'].append(entry)

        elif ctype == 'service_package':
            code = extract_sp_code(doc['title'])
            if code:
                entry['sp_code'] = code
                cat = extract_sp_category(code)
                analysis['sp_codes'].add(code)
                analysis['sp_categories'][cat].add(code)
                analysis['service_packages'][code].append(entry)

        elif ctype == 'funreq':
            analysis['funreqs'].append(entry)

        elif ctype == 'interface':
            analysis['interfaces'].append(entry)

        elif ctype == 'flow':
            analysis['flows'].append(entry)

        elif ctype == 'plan':
            analysis['plans'].append(entry)

        elif ctype == 'bundle':
            analysis['bundles'].append(entry)

        elif ctype == 'solution':
            analysis['solutions'].append(entry)

        elif ctype == 'project':
            analysis['projects'].append(entry)

    return analysis


# ---------------------------------------------------------------------------
# Source corpus loader
# ---------------------------------------------------------------------------

def load_documents(input_file):
    """Load the source corpus as a list of {url, title, content} dicts.

    Supports the CSV corpus (one row per page, full page text in large content
    cells) and the legacy JSON array. The analyzer and traceability builder only
    need url/title/content.
    """
    if input_file.lower().endswith('.csv'):
        # Content cells hold whole pages; the default 128 KB field limit is too
        # small. 10**9 stays inside a 32-bit signed long (safe on Windows).
        csv.field_size_limit(10 ** 9)
        docs = []
        with open(input_file, 'r', encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                docs.append({
                    'url': (row.get('url') or '').strip(),
                    'title': (row.get('title') or '').strip(),
                    'content': row.get('content') or '',
                })
        return docs
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Traceability enrichment (interfaces + standards from spinstance pages)
# ---------------------------------------------------------------------------
# The summary wiki only *links* to interfaces and standards. To inline real
# detail we mine the "List of Interfaces" tables embedded in every service
# package instance (spinstance) page. Each table row is
#     <source element> <information flow> <destination element> <standard>
# run together with no delimiters, so we segment it greedily against the known
# vocabularies of element names (from element.htm rows) and information-flow
# names (from flow.htm rows). Because a spinstance carries a service package
# code (e.g. TM01) we attribute every parsed interface to the correct service
# area — far more precise than the keyword scan used for functional requirements.

# Standards bodies (NTCIP/IEEE/SAE/etc.) cited inside a solution page. Used to
# build a one-line "purpose" for each standard.
_STD_ID_RE = re.compile(
    r'\b(?:NTCIP|IEEE|SAE|ISO|IETF|RFC|TMDD|ITE|APTA|OMG|ASTM|AASHTO|ANSI|EIA|TIA|NEMA|ETSI|NMEA)'
    r'\s*[A-Z]?\d[\w.\-]*'
)

# Descriptive opening clause used when a solution names no numbered standard
# (e.g. proprietary or "(None)" communication profiles).
_STD_DESC_RE = re.compile(
    r'(This std[^.]*\.|This specification[^.]*\.|A bundle of standards[^.]*\.|'
    r'A proprietary[^.]*\.|Defines[^.]*\.|Communication profile not defined[^.]*\.|'
    r'No Standard Needed[^.]*\.)'
)


def _standard_purpose(content, name):
    """Return a one-line purpose for a solution/standard page.

    Prefers the concrete standards it cites (e.g. "NTCIP 1201, NTCIP 1203").
    When none are named (proprietary / "(None)" comm profiles) falls back to the
    first descriptive sentence, then to a cleaned snippet.
    """
    body = content[len(name):] if content.startswith(name) else content
    ids = []
    for m in _STD_ID_RE.findall(body):
        m = m.strip()
        if m not in ids:
            ids.append(m)
    if ids:
        return 'Specifies ' + ', '.join(ids[:8])
    clean = re.sub(r'\b(?:Data Standards|Comm Standards)\b', ' ', body)
    clean = re.sub(r'\s+', ' ', clean).strip()
    m = _STD_DESC_RE.search(clean)
    if m:
        return m.group(1).strip()[:180]
    return clean[:140].strip() or name


def _match_prefix(text, candidates_sorted):
    """Return the longest candidate that is a whole-token prefix of `text`.

    `candidates_sorted` must be sorted longest-first so that, e.g.,
    "Metropistas TMC Information Services" wins over "Metropistas TMC".
    """
    for c in candidates_sorted:
        if text.startswith(c) and (len(text) == len(c) or text[len(c)] == ' '):
            return c
    return None


def _parse_interface_table(segment, elem_names_sorted, flow_names_sorted):
    """Segment a run-on '<src> <flow> <dst> <std>' table into 4-tuples.

    Greedy: match the longest known element name (source), the longest known
    flow name, the longest known element name (destination), then take the
    standard as everything up to where the next element name begins. The
    standard is *not* validated here — callers apply resolve-or-drop.
    """
    triplets = []
    text = segment.strip()
    guard = 0
    while text and guard < 1000:
        guard += 1
        src = _match_prefix(text, elem_names_sorted)
        if not src:
            sp = text.find(' ')
            if sp < 0:
                break
            text = text[sp + 1:]
            continue
        rest = text[len(src):].lstrip()
        flow = _match_prefix(rest, flow_names_sorted)
        if not flow:
            sp = rest.find(' ')
            if sp < 0:
                break
            text = rest[sp + 1:]
            continue
        rest = rest[len(flow):].lstrip()
        dst = _match_prefix(rest, elem_names_sorted)
        if not dst:
            text = rest
            continue
        rest = rest[len(dst):].lstrip()
        # Standard runs until the next element name begins (start of next row).
        cut = len(rest)
        for nm in elem_names_sorted:
            k = rest.find(nm)
            if 0 <= k < cut:
                cut = k
        std = rest[:cut].strip()
        triplets.append((src, flow, dst, std))
        text = rest[cut:].lstrip()
    return triplets


def build_traceability(data):
    """Mine interfaces + standards from spinstance pages, keyed by service area.

    Returns a dict merged into `analysis`:
      cat_interfaces[cat] = {(src, flow, dst): record}   # deduped per category
      cat_standards[cat]  = {std_name: {url, purpose}}
      csv_urls            = set of every source URL (for link validation)
    Standards are resolve-or-drop: a standard is only attached if its name
    matches a real solution page, so every emitted standard URL is real.
    """
    # element name <-> id (interface URLs are keyed by element-id pairs)
    elem_name_to_id = {}
    for d in data:
        m = re.search(r'/element\.htm\?id=(\d+)', d['url'])
        if m:
            elem_name_to_id[d['title'].strip()] = m.group(1)
    elem_names_sorted = sorted((n for n in elem_name_to_id if n), key=len, reverse=True)

    # (element-id, element-id) -> interface URL, both orderings
    pair_to_iface = {}
    for d in data:
        m = re.search(r'/interface\.htm\?id=(\d+)-(\d+)', d['url'])
        if m:
            a, b = m.group(1), m.group(2)
            pair_to_iface[(a, b)] = d['url']
            pair_to_iface[(b, a)] = d['url']

    # standard name -> solution page. The name is the text before "Data
    # Standards"/"Comm Standards" in the solution body.
    std_to_sol = {}
    for d in data:
        if '/solution.htm?id=' in d['url']:
            content = d['content'].strip()
            name = re.split(r'\s+(?:Data Standards|Comm Standards)\b', content, maxsplit=1)[0].strip()
            if name and name.lower() != '(none)':
                std_to_sol.setdefault(name, {'url': d['url'], 'purpose': _standard_purpose(content, name)})

    flow_names_sorted = sorted(
        {d['title'].strip() for d in data if '/flow.htm?id=' in d['url'] and d['title'].strip()},
        key=len, reverse=True,
    )

    cat_interfaces = defaultdict(dict)   # cat -> {(src,flow,dst): record}
    cat_standards = defaultdict(dict)    # cat -> {std_name: {url,purpose}}
    parsed = 0
    for d in data:
        if '/spinstance.htm?' not in d['url']:
            continue
        code = extract_sp_code(d['title'])
        if not code:
            continue
        cat = extract_sp_category(code)
        idx = d['content'].find('List of Interfaces')
        if idx < 0:
            continue
        seg = d['content'][idx + len('List of Interfaces'):]
        seg = re.sub(r'^\s*Source Element Information Flow Destination Element Standards?', '', seg)
        seg = re.sub(r'\s+end\s*$', '', seg)
        for (src, flow, dst, std) in _parse_interface_table(seg, elem_names_sorted, flow_names_sorted):
            parsed += 1
            sol = std_to_sol.get(std)            # resolve-or-drop
            iface_url = pair_to_iface.get((elem_name_to_id.get(src), elem_name_to_id.get(dst)), '')
            key = (src, flow, dst)
            rec = cat_interfaces[cat].get(key)
            if rec is None:
                cat_interfaces[cat][key] = {
                    'src': src, 'flow': flow, 'dst': dst,
                    'std': std if sol else '',
                    'std_url': sol['url'] if sol else '',
                    'iface_url': iface_url,
                }
            elif sol and not rec['std']:
                rec['std'] = std
                rec['std_url'] = sol['url']
            if sol:
                cat_standards[cat].setdefault(std, sol)

    return {
        'cat_interfaces': cat_interfaces,
        'cat_standards': cat_standards,
        'csv_urls': {d['url'] for d in data},
        'trace_stats': {'parsed_triplets': parsed},
    }


# ---------------------------------------------------------------------------
# Service package -> functional requirement linkage
# ---------------------------------------------------------------------------
# Every spinstance page carries a "Functions Linked to Requirements" table that
# assigns named functions (e.g. "TMC Traffic Management Decision Support") to
# each participating element. This is the AUTHORITATIVE service-package ->
# functional-requirement edge. The summary wiki previously surfaced functional
# requirements only through a keyword scan, with no link back to the packages
# that implement them — so a query like "decision support service packages"
# could not be answered from the wiki even though the source states it outright
# (the decision-support function is named on exactly the packages that deploy
# it). We mine that table here and emit it bidirectionally on each service area
# page: each package lists the functions it implements, and each functional
# requirement lists the in-area packages that implement it.

_FN_BOILERPLATE = 'Specific functions are defined below:'


def build_function_links(data):
    """Mine the 'Functions Linked to Requirements' table from spinstance pages.

    Returns, keyed for merge into `analysis`:
      sp_functions[code]       = sorted [function name]   # what a package implements
      fr_implemented_by[name]  = sorted [code]            # the reverse edge
      fn_name_to_url[name]     = funreq URL               # for linking

    Function names are segmented out of the run-on table greedily against the
    vocabulary of real functional-requirement page titles (same technique as
    the interface miner), so every emitted function resolves to a real funreq
    page — resolve-or-drop, no fabricated links.
    """
    # Vocabulary 1: functional-requirement names <- funreq page titles
    # ("Functional Requirements: <name>" -> "<name>").
    fn_name_to_url = {}
    for d in data:
        if '/funreq.htm?id=' in d['url']:
            title = d['title'].strip()
            name = title.split(':', 1)[1].strip() if ':' in title else title
            if name:
                fn_name_to_url.setdefault(name, d['url'])
    fn_names_sorted = sorted(fn_name_to_url, key=len, reverse=True)

    # Vocabulary 2: element names, skipped over while scanning the table.
    elem_names_sorted = sorted(
        {d['title'].strip() for d in data
         if '/element.htm?id=' in d['url'] and d['title'].strip()},
        key=len, reverse=True,
    )

    sp_functions = defaultdict(set)
    fr_implemented_by = defaultdict(set)

    for d in data:
        if '/spinstance.htm?' not in d['url']:
            continue
        code = extract_sp_code(d['title'])
        if not code:
            continue
        content = d['content']
        i = content.find('Functions Linked to Requirements')
        if i < 0:
            continue
        seg = content[i + len('Functions Linked to Requirements'):]
        # The table ends where the next major section of the page begins.
        for marker in ('Interfaces and Standards', 'List of Interfaces',
                       'Projects Associated', 'Interfaces'):
            k = seg.find(marker)
            if k >= 0:
                seg = seg[:k]
        # Greedily pull function names out of the run-on text; advance past
        # element names and the per-element boilerplate phrase in between.
        text = seg.strip()
        guard = 0
        while text and guard < 5000:
            guard += 1
            fn = _match_prefix(text, fn_names_sorted)
            if fn:
                sp_functions[code].add(fn)
                fr_implemented_by[fn].add(code)
                text = text[len(fn):].lstrip()
                continue
            if text.startswith(_FN_BOILERPLATE):
                text = text[len(_FN_BOILERPLATE):].lstrip()
                continue
            el = _match_prefix(text, elem_names_sorted)
            if el:
                text = text[len(el):].lstrip()
                continue
            sp = text.find(' ')
            if sp < 0:
                break
            text = text[sp + 1:]

    return {
        'sp_functions': {c: sorted(fns) for c, fns in sp_functions.items()},
        'fr_implemented_by': {n: sorted(cs) for n, cs in fr_implemented_by.items()},
        'fn_name_to_url': fn_name_to_url,
    }


# ---------------------------------------------------------------------------
# Wiki page generators
# ---------------------------------------------------------------------------

def generate_overview(analysis, arch_name, base_url):
    """Generate the top-level architecture overview page."""
    n = {
        'elements': len(analysis['elements']),
        'stakeholders': len(analysis['stakeholders']),
        'sp_codes': len(analysis['sp_codes']),
        'sp_instances': sum(len(v) for v in analysis['service_packages'].values()),
        'funreqs': len(analysis['funreqs']),
        'interfaces': len(analysis['interfaces']),
        'flows': len(analysis['flows']),
        'plans': len(analysis['plans']),
        'bundles': len(analysis['bundles']),
        'solutions': len(analysis['solutions']),
        'projects': len(analysis['projects']),
    }

    # Find status distribution for elements
    statuses = defaultdict(int)
    for el in analysis['elements']:
        statuses[el.get('status', 'Unknown')] += 1

    status_lines = ', '.join(f"{s}: {c}" for s, c in sorted(statuses.items(), key=lambda x: -x[1]))

    return f"""# {arch_name} — Overview

## Scope
This architecture contains **{n['elements']} elements**, **{n['stakeholders']} stakeholders**, and **{n['sp_codes']} unique service package types** ({n['sp_instances']} total instances including stakeholder-specific variants).

Additional content: {n['funreqs']} functional requirements, {n['interfaces']} interfaces, {n['flows']} data flows, {n['plans']} planning documents, {n['bundles']} standards bundles, {n['solutions']} solutions/standards, {n['projects']} projects.

## Element Status Distribution
{status_lines}

## Service Area Categories Present
{_format_category_summary(analysis)}

## Key Agencies / Stakeholders
{_format_top_stakeholders(analysis)}

## How to Use This Wiki
- **Conceptual questions** ("What does traffic management involve?"): Read the relevant service area page.
- **Specific lookups** ("Show me element el599"): Use keyword search against the raw content index.
- **Deployment questions** ("What do I need for a DMS deployment?"): Read the service area page for context, then search for specific functional requirements and standards.
- **RFP/RFI questions**: The service area pages list which functional requirements, interfaces, and standards apply. These map directly to RFP specification sections.

Base URL: {base_url}

{_deployment_guidance()}"""


def _format_category_summary(analysis):
    lines = []
    for cat_code in sorted(analysis['sp_categories'].keys()):
        codes = analysis['sp_categories'][cat_code]
        if cat_code in SP_CATEGORIES:
            cat_info = SP_CATEGORIES[cat_code]
            lines.append(f"- **{cat_info['name']}** ({cat_code}): {len(codes)} service package types — {cat_info['desc']}")
        else:
            lines.append(f"- **{cat_code}**: {len(codes)} service package types")
    return '\n'.join(lines)


def _format_top_stakeholders(analysis):
    # List stakeholders, grouped roughly by type
    stakeholders = analysis['stakeholders']
    if not stakeholders:
        return "(No stakeholders found)"

    lines = []
    for s in sorted(stakeholders, key=lambda x: x.get('name', x['title'])):
        name = s.get('name', s['title'])
        if name.startswith('Stakeholder '):
            continue  # Skip unnamed ones
        lines.append(f"- [{name}]({s['url']})")

    return '\n'.join(lines)


def generate_service_area_page(cat_code, analysis, base_url,
                               include_interfaces=True,
                               include_standards=True,
                               inline_standard_on_interface=True):
    """Generate a wiki page for one service area category.

    The detail tier is driven by flags so the same generator emits every role
    variant (see the VARIANTS config / build_wiki):
      include_interfaces            -> emit the Interfaces section (gated on the
                                       'interface' content type)
      include_standards             -> emit the Applicable Standards section
                                       (gated on the 'solution' content type)
      inline_standard_on_interface  -> keep the standard name on each interface
                                       line. An interface flow inherently names
                                       its standard, so this stays on even for
                                       the planning tier; only the dedicated
                                       Applicable Standards section (solution.htm
                                       links) is withheld there.
    """
    if cat_code not in SP_CATEGORIES:
        return None

    cat = SP_CATEGORIES[cat_code]
    codes_in_arch = sorted(analysis['sp_categories'].get(cat_code, set()))

    if not codes_in_arch:
        return None

    # Find elements that participate in this category's service packages
    relevant_elements = []
    for el in analysis['elements']:
        el_sp_codes = el.get('service_packages', [])
        if any(extract_sp_category(c) == cat_code for c in el_sp_codes):
            relevant_elements.append(el)

    # Find functional requirements mentioning this category's keywords
    cat_keywords = _get_category_keywords(cat_code)
    relevant_funreqs = []
    for fr in analysis['funreqs']:
        preview = fr['content_preview'].lower()
        if any(kw in preview for kw in cat_keywords):
            relevant_funreqs.append(fr)

    # Build the page
    enriched_cat_desc = expand_desc_with_synonyms(cat['desc'])
    page = f"""# {cat['name']} ({cat_code})

{enriched_cat_desc}

## Service Packages in This Architecture

"""
    # Group by subcategory
    for sub_key, sub_info in cat.get('subcategories', {}).items():
        matched_codes = [c for c in codes_in_arch if c in sub_info['codes']]
        if not matched_codes:
            continue

        page += f"### {sub_info['name']}\n"
        enriched_desc = expand_desc_with_synonyms(sub_info['desc'])
        page += f"*{enriched_desc}*\n\n"

        for code in matched_codes:
            instances = analysis['service_packages'].get(code, [])
            # Deduplicate by grouping stakeholder-specific instances
            base_instances = [i for i in instances if 'mp' not in i['title'].lower()[:4]]
            mp_count = len(instances) - len(base_instances)

            if base_instances:
                for inst in base_instances:
                    # Drop the redundant "Service Package " label from the link
                    # TEXT only — the id (e.g. mpSH1_TM04-02(Co-Mun)) already
                    # identifies it, and the URL is unchanged so the runtime can
                    # still cite it verbatim. ~7K tokens saved across the wiki.
                    disp = inst['title']
                    if disp.startswith('Service Package '):
                        disp = disp[len('Service Package '):]
                    page += f"- [{disp}]({inst['url']})"
                    if mp_count > 0:
                        page += f" (+{mp_count} stakeholder-specific instances)"
                    page += "\n"
            else:
                page += f"- {code}: {len(instances)} stakeholder-specific instances\n"

            # Authoritative functions this package's elements perform, linked to
            # their functional requirement pages. This is the SP -> FR edge mined
            # from each spinstance's "Functions Linked to Requirements" table; it
            # lets a capability query (e.g. "decision support") match the package
            # that deploys it even when the package title/description does not say so.
            functions = analysis.get('sp_functions', {}).get(code, [])
            if functions:
                fn_links = []
                for fn in functions:
                    fn_url = analysis.get('fn_name_to_url', {}).get(fn)
                    fn_links.append(f"[{fn}]({fn_url})" if fn_url else fn)
                page += f"  - *Implements:* {', '.join(fn_links)}\n"

        page += "\n"

    # Elements section
    if relevant_elements:
        page += f"## Key Elements ({len(relevant_elements)} total)\n\n"
        page += "| Element | Status | Stakeholder |\n"
        page += "|---------|--------|-------------|\n"
        for el in sorted(relevant_elements, key=lambda x: x['title']):
            page += f"| [{el['title']}]({el['url']}) | {el.get('status', '?')} | {el.get('stakeholder', '')[:50]} |\n"
        page += "\n"

    # Interfaces section (real source -> flow -> destination triplets)
    if include_interfaces:
        page += _format_interfaces_section(cat_code, analysis, inline_standard_on_interface)

    # Applicable standards section (only for tiers that may see standards)
    if include_standards:
        page += _format_standards_section(cat_code, analysis)

    # Functional requirements section
    if relevant_funreqs:
        page += f"## Related Functional Requirements ({len(relevant_funreqs)} found)\n\n"
        impl = analysis.get('fr_implemented_by', {})
        for fr in relevant_funreqs:
            title = fr['title']
            name = title.split(':', 1)[1].strip() if ':' in title else title
            # The reverse SP -> FR edge: name the packages in THIS service area
            # that deploy this requirement, so the requirement is reachable from
            # a package query and vice versa.
            codes_here = [c for c in impl.get(name, [])
                          if extract_sp_category(c) == cat_code]
            page += f"- [{title}]({fr['url']})"
            if codes_here:
                page += f" — implemented by {', '.join(codes_here)}"
            page += "\n"
        page += "\n"

    # Deployment guidance is emitted ONCE per variant (in the overview), not on
    # every service-area page — the steps are identical across areas, so the 12
    # per-variant copies were ~8K tokens of pure repetition in the always-loaded
    # context. See _deployment_guidance() / generate_overview().

    return page


def _format_interfaces_section(cat_code, analysis, inline_standard):
    """Render the deduped interface triplets for a service area."""
    records = analysis.get('cat_interfaces', {}).get(cat_code, {})
    if not records:
        return ""
    items = sorted(records.values(), key=lambda r: (r['src'], r['flow'], r['dst']))
    lines = [
        f"## Interfaces ({len(items)} data flows)\n",
        "Real information flows between elements in this service area, in the form "
        "*Source Element → information flow → Destination Element*. Each links to "
        "its interface specification.\n",
    ]
    for r in items:
        line = f"- {r['src']} → {r['flow']} → {r['dst']}"
        if inline_standard and r['std']:
            line += f" ({r['std']})"
        if r['iface_url']:
            line += f" — [interface]({r['iface_url']})"
        lines.append(line)
    return "\n".join(lines) + "\n\n"


def _format_standards_section(cat_code, analysis):
    """Render the distinct standards referenced by a service area's interfaces."""
    stds = analysis.get('cat_standards', {}).get(cat_code, {})
    if not stds:
        return ""
    lines = [
        f"## Applicable Standards ({len(stds)})\n",
        "Communication and data standards referenced by the interfaces above.\n",
    ]
    for name in sorted(stds):
        info = stds[name]
        lines.append(f"- **{name}** — {info['purpose']} ([standard]({info['url']}))")
    return "\n".join(lines) + "\n\n"


def _get_category_keywords(cat_code):
    """Return lowercase keywords used to match functional requirements to a category."""
    keyword_map = {
        "TM": ["traffic", "signal", "freeway", "ramp meter", "dms", "dynamic message", "highway advisory", "hov", "hot", "speed management", "lane control", "incident detect", "traffic surveil"],
        "PT": ["transit", "bus", "rail", "passenger", "fare", "schedule", "avl", "paratransit", "demand response"],
        "TI": ["traveler info", "511", "trip plan", "multimodal", "personalized"],
        "PS": ["incident", "emergency", "hazmat", "railroad crossing", "cctv", "security", "wrong-way", "bridge monitor"],
        "MC": ["maintenance", "construction", "work zone", "road weather", "rwis", "infrastructure monitor", "winter"],
        "CVO": ["commercial vehicle", "freight", "credential", "screening", "oversize", "overweight", "hazmat"],
        "DM": ["data archiv", "performance measure", "data warehouse", "data collect"],
        "PM": ["planning", "scenario", "emission", "regional plan"],
        "WX": ["weather", "rwis", "wind", "visibility", "road surface"],
        "SU": ["device manage", "map manage", "communication", "cybersecur", "location"],
        "VS": ["v2v", "v2i", "automated", "platooning", "collision", "connected vehicle safety"],
        "ST": ["congestion pric", "emission", "alternative fuel", "transit incentive", "sustainable"],
    }
    return keyword_map.get(cat_code, [])


def _deployment_guidance():
    """Return the generic deployment-guidance section.

    Emitted ONCE per variant (in the overview) rather than repeated on every
    service-area page. The steps are identical across areas, so the old
    per-page emission cost ~8K tokens/variant of duplicated text in the
    always-loaded context for no added information.
    """
    return """## Deployment Guidance (applies to every service area)

When planning a deployment in any service area:

1. **Identify the service packages** that apply to your use case from that service area's page.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
"""


def generate_stakeholders_page(analysis):
    """Generate the stakeholders summary page."""
    stakeholders = analysis['stakeholders']

    # Group by apparent type based on name patterns
    groups = defaultdict(list)
    for s in stakeholders:
        name = s.get('name', s['title'])
        if any(k in name.upper() for k in ['DOT', 'DEPARTMENT OF TRANS']):
            groups['State DOTs'].append(s)
        elif any(k in name.upper() for k in ['MPO', 'PLANNING', 'NJTPA', 'NYMTC', 'DVRPC']):
            groups['MPOs & Planning Agencies'].append(s)
        elif any(k in name.upper() for k in ['TRANSIT', 'MTA', 'NJT', 'BUS', 'RAIL']):
            groups['Transit Agencies'].append(s)
        elif any(k in name.upper() for k in ['TOLL', 'TURNPIKE', 'THRUWAY', 'PANYNJ', 'AUTHORITY']):
            groups['Toll & Bridge Authorities'].append(s)
        elif any(k in name.upper() for k in ['COUNTY', 'MUNICIPAL', 'CITY', 'LOCAL']):
            groups['Local / Municipal'].append(s)
        elif any(k in name.upper() for k in ['PRIVATE', 'COMMERCIAL', '3RD PARTY']):
            groups['Private Sector'].append(s)
        elif any(k in name.upper() for k in ['FEDERAL', 'FHWA', 'FTA', 'USDOT', 'FMCSA']):
            groups['Federal Agencies'].append(s)
        else:
            groups['Other'].append(s)

    page = f"# Stakeholders ({len(stakeholders)} total)\n\n"
    for group_name in ['State DOTs', 'MPOs & Planning Agencies', 'Transit Agencies',
                       'Toll & Bridge Authorities', 'Local / Municipal', 'Federal Agencies',
                       'Private Sector', 'Other']:
        members = groups.get(group_name, [])
        if not members:
            continue
        page += f"## {group_name} ({len(members)})\n"
        for s in sorted(members, key=lambda x: x.get('name', x['title'])):
            name = s.get('name', s['title'])
            page += f"- [{name}]({s['url']})\n"
        page += "\n"

    return page


def generate_standards_page(analysis):
    """Generate a standards overview page from bundles and solutions."""
    page = "# Standards & Specifications\n\n"

    if analysis['bundles']:
        page += f"## Standards Bundles ({len(analysis['bundles'])})\n\n"
        page += "Bundles are collections of related standards (typically IETF RFCs, NTCIP, SAE, IEEE) grouped by function.\n\n"
        for b in sorted(analysis['bundles'], key=lambda x: x['title']):
            page += f"- [{b['title']}]({b['url']})\n"
        page += "\n"

    if analysis['solutions']:
        page += f"## Individual Standards / Solutions ({len(analysis['solutions'])})\n\n"
        # Group by prefix pattern
        ntcip = [s for s in analysis['solutions'] if 'NTCIP' in s['title'].upper() or 'NTCIP' in s['content_preview'].upper()]
        other = [s for s in analysis['solutions'] if s not in ntcip]

        if ntcip:
            page += f"### NTCIP Standards ({len(ntcip)})\n"
            for s in sorted(ntcip, key=lambda x: x['title']):
                page += f"- [{s['title']}]({s['url']})\n"
            page += "\n"

        if other:
            page += f"### Other Standards ({len(other)})\n"
            for s in sorted(other, key=lambda x: x['title']):
                page += f"- [{s['title']}]({s['url']})\n"
            page += "\n"

    return page


def generate_index(analysis, arch_name, output_dir, include_standards_page=True):
    """Generate the master index.md that the LLM reads first.

    `include_standards_page` is threaded from the variant flags: when False
    (planning/strategic tiers) the standards.md link is omitted so the index
    never points at a page that variant does not emit, and never leaks standards
    terminology to a role that should not see it.
    """
    # List all generated pages
    service_area_files = []
    for cat_code in sorted(SP_CATEGORIES.keys()):
        if cat_code in analysis['sp_categories']:
            cat = SP_CATEGORIES[cat_code]
            filename = f"service-areas/{cat_code.lower()}-{cat['name'].lower().replace(' ', '-').replace('/', '-')}.md"
            service_area_files.append((cat_code, cat['name'], filename, cat['desc']))

    page = f"""# {arch_name} — Wiki Index

> This index is read by the LLM before answering any query.
> Each linked page contains pre-synthesized architectural knowledge.
> For specific element/interface/requirement lookups by ID, use keyword search.

## Architecture Overview
- [overview.md](overview.md) — Architecture scope, element counts, key agencies

## Service Areas
"""

    for cat_code, cat_name, filename, desc in service_area_files:
        codes = sorted(analysis['sp_categories'][cat_code])
        page += f"- [{cat_name} ({cat_code})]({filename}) — {', '.join(codes)}\n"

    page += f"""
## Cross-Cutting
- [stakeholders.md](stakeholders.md) — {len(analysis['stakeholders'])} stakeholders by type: DOTs, MPOs, transit, toll authorities, local, private
"""
    if include_standards_page:
        page += "- [standards.md](standards.md) — Standards bundles and individual specifications (NTCIP, TMDD, SAE, IEEE, etc.)\n"

    page += """
## How the LLM Should Use This Wiki
1. Read this index to find the relevant page(s)
2. Open 1-2 pages for conceptual/deployment questions
3. For precise lookups (element by ID, specific interface), fall back to keyword search
4. For RFP/RFI questions, the service area page provides the traceability chain:
   Service Package → Elements → Functional Requirements → Interfaces → Standards
"""

    return page


# ---------------------------------------------------------------------------
# Role-tiered variant configuration
# ---------------------------------------------------------------------------
# Each of main.py's five roles is collapsed into one of three detail tiers,
# derived from ROLE_CONTENT_CONFIG (HANDOFF.md §3.1). The deciding inputs are
# whether the role's content_types include 'interface' and/or 'solution':
#
#   Role          interface?  solution?   Variant
#   POLICY_MAKER   no          no          strategic
#   PLANNER        yes         no          planning
#   CONSULTANT     yes         yes         technical
#   MPO_STAFF      yes         yes         technical
#   ENGINEER       yes         yes         technical
#   UNKNOWN        yes         yes         technical  (default)
#
# main.py's variant_for_role() applies the SAME rule at runtime (a pure dict
# lookup, no I/O) so the two can't drift.
#
# inline_standard_on_interface stays True for the planning tier on purpose: an
# interface data flow inherently names its standard in the Standard column, so
# "a planner sees no standards" means no dedicated Applicable Standards section
# and no standards.md page — NOT scrubbing the standard name off each interface
# line. Flip planning's inline_standard_on_interface to False for a stricter
# reading; the generator already supports it.
VARIANTS = {
    "technical": dict(include_interfaces=True,  include_standards=True,
                      inline_standard_on_interface=True,  include_standards_page=True),
    "planning":  dict(include_interfaces=True,  include_standards=False,
                      inline_standard_on_interface=True,  include_standards_page=False),
    "strategic": dict(include_interfaces=False, include_standards=False,
                      inline_standard_on_interface=False, include_standards_page=False),
}


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_wiki(input_file, output_dir, arch_name, base_url):
    """Build the role-tiered wiki from the source corpus (CSV or legacy JSON).

    The corpus is loaded, analyzed, and mined for interface/standard
    traceability ONCE; then each detail tier in VARIANTS is rendered into its
    own subdirectory (output_dir/<variant>/) by re-running the same page
    generators with different flags. main.py picks a variant per request with a
    pure dict lookup, so this build-time tiering adds zero runtime latency.
    """
    print(f"Reading {input_file}...")
    data = load_documents(input_file)
    print(f"  {len(data)} documents loaded")

    print("Analyzing architecture...")
    analysis = analyze_architecture(data)
    print(f"  Elements: {len(analysis['elements'])}")
    print(f"  Stakeholders: {len(analysis['stakeholders'])}")
    print(f"  Service package types: {len(analysis['sp_codes'])}")
    print(f"  Functional requirements: {len(analysis['funreqs'])}")
    print(f"  Interfaces: {len(analysis['interfaces'])}")

    print("Mining interfaces + standards from spinstance pages...")
    analysis.update(build_traceability(data))
    print(f"  Parsed interface flows: {analysis['trace_stats']['parsed_triplets']}")

    print("Mining service-package -> functional-requirement links...")
    analysis.update(build_function_links(data))
    print(f"  Service packages with linked functions: {len(analysis['sp_functions'])}")

    # M1 wrote pages at the top level of output_dir; those are stale now that
    # every variant lives in output_dir/<variant>/. Clear the whole tree so no
    # stale page can linger and get merged into a runtime context.
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    # Render each variant. Keys are namespaced by variant so the URL validator
    # can check every emitted link across all variants in one pass.
    all_written = {}
    for variant, flags in VARIANTS.items():
        written = _build_variant(os.path.join(output_dir, variant), variant, flags,
                                 analysis, arch_name, base_url)
        for relpath, content in written.items():
            all_written[f"{variant}/{relpath}"] = content

    # --- Validate every emitted http(s) link resolves to a real source URL ---
    violations = _validate_emitted_urls(all_written, analysis['csv_urls'])
    if violations:
        print(f"\nWARNING: {len(violations)} emitted URL(s) are NOT in the source corpus:")
        for relpath, url in violations[:20]:
            print(f"  [{relpath}] {url}")
    else:
        print("\nURL check: all emitted source links resolve to real corpus rows. OK")

    print(f"\nDone. {len(all_written)} wiki pages written across "
          f"{len(VARIANTS)} variants ({', '.join(VARIANTS)}) to {output_dir}/")


def _build_variant(variant_dir, variant, flags, analysis, arch_name, base_url):
    """Render one detail-tier variant into variant_dir.

    Returns {relpath: content} for every page written, and prints the
    per-page + total token counts for this variant.
    """
    os.makedirs(os.path.join(variant_dir, 'service-areas'), exist_ok=True)

    written = {}

    def emit(relpath, content):
        path = os.path.join(variant_dir, relpath)
        _write(path, content)
        written[relpath.replace('\\', '/')] = content

    print(f"\n=== Building '{variant}' variant -> {variant_dir}/ ===")

    # Overview
    emit('overview.md', generate_overview(analysis, arch_name, base_url))

    # Service area pages (detail tier driven by the variant flags)
    for cat_code in sorted(SP_CATEGORIES.keys()):
        if cat_code not in analysis['sp_categories']:
            continue
        cat = SP_CATEGORIES[cat_code]
        filename = f"{cat_code.lower()}-{cat['name'].lower().replace(' ', '-').replace('/', '-')}.md"
        page = generate_service_area_page(
            cat_code, analysis, base_url,
            include_interfaces=flags['include_interfaces'],
            include_standards=flags['include_standards'],
            inline_standard_on_interface=flags['inline_standard_on_interface'],
        )
        if page:
            emit(os.path.join('service-areas', filename), page)

    # Stakeholders
    emit('stakeholders.md', generate_stakeholders_page(analysis))

    # Standards page — only for tiers that may see standards (omitted for
    # planning/strategic so no solution.htm links leak to those roles).
    if flags['include_standards_page']:
        emit('standards.md', generate_standards_page(analysis))

    # Index (last, since it references all pages)
    emit('index.md', generate_index(analysis, arch_name, variant_dir,
                                    include_standards_page=flags['include_standards_page']))

    # --- Report per-variant token counts (approx = chars / 4) ---
    print(f"Token counts ({variant}):")
    total_chars = 0
    for relpath in sorted(written):
        chars = len(written[relpath])
        total_chars += chars
        print(f"  {relpath:55} {chars // 4:>7,} tok")
    print(f"  {'TOTAL':55} {total_chars // 4:>7,} tok")

    return written


# Start of a markdown inline link to an http(s) target, e.g. [text](https://...
# The URL itself may contain balanced parentheses (spinstance IDs look like
# "...(PRHTA)"), so the closing ")" is found by paren-balancing, not a regex.
_MD_HTTP_LINK_START_RE = re.compile(r'\]\((https?://)')


def _extract_md_http_urls(content):
    """Yield every http(s) URL used as a markdown link target in `content`.

    Handles URLs containing balanced parentheses by tracking paren depth and
    treating the first unbalanced ")" as the closing link delimiter.
    """
    urls = []
    for m in _MD_HTTP_LINK_START_RE.finditer(content):
        i = m.start(1)
        depth = 0
        j = i
        while j < len(content):
            ch = content[j]
            if ch == '(':
                depth += 1
            elif ch == ')':
                if depth == 0:
                    break
                depth -= 1
            elif ch.isspace():
                break
            j += 1
        urls.append(content[i:j])
    return urls


def _validate_emitted_urls(written, csv_urls):
    """Return [(relpath, url)] for every emitted http(s) link not in the corpus.

    Relative wiki links (e.g. overview.md) are http-less and intentionally
    skipped — only links that claim to point at the source architecture are
    checked, per the "no fabricated links" guardrail.
    """
    violations = []
    for relpath, content in written.items():
        for url in _extract_md_http_urls(content):
            if url not in csv_urls:
                violations.append((relpath, url))
    return violations


def _write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build a wiki knowledge layer from an ITS architecture.')
    parser.add_argument('--input', default='../processed_content.csv', help='Path to the source corpus (.csv with url,title,content; legacy .json array also supported)')
    parser.add_argument('--output', default='wiki', help='Output directory for wiki pages')
    parser.add_argument('--architecture-name', default=DOT_NAME, help='Name of the architecture (default: DOT_NAME from config)')
    parser.add_argument('--base-url', default=ARCHITECTURE_BASE_URL, help='Base URL for the architecture website (default: ARCHITECTURE_BASE_URL from config)')
    args = parser.parse_args()

    build_wiki(args.input, args.output, args.architecture_name, args.base_url)
