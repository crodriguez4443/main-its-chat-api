# MAINEDOT — Wiki Index

> This index is read by the LLM before answering any query.
> Each linked page contains pre-synthesized architectural knowledge.
> For specific element/interface/requirement lookups by ID, use keyword search.

## Architecture Overview
- [overview.md](overview.md) — Architecture scope, element counts, key agencies

## Service Areas
- [Commercial Vehicle Operations (CVO)](service-areas/cvo-commercial-vehicle-operations.md) — CVO01, CVO03, CVO04, CVO05, CVO07, CVO08, CVO09, CVO10, CVO12, CVO21
- [Data Management (DM)](service-areas/dm-data-management.md) — DM01
- [Maintenance & Construction (MC)](service-areas/mc-maintenance-&-construction.md) — MC01, MC02, MC03, MC04, MC05, MC06, MC07, MC08, MC10
- [Performance Management (PM)](service-areas/pm-performance-management.md) — PM01, PM02, PM03
- [Public Safety (PS)](service-areas/ps-public-safety.md) — PS01, PS02, PS03, PS08, PS09, PS10, PS11, PS12, PS13, PS14
- [Public Transportation (PT)](service-areas/pt-public-transportation.md) — PT01, PT02, PT03, PT04, PT05, PT06, PT07, PT08, PT09, PT14, PT15, PT16
- [Sustainable Transport (ST)](service-areas/st-sustainable-transport.md) — ST04, ST05
- [Support (SU)](service-areas/su-support.md) — SU03
- [Traveler Information (TI)](service-areas/ti-traveler-information.md) — TI01, TI02, TI03, TI07
- [Traffic Management (TM)](service-areas/tm-traffic-management.md) — TM01, TM02, TM03, TM04, TM05, TM06, TM07, TM08, TM09, TM10, TM12, TM13, TM14, TM15, TM17, TM18, TM19, TM20, TM22, TM23, TM25
- [Vehicle Safety (VS)](service-areas/vs-vehicle-safety.md) — VS07, VS08, VS09, VS12
- [Weather (WX)](service-areas/wx-weather.md) — WX01, WX02, WX03

## Cross-Cutting
- [stakeholders.md](stakeholders.md) — 37 stakeholders by type: DOTs, MPOs, transit, toll authorities, local, private
- [standards.md](standards.md) — Standards bundles and individual specifications (NTCIP, TMDD, SAE, IEEE, etc.)

## How the LLM Should Use This Wiki
1. Read this index to find the relevant page(s)
2. Open 1-2 pages for conceptual/deployment questions
3. For precise lookups (element by ID, specific interface), fall back to keyword search
4. For RFP/RFI questions, the service area page provides the traceability chain:
   Service Package → Elements → Functional Requirements → Interfaces → Standards
