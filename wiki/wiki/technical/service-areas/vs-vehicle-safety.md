# Vehicle Safety (VS)

V2V safety, automated driving, platooning, collision avoidance. (also: vehicle to vehicle, V2X)

## Service Packages in This Architecture

### Vehicle Safety & Automation
*V2V, automated vehicles, platooning, collision avoidance, autonomous vehicle safety, basic safety, situational awareness, special vehicle alert, stop sign gap assist, road weather alert, restricted lane warnings, cooperative adaptive cruise control, METR, VRU clustering (also: vehicle to vehicle, V2X; also: self-driving, automated driving, ADS, ADAS, advanced driver assistance; also: winter maintenance, anti-icing, de-icing, snow removal, weather responsive management)*

- [Service Package mpSH3_VS07-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS07-01(MaineDOT))
- [Service Package mpSH5_VS07-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS07-01(MaineDOT))
- [Service Package mpSH3_VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS08-01(MaineDOT))
- [Service Package mpSH5_VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS08-01(MaineDOT))
- [Service Package mpSH83_VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH83_VS08-01(MaineDOT))
- [Service Package mpSH3_VS09-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS09-01(MaineDOT))
- [Service Package mpSH5_VS09-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS09-01(MaineDOT))
- [Service Package mpSH1_VS12-01(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH1_VS12-01(Co-Mun))
- [Service Package mpSH3_VS12-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS12-02(MaineDOT))
- [Service Package mpSH5_VS12-01(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS12-01(Co-Mun))
- [Service Package mpSH5_VS12-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS12-02(MaineDOT))

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
