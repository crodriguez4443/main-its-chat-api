# MAINEDOT — Overview

## Scope
This architecture contains **111 elements**, **37 stakeholders**, and **80 unique service package types** (564 total instances including stakeholder-specific variants).

Additional content: 261 functional requirements, 339 interfaces, 298 data flows, 10 planning documents, 54 standards bundles, 245 solutions/standards, 98 projects.

## Element Status Distribution
Existing: 73, Planned: 37, : 1

## Service Area Categories Present
- **Commercial Vehicle Operations** (CVO): 10 service package types — Freight credentialing, electronic screening, HAZMAT tracking, oversize/overweight permits.
- **Data Management** (DM): 1 service package types — ITS data archiving, performance measurement, data warehousing.
- **Maintenance & Construction** (MC): 9 service package types — Road weather management, maintenance vehicle tracking, work zone management, infrastructure monitoring.
- **Performance Management** (PM): 3 service package types — Regional planning data, scenario modeling, emissions monitoring.
- **Public Safety** (PS): 10 service package types — Incident management, emergency response, HAZMAT, railroad crossings, security monitoring.
- **Public Transportation** (PT): 12 service package types — Transit vehicle tracking, scheduling, passenger info, fare collection, demand response.
- **Sustainable Transport** (ST): 2 service package types — Congestion pricing, transit incentives, emissions management.
- **Support** (SU): 1 service package types — Device management, mapping, location services, communications infrastructure.
- **Traveler Information** (TI): 4 service package types — 511 services, third-party apps, multimodal alerts, personalized traveler info.
- **Traffic Management** (TM): 21 service package types — Signal control, freeway management, traffic surveillance, incident detection, DMS, connected vehicle applications.
- **Vehicle Safety** (VS): 4 service package types — V2V safety, automated driving, platooning, collision avoidance.
- **Weather** (WX): 3 service package types — Road weather information systems, mobile weather observations.

## Key Agencies / Stakeholders
- [Acadia National Park/Island Explorer Is a member of stakeholder group: Local Transit Agencies](https://www.consystec.com/maine2026/web/stakeholder.htm?id=113)
- [Airport Authorities](https://www.consystec.com/maine2026/web/stakeholder.htm?id=60)
- [American Association of Motor Vehicle Administrators](https://www.consystec.com/maine2026/web/stakeholder.htm?id=52)
- [Amtrak](https://www.consystec.com/maine2026/web/stakeholder.htm?id=111)
- [Archive Data Users](https://www.consystec.com/maine2026/web/stakeholder.htm?id=20)
- [Canadian Border Services Agency](https://www.consystec.com/maine2026/web/stakeholder.htm?id=77)
- [County/Municipal Public Safety Agencies](https://www.consystec.com/maine2026/web/stakeholder.htm?id=92)
- [County/Municipal Traffic and Maintenance Agencies](https://www.consystec.com/maine2026/web/stakeholder.htm?id=1)
- [Electric Vehicle Charging Organizations](https://www.consystec.com/maine2026/web/stakeholder.htm?id=109)
- [Federal Motor Carrier Safety Administration](https://www.consystec.com/maine2026/web/stakeholder.htm?id=42)
- [Financial Institution](https://www.consystec.com/maine2026/web/stakeholder.htm?id=26)
- [IFTA](https://www.consystec.com/maine2026/web/stakeholder.htm?id=51)
- [Local Ferry Operators](https://www.consystec.com/maine2026/web/stakeholder.htm?id=114)
- [Local Transit Agencies Is a stakeholder group. Members include: - Acadia National Park/Island Explorer](https://www.consystec.com/maine2026/web/stakeholder.htm?id=21)
- [Maine Bureau of Motor Vehicles](https://www.consystec.com/maine2026/web/stakeholder.htm?id=75)
- [Maine Department of Transportation](https://www.consystec.com/maine2026/web/stakeholder.htm?id=3)
- [Maine Emergency Management Agency](https://www.consystec.com/maine2026/web/stakeholder.htm?id=64)
- [Maine State Police](https://www.consystec.com/maine2026/web/stakeholder.htm?id=68)
- [Maine State Police Commercial Vehicle Enforcement](https://www.consystec.com/maine2026/web/stakeholder.htm?id=36)
- [Maine Turnpike Authority](https://www.consystec.com/maine2026/web/stakeholder.htm?id=112)
- [Media](https://www.consystec.com/maine2026/web/stakeholder.htm?id=6)
- [Metropolitan Planning Organizations](https://www.consystec.com/maine2026/web/stakeholder.htm?id=74)
- [NH State Police](https://www.consystec.com/maine2026/web/stakeholder.htm?id=71)
- [NHDOT](https://www.consystec.com/maine2026/web/stakeholder.htm?id=39)
- [NOAA](https://www.consystec.com/maine2026/web/stakeholder.htm?id=28)
- [Other Counties](https://www.consystec.com/maine2026/web/stakeholder.htm?id=19)
- [Private Customs Brokers](https://www.consystec.com/maine2026/web/stakeholder.htm?id=70)
- [Private Maintenance Contractors](https://www.consystec.com/maine2026/web/stakeholder.htm?id=84)
- [Private Motor Carriers](https://www.consystec.com/maine2026/web/stakeholder.htm?id=41)
- [Private Tow/Wrecker Providers](https://www.consystec.com/maine2026/web/stakeholder.htm?id=29)
- [Private Traffic Data Provider](https://www.consystec.com/maine2026/web/stakeholder.htm?id=83)
- [Private Travelers](https://www.consystec.com/maine2026/web/stakeholder.htm?id=5)
- [Private Weather Information Provider](https://www.consystec.com/maine2026/web/stakeholder.htm?id=7)
- [Rail Operators](https://www.consystec.com/maine2026/web/stakeholder.htm?id=31)
- [Regional Event Coordinators](https://www.consystec.com/maine2026/web/stakeholder.htm?id=4)
- [US Department of Homeland Security](https://www.consystec.com/maine2026/web/stakeholder.htm?id=72)
- [US Government Agencies](https://www.consystec.com/maine2026/web/stakeholder.htm?id=108)

## How to Use This Wiki
- **Conceptual questions** ("What does traffic management involve?"): Read the relevant service area page.
- **Specific lookups** ("Show me element el599"): Use keyword search against the raw content index.
- **Deployment questions** ("What do I need for a DMS deployment?"): Read the service area page for context, then search for specific functional requirements and standards.
- **RFP/RFI questions**: The service area pages list which functional requirements, interfaces, and standards apply. These map directly to RFP specification sections.

Base URL: https://www.consystec.com/maine2026/web

## Deployment Guidance (applies to every service area)

When planning a deployment in any service area:

1. **Identify the service packages** that apply to your use case from that service area's page.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
