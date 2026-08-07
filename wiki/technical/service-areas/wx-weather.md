# Weather (WX)

Road weather information systems, mobile weather observations. (also: winter maintenance, anti-icing, de-icing, snow removal, weather responsive management)

## Service Packages in This Architecture

### Weather Services
*RWIS, mobile observations, weather alerts, spot weather impact warning, roadway micro-prediction (also: road weather information system, ESS, environmental sensor station, weather station, road weather station)*

- [Service Package WX01-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX01-01(MaineDOT))
- [Service Package WX01-02(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX01-02(Co-Mun))
- [Service Package WX02-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX02-01(MaineDOT))
- [Service Package WX02-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX02-02(MaineDOT))
- [Service Package WX02-03(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX02-03(MaineDOT))
- [Service Package WX02-04(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX02-04(Co-Mun))
- [Service Package WX02-05(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX02-05(Co-Mun))
- [Service Package WX03-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX03-01(MaineDOT))
- [Service Package WX03-02(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/WX03-02(Co-Mun))

## Key Elements (22 total)

| Element | Status | Stakeholder |
|---------|--------|-------------|
| [511 Maine](https://www.consystec.com/maine2026/web/element.htm?id=115) | Existing | Maine Department of Transportation |
| [Amtrak Rail Operations Center](https://www.consystec.com/maine2026/web/element.htm?id=276) | Planned | Amtrak |
| [County/Municipal ITS Field Equipment](https://www.consystec.com/maine2026/web/element.htm?id=45) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal Public Safety Dispatch](https://www.consystec.com/maine2026/web/element.htm?id=89) | Existing | County/Municipal Public Safety Agencies |
| [County/Municipal Public Works Dispatch](https://www.consystec.com/maine2026/web/element.htm?id=47) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal TOCs](https://www.consystec.com/maine2026/web/element.htm?id=51) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal Website](https://www.consystec.com/maine2026/web/element.htm?id=52) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [Local Ferry Operations Centers](https://www.consystec.com/maine2026/web/element.htm?id=293) | Existing | Local Ferry Operators |
| [Local Transit Operations Centers](https://www.consystec.com/maine2026/web/element.htm?id=69) | Existing | Local Transit Agencies |
| [MEMA State EOC](https://www.consystec.com/maine2026/web/element.htm?id=102) | Existing | Maine Emergency Management Agency |
| [Maine State Police Dispatch](https://www.consystec.com/maine2026/web/element.htm?id=106) | Existing | Maine State Police |
| [Maine Turnpike Communications Center](https://www.consystec.com/maine2026/web/element.htm?id=278) | Planned | Maine Turnpike Authority |
| [MaineDOT ITS Field Devices](https://www.consystec.com/maine2026/web/element.htm?id=264) | Planned | Maine Department of Transportation |
| [MaineDOT Maintenance and Construction Systems](https://www.consystec.com/maine2026/web/element.htm?id=128) | Existing | Maine Department of Transportation |
| [MaineDOT Region Public Information Office](https://www.consystec.com/maine2026/web/element.htm?id=130) | Existing | Maine Department of Transportation |
| [MaineDOT Regional Facilities](https://www.consystec.com/maine2026/web/element.htm?id=119) | Existing | Maine Department of Transportation |
| [MaineDOT Statewide TMC](https://www.consystec.com/maine2026/web/element.htm?id=154) | Existing | Maine Department of Transportation |
| [National Weather Service](https://www.consystec.com/maine2026/web/element.htm?id=96) | Existing | NOAA |
| [Other County/Municipal Public Works Dispatch](https://www.consystec.com/maine2026/web/element.htm?id=172) | Planned | County/Municipal Traffic and Maintenance Agencies |
| [Private Travelers Vehicles](https://www.consystec.com/maine2026/web/element.htm?id=252) | Existing | Private Travelers |
| [Private Weather Information Provider](https://www.consystec.com/maine2026/web/element.htm?id=189) | Existing | Private Weather Information Provider |
| [Private Weather Support Services System](https://www.consystec.com/maine2026/web/element.htm?id=248) | Existing | Private Weather Information Provider |

## Interfaces (26 data flows)

Real information flows between elements in this service area, in the form *Source Element → information flow → Destination Element*. Each links to its interface specification.

- 511 Maine → ferry status_ud → Local Ferry Operations Centers — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-293)
- 511 Maine → road network environmental situation data → County/Municipal TOCs ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-115)
- 511 Maine → road network environmental situation data → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-154)
- 511 Maine → road weather advisories → Private Travelers Vehicles (TPEG2 - Wide Area Broadcast) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- County/Municipal ITS Field Equipment → environmental sensor data → County/Municipal Public Works Dispatch (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-47)
- County/Municipal ITS Field Equipment → environmental sensor data → County/Municipal TOCs (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-51)
- County/Municipal Public Works Dispatch → environmental sensor control → County/Municipal ITS Field Equipment (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-47)
- County/Municipal TOCs → environmental sensor control → County/Municipal ITS Field Equipment (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-51)
- County/Municipal TOCs → road network conditions → 511 Maine (US: TMDD - NTCIP Messaging) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-115)
- County/Municipal TOCs → road network conditions → County/Municipal Public Works Dispatch (US: TMDD - NTCIP Messaging) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=47-51)
- Local Ferry Operations Centers → ferry status_ud → 511 Maine — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-293)
- MaineDOT ITS Field Devices → environmental sensor data → MaineDOT Statewide TMC (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT ITS Field Devices → environmental sensor data → Private Weather Support Services System (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=248-264)
- MaineDOT ITS Field Devices → variable speed limit status → MaineDOT Statewide TMC (US: NTCIP Message Sign - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Statewide TMC → environmental sensor control → MaineDOT ITS Field Devices (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- MaineDOT Statewide TMC → road network conditions → 511 Maine (US: TMDD - NTCIP Messaging) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-154)
- MaineDOT Statewide TMC → variable speed limit control → MaineDOT ITS Field Devices (US: NTCIP Message Sign - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- National Weather Service → environmental conditions data status → 511 Maine — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=96-115)
- National Weather Service → qualified environmental conditions data → County/Municipal Public Works Dispatch — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=47-96)
- National Weather Service → qualified environmental conditions data → County/Municipal TOCs — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-96)
- Private Travelers Vehicles → vehicle environmental data → 511 Maine (US: SAE Weather Info - Secure Wireless Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Private Weather Information Provider → qualified environmental conditions data → County/Municipal Public Works Dispatch — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=47-189)
- Private Weather Information Provider → qualified environmental conditions data → County/Municipal TOCs — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-189)
- Private Weather Support Services System → environmental sensor control → MaineDOT ITS Field Devices (US: NTCIP Environmental Sensors - SNMPv1) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=248-264)
- Private Weather Support Services System → qualified environmental conditions data → 511 Maine ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-248)
- Private Weather Support Services System → qualified environmental conditions data → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-248)

## Applicable Standards (6)

Communication and data standards referenced by the interfaces above.

- **(None-Data) - Secure Internet (ITS)** — A bundle of standards (RFCs) that groups the common mgmt info bases (MIBs) used to manage IP networks at the transport layer and below using SNMPv3. ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=12106))
- **TPEG2 - Wide Area Broadcast** — Specifies ISO 21219-15, ISO 21219-24, ISO 21219-6, ISO 21219 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=58735))
- **US: NTCIP Environmental Sensors - SNMPv1** — Specifies NTCIP 1201, NTCIP 1204, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=62))
- **US: NTCIP Message Sign - SNMPv1** — Specifies NTCIP 1201, NTCIP 1203, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=54))
- **US: SAE Weather Info - Secure Wireless Internet (ITS)** — Specifies SAE J2735, SAE J2945 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=70538))
- **US: TMDD - NTCIP Messaging** — Specifies RFC 9293 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=142))

## Related Functional Requirements (33 found)

- [Functional Requirements: TMC Roadway Warning](https://www.consystec.com/maine2026/web/funreq.htm?id=108)
- [Functional Requirements: EV On-Board Incident Management Communication](https://www.consystec.com/maine2026/web/funreq.htm?id=149)
- [Functional Requirements: Transit Vehicle On-Board Information Services](https://www.consystec.com/maine2026/web/funreq.htm?id=160)
- [Functional Requirements: TIC Interactive Traveler Information](https://www.consystec.com/maine2026/web/funreq.htm?id=177)
- [Functional Requirements: MCM Winter Maintenance Management](https://www.consystec.com/maine2026/web/funreq.htm?id=214)
- [Functional Requirements: Emergency Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=225)
- [Functional Requirements: Vehicle Traveler Information Reception](https://www.consystec.com/maine2026/web/funreq.htm?id=23)
- [Functional Requirements: TIC Road Weather Advisories and Warnings](https://www.consystec.com/maine2026/web/funreq.htm?id=32)
- [Functional Requirements: Roadway Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=33)
- [Functional Requirements: MCV Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=34)
- [Functional Requirements: MCM Environmental Information Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=35)
- [Functional Requirements: TMC Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=36)
- [Functional Requirements: MCM Environmental Information Processing](https://www.consystec.com/maine2026/web/funreq.htm?id=38)
- [Functional Requirements: TMC Road Weather Advisories and Warnings](https://www.consystec.com/maine2026/web/funreq.htm?id=428)
- [Functional Requirements: Transit Center Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=431)
- [Functional Requirements: TIC Traveler Information Broadcast](https://www.consystec.com/maine2026/web/funreq.htm?id=55)
- [Functional Requirements: TIC Connected Vehicle Traveler Info Distribution](https://www.consystec.com/maine2026/web/funreq.htm?id=83)
- [Functional Requirements: TIC Interactive Traveler Information](https://www.consystec.com/maine2026/web/funreq.htm?id=_el104)
- [Functional Requirements: MCV Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=_el127)
- [Functional Requirements: TIC Connected Vehicle Traveler Info Distribution](https://www.consystec.com/maine2026/web/funreq.htm?id=_el130)
- [Functional Requirements: TIC Connected Vehicle Traveler Info Distribution](https://www.consystec.com/maine2026/web/funreq.htm?id=_el153)
- [Functional Requirements: MCM Environmental Information Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=_el168)
- [Functional Requirements: MCM Environmental Information Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=_el172)
- [Functional Requirements: MCM Environmental Information Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=_el177)
- [Functional Requirements: MCM Environmental Information Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=_el248)
- [Functional Requirements: TIC Connected Vehicle Traveler Info Distribution](https://www.consystec.com/maine2026/web/funreq.htm?id=_el254)
- [Functional Requirements: TIC Interactive Traveler Information](https://www.consystec.com/maine2026/web/funreq.htm?id=_el263)
- [Functional Requirements: Vehicle Traveler Information Reception](https://www.consystec.com/maine2026/web/funreq.htm?id=_el275)
- [Functional Requirements: Transit Center Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=_el293)
- [Functional Requirements: MCM Environmental Information Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=_el47)
- [Functional Requirements: MCV Environmental Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=_el48)
- [Functional Requirements: TIC Connected Vehicle Traveler Info Distribution](https://www.consystec.com/maine2026/web/funreq.htm?id=_el52)
- [Functional Requirements: TIC Connected Vehicle Traveler Info Distribution](https://www.consystec.com/maine2026/web/funreq.htm?id=_el68)

## Deployment Guidance

When planning a deployment in Weather:

1. **Identify the service packages** that apply to your use case from the list above.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
