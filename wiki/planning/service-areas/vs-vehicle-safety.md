# Vehicle Safety (VS)

V2V safety, automated driving, platooning, collision avoidance. (also: vehicle to vehicle, V2X)

## Service Packages in This Architecture

### Vehicle Safety & Automation
*V2V, automated vehicles, platooning, collision avoidance, autonomous vehicle safety, basic safety, situational awareness, special vehicle alert, stop sign gap assist, road weather alert, restricted lane warnings, cooperative adaptive cruise control, METR, VRU clustering (also: vehicle to vehicle, V2X; also: self-driving, automated driving, ADS, ADAS, advanced driver assistance; also: winter maintenance, anti-icing, de-icing, snow removal, weather responsive management)*

- [Service Package VS07-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS07-01(MaineDOT))
- [Service Package VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS08-01(MaineDOT))
- [Service Package VS09-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS09-01(MaineDOT))
- [Service Package VS12-01(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS12-01(Co-Mun))
- [Service Package VS12-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS12-02(MaineDOT))

## Key Elements (13 total)

| Element | Status | Stakeholder |
|---------|--------|-------------|
| [511 Maine](https://www.consystec.com/maine2026/web/element.htm?id=115) | Existing | Maine Department of Transportation |
| [County/Municipal Connected Vehicle Equipment](https://www.consystec.com/maine2026/web/element.htm?id=261) | Planned | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal ITS Field Equipment](https://www.consystec.com/maine2026/web/element.htm?id=45) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal TOCs](https://www.consystec.com/maine2026/web/element.htm?id=51) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [MaineDOT Connected Vehicle Equipment](https://www.consystec.com/maine2026/web/element.htm?id=268) | Planned | Maine Department of Transportation |
| [MaineDOT ITS Field Devices](https://www.consystec.com/maine2026/web/element.htm?id=264) | Planned | Maine Department of Transportation |
| [MaineDOT Regional Facilities](https://www.consystec.com/maine2026/web/element.htm?id=119) | Existing | Maine Department of Transportation |
| [MaineDOT Signals Lab](https://www.consystec.com/maine2026/web/element.htm?id=149) | Existing | Maine Department of Transportation |
| [MaineDOT Statewide TMC](https://www.consystec.com/maine2026/web/element.htm?id=154) | Existing | Maine Department of Transportation |
| [Other Vehicle OBEs](https://www.consystec.com/maine2026/web/element.htm?id=255) | Planned | Private Travelers |
| [Private Third Party Information Providers](https://www.consystec.com/maine2026/web/element.htm?id=254) | Existing | Private Traffic Data Provider |
| [Private Travelers Personal Computing Devices](https://www.consystec.com/maine2026/web/element.htm?id=187) | Existing | Private Travelers |
| [Private Travelers Vehicles](https://www.consystec.com/maine2026/web/element.htm?id=252) | Existing | Private Travelers |

## Interfaces (57 data flows)

Real information flows between elements in this service area, in the form *Source Element → information flow → Destination Element*. Each links to its interface specification.

- 511 Maine → lane closure warning_ud → Private Travelers Vehicles — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- 511 Maine → queue warning information_ud → Private Travelers Vehicles — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- 511 Maine → road network environmental situation data → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-154)
- 511 Maine → road weather advisories → Private Travelers Vehicles (TPEG2 - Wide Area Broadcast) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- 511 Maine → speed warning_ud → Private Travelers Vehicles — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- County/Municipal Connected Vehicle Equipment → intersection geometry → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- County/Municipal Connected Vehicle Equipment → intersection safety application status → County/Municipal TOCs ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-261)
- County/Municipal Connected Vehicle Equipment → intersection safety warning → Private Travelers Vehicles (US: SAE Other J2735 - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- County/Municipal Connected Vehicle Equipment → intersection status → Private Travelers Personal Computing Devices (US: SAE Signal Control Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-261)
- County/Municipal Connected Vehicle Equipment → intersection status → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- County/Municipal Connected Vehicle Equipment → proxied personal location → Private Travelers Vehicles ((None-Data) - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- County/Municipal Connected Vehicle Equipment → signal service request → County/Municipal ITS Field Equipment (US: NTCIP Signal Priority - SNMPv3/TLS) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-261)
- County/Municipal ITS Field Equipment → intersection control status → County/Municipal Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-261)
- County/Municipal ITS Field Equipment → mixed use crossing status → County/Municipal Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-261)
- County/Municipal ITS Field Equipment → mixed use safety warning status → County/Municipal TOCs (US: NTCIP Traffic Signal - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-51)
- County/Municipal TOCs → intersection safety application info → County/Municipal Connected Vehicle Equipment ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-261)
- County/Municipal TOCs → mixed use safety warning control → County/Municipal ITS Field Equipment (US: NTCIP Traffic Signal - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-51)
- MaineDOT Connected Vehicle Equipment → intersection geometry → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- MaineDOT Connected Vehicle Equipment → intersection safety application status → MaineDOT Signals Lab ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=149-268)
- MaineDOT Connected Vehicle Equipment → intersection safety application status → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-268)
- MaineDOT Connected Vehicle Equipment → intersection safety warning → Private Travelers Vehicles (US: SAE Other J2735 - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- MaineDOT Connected Vehicle Equipment → intersection status → Private Travelers Personal Computing Devices (US: SAE Signal Control Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-268)
- MaineDOT Connected Vehicle Equipment → intersection status → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- MaineDOT Connected Vehicle Equipment → proxied personal location → Private Travelers Vehicles ((None-Data) - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- MaineDOT Connected Vehicle Equipment → signal service request → MaineDOT ITS Field Devices (US: NTCIP Signal Priority - SNMPv3/TLS) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- MaineDOT ITS Field Devices → environmental sensor data → MaineDOT Statewide TMC (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT ITS Field Devices → infrastructure restriction warning status → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT ITS Field Devices → intersection control status → MaineDOT Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- MaineDOT ITS Field Devices → mixed use crossing status → MaineDOT Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- MaineDOT ITS Field Devices → mixed use safety warning status → MaineDOT Signals Lab (US: NTCIP Traffic Signal - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=149-264)
- MaineDOT ITS Field Devices → mixed use safety warning status → MaineDOT Statewide TMC (US: NTCIP Traffic Signal - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT ITS Field Devices → roadway dynamic signage status → MaineDOT Statewide TMC (US: NTCIP Message Sign - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT ITS Field Devices → traffic images → MaineDOT Statewide TMC — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT ITS Field Devices → wrong way vehicle detected → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Signals Lab → intersection safety application info → MaineDOT Connected Vehicle Equipment ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=149-268)
- MaineDOT Signals Lab → mixed use safety warning control → MaineDOT ITS Field Devices (US: NTCIP Traffic Signal - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=149-264)
- MaineDOT Statewide TMC → environmental sensor control → MaineDOT ITS Field Devices (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Statewide TMC → infrastructure restriction warning control → MaineDOT ITS Field Devices ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Statewide TMC → intersection safety application info → MaineDOT Connected Vehicle Equipment ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-268)
- MaineDOT Statewide TMC → mixed use safety warning control → MaineDOT ITS Field Devices (US: NTCIP Traffic Signal - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Statewide TMC → road network conditions → 511 Maine (US: TMDD - NTCIP Messaging) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-154)
- MaineDOT Statewide TMC → roadway dynamic signage data → MaineDOT ITS Field Devices (US: NTCIP Message Sign - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Statewide TMC → speed monitoring control → MaineDOT ITS Field Devices (US: NTCIP Warning Device - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Other Vehicle OBEs → vehicle control event → Private Travelers Vehicles (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)
- Other Vehicle OBEs → vehicle location and motion → Private Travelers Vehicles (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)
- Private Third Party Information Providers → queue warning information_ud → Private Travelers Vehicles — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-254)
- Private Travelers Personal Computing Devices → personal location → County/Municipal Connected Vehicle Equipment (US: SAE VRU Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-261)
- Private Travelers Personal Computing Devices → personal location → MaineDOT Connected Vehicle Equipment (US: SAE VRU Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-268)
- Private Travelers Personal Computing Devices → personal signal service request → County/Municipal Connected Vehicle Equipment (US: SAE Other J2735 - Local Unicast Wireless (1609.2)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-261)
- Private Travelers Personal Computing Devices → personal signal service request → MaineDOT Connected Vehicle Equipment (US: SAE Other J2735 - Local Unicast Wireless (1609.2)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-268)
- Private Travelers Vehicles → intersection infringement info → County/Municipal Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Private Travelers Vehicles → intersection infringement info → MaineDOT Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Private Travelers Vehicles → vehicle control event → Other Vehicle OBEs (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)
- Private Travelers Vehicles → vehicle environmental data → 511 Maine (US: SAE Weather Info - Secure Wireless Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Private Travelers Vehicles → vehicle location and motion → County/Municipal Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Private Travelers Vehicles → vehicle location and motion → MaineDOT Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Private Travelers Vehicles → vehicle location and motion → Other Vehicle OBEs (US: SAE Basic Safety Messages - WAVE WSMP) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)

## Related Functional Requirements (7 found)

- [Functional Requirements: Vehicle Intersection Warning](https://www.consystec.com/maine2026/web/funreq.htm?id=1)
- [Functional Requirements: Transit Center Paratransit Operations](https://www.consystec.com/maine2026/web/funreq.htm?id=165)
- [Functional Requirements: CV On-Board Trip Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=195)
- [Functional Requirements: Vehicle Basic Safety Communication](https://www.consystec.com/maine2026/web/funreq.htm?id=39)
- [Functional Requirements: Transit Center Fixed-Route Operations](https://www.consystec.com/maine2026/web/funreq.htm?id=390)
- [Functional Requirements: Personal Pedestrian Safety](https://www.consystec.com/maine2026/web/funreq.htm?id=66)
- [Functional Requirements: Vehicle Basic Safety Communication](https://www.consystec.com/maine2026/web/funreq.htm?id=_el252)

## Deployment Guidance

When planning a deployment in Vehicle Safety:

1. **Identify the service packages** that apply to your use case from the list above.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
