# Vehicle Safety (VS)

V2V safety, automated driving, platooning, collision avoidance. (also: vehicle to vehicle, V2X)

## Service Packages in This Architecture

### Vehicle Safety & Automation
*V2V, automated vehicles, platooning, collision avoidance, autonomous vehicle safety, basic safety, situational awareness, special vehicle alert, stop sign gap assist, road weather alert, restricted lane warnings, cooperative adaptive cruise control, METR, VRU clustering (also: vehicle to vehicle, V2X; also: self-driving, automated driving, ADS, ADAS, advanced driver assistance; also: winter maintenance, anti-icing, de-icing, snow removal, weather responsive management)*

- [Service Package mpSH3_VS07-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS07-01(MaineDOT))
- [Service Package mpSH5_VS07-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS07-01(MaineDOT))
- [Service Package VS07-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS07-01(MaineDOT))
- [Service Package mpSH3_VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS08-01(MaineDOT))
- [Service Package mpSH5_VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS08-01(MaineDOT))
- [Service Package mpSH83_VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH83_VS08-01(MaineDOT))
- [Service Package VS08-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS08-01(MaineDOT))
- [Service Package mpSH3_VS09-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS09-01(MaineDOT))
- [Service Package mpSH5_VS09-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS09-01(MaineDOT))
- [Service Package VS09-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS09-01(MaineDOT))
- [Service Package mpSH1_VS12-01(MPO-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH1_VS12-01(MPO-Mun))
- [Service Package mpSH3_VS12-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS12-02(MaineDOT))
- [Service Package mpSH5_VS12-01(MPO-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS12-01(MPO-Mun))
- [Service Package mpSH5_VS12-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS12-02(MaineDOT))
- [Service Package VS12-01(MPO-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS12-01(MPO-Mun))
- [Service Package VS12-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS12-02(MaineDOT))
- [Service Package mpSH3_VS13-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_VS13-01(MaineDOT))
- [Service Package mpSH5_VS13-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_VS13-01(MaineDOT))
- [Service Package VS13-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/VS13-01(MaineDOT))

## Key Elements (11 total)

| Element | Status | Stakeholder |
|---------|--------|-------------|
| [511 Maine](https://www.consystec.com/maine2026/web/element.htm?id=115) | Existing | Maine Department of Transportation |
| [MPO/Municipal Connected Vehicle Equipment](https://www.consystec.com/maine2026/web/element.htm?id=261) | Planned | MPO/Municipal Traffic and Maintenance Agencies |
| [MPO/Municipal ITS Field Equipment](https://www.consystec.com/maine2026/web/element.htm?id=45) | Existing | MPO/Municipal Traffic and Maintenance Agencies |
| [MPO/Municipal Traffic Management Systems](https://www.consystec.com/maine2026/web/element.htm?id=51) | Existing | MPO/Municipal Traffic and Maintenance Agencies |
| [Maine Link](https://www.consystec.com/maine2026/web/element.htm?id=294) | Existing | Maine Department of Transportation |
| [MaineDOT Connected Vehicle Equipment](https://www.consystec.com/maine2026/web/element.htm?id=268) | Planned | Maine Department of Transportation |
| [MaineDOT ITS Field Devices](https://www.consystec.com/maine2026/web/element.htm?id=264) | Planned | Maine Department of Transportation |
| [Other Vehicle OBEs](https://www.consystec.com/maine2026/web/element.htm?id=255) | Planned | Private Travelers |
| [Private Third Party Information Providers](https://www.consystec.com/maine2026/web/element.htm?id=254) | Existing | Private Traffic Data Provider |
| [Private Travelers Personal Computing Devices](https://www.consystec.com/maine2026/web/element.htm?id=187) | Existing | Private Travelers |
| [Private Travelers Vehicles](https://www.consystec.com/maine2026/web/element.htm?id=252) | Existing | Private Travelers |

## Interfaces (64 data flows)

Real information flows between elements in this service area, in the form *Source Element → information flow → Destination Element*. Each links to its interface specification.

- Interface: 511 Maine → lane closure warning_ud → Private Travelers Vehicles — [lane closure warning_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Interface: 511 Maine → queue warning information_ud → Private Travelers Vehicles — [queue warning information_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Interface: 511 Maine → road network environmental situation data → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [road network environmental situation data interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-154)
- Interface: 511 Maine → road weather advisories → Private Travelers Vehicles (TPEG2 - Wide Area Broadcast) — [road weather advisories interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Interface: 511 Maine → speed warning_ud → Private Travelers Vehicles — [speed warning_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Interface: MPO/Municipal Connected Vehicle Equipment → intersection geometry → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [intersection geometry interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Interface: MPO/Municipal Connected Vehicle Equipment → intersection safety application status → MPO/Municipal Traffic Management Systems ((None-Data) - Secure Internet (ITS)) — [intersection safety application status interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-261)
- Interface: MPO/Municipal Connected Vehicle Equipment → intersection safety warning → Private Travelers Vehicles (US: SAE Other J2735 - WAVE WSMP) — [intersection safety warning interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Interface: MPO/Municipal Connected Vehicle Equipment → intersection status → Private Travelers Personal Computing Devices (US: SAE Signal Control Messages - WAVE WSMP) — [intersection status interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-261)
- Interface: MPO/Municipal Connected Vehicle Equipment → intersection status → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [intersection status interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Interface: MPO/Municipal Connected Vehicle Equipment → proxied personal location → Private Travelers Vehicles ((None-Data) - WAVE WSMP) — [proxied personal location interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Interface: MPO/Municipal Connected Vehicle Equipment → signal service request → MPO/Municipal ITS Field Equipment (US: NTCIP Signal Priority - SNMPv3/TLS) — [signal service request interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-261)
- Interface: MPO/Municipal ITS Field Equipment → intersection control status → MPO/Municipal Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [intersection control status interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-261)
- Interface: MPO/Municipal ITS Field Equipment → mixed use crossing status → MPO/Municipal Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [mixed use crossing status interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-261)
- Interface: MPO/Municipal ITS Field Equipment → mixed use safety warning status → MPO/Municipal Traffic Management Systems (US: NTCIP Traffic Signal - SNMPv1) — [mixed use safety warning status interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-51)
- Interface: MPO/Municipal Traffic Management Systems → intersection safety application info → MPO/Municipal Connected Vehicle Equipment ((None-Data) - Secure Internet (ITS)) — [intersection safety application info interface](https://www.consystec.com/maine2026/web/interface.htm?id=51-261)
- Interface: MPO/Municipal Traffic Management Systems → mixed use safety warning control → MPO/Municipal ITS Field Equipment (US: NTCIP Traffic Signal - SNMPv1) — [mixed use safety warning control interface](https://www.consystec.com/maine2026/web/interface.htm?id=45-51)
- Interface: Maine Link → intersection safety application info → MaineDOT Connected Vehicle Equipment ((None-Data) - Secure Internet (ITS)) — [intersection safety application info interface](https://www.consystec.com/maine2026/web/interface.htm?id=268-294)
- Interface: Maine Link → mixed use safety warning control → MaineDOT ITS Field Devices (US: NTCIP Traffic Signal - SNMPv1) — [mixed use safety warning control interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-294)
- Interface: Maine Link → signal control commands → MaineDOT ITS Field Devices (US: NTCIP Signal System Masters - SNMPv1) — [signal control commands interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-294)
- Interface: MaineDOT Connected Vehicle Equipment → intersection geometry → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [intersection geometry interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Interface: MaineDOT Connected Vehicle Equipment → intersection infringement info → MaineDOT ITS Field Devices ((None-Data) - Secure Internet (ITS)) — [intersection infringement info interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- Interface: MaineDOT Connected Vehicle Equipment → intersection safety application status → Maine Link ((None-Data) - Secure Internet (ITS)) — [intersection safety application status interface](https://www.consystec.com/maine2026/web/interface.htm?id=268-294)
- Interface: MaineDOT Connected Vehicle Equipment → intersection safety application status → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [intersection safety application status interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-268)
- Interface: MaineDOT Connected Vehicle Equipment → intersection safety warning → Private Travelers Vehicles (US: SAE Other J2735 - WAVE WSMP) — [intersection safety warning interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Interface: MaineDOT Connected Vehicle Equipment → intersection status → Private Travelers Personal Computing Devices (US: SAE Signal Control Messages - WAVE WSMP) — [intersection status interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-268)
- Interface: MaineDOT Connected Vehicle Equipment → intersection status → Private Travelers Vehicles (US: SAE Signal Control Messages - WAVE WSMP) — [intersection status interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Interface: MaineDOT Connected Vehicle Equipment → intersection status monitoring → MaineDOT ITS Field Devices (US: SAE Signal Control Messages - WAVE WSMP) — [intersection status monitoring interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- Interface: MaineDOT Connected Vehicle Equipment → proxied personal location → Private Travelers Vehicles ((None-Data) - WAVE WSMP) — [proxied personal location interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Interface: MaineDOT Connected Vehicle Equipment → signal service request → MaineDOT ITS Field Devices (US: NTCIP Signal Priority - SNMPv3/TLS) — [signal service request interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- Interface: MaineDOT ITS Field Devices → environmental sensor data → MaineDOT Statewide TMC (US: NTCIP Environmental Sensors - SNMPv1) — [environmental sensor data interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT ITS Field Devices → infrastructure restriction warning status → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [infrastructure restriction warning status interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT ITS Field Devices → intersection control status → MaineDOT Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [intersection control status interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- Interface: MaineDOT ITS Field Devices → mixed use crossing status → MaineDOT Connected Vehicle Equipment (US: NTCIP Traffic Signal - SNMPv3/TLS) — [mixed use crossing status interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-268)
- Interface: MaineDOT ITS Field Devices → mixed use safety warning status → Maine Link (US: NTCIP Traffic Signal - SNMPv1) — [mixed use safety warning status interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-294)
- Interface: MaineDOT ITS Field Devices → mixed use safety warning status → MaineDOT Statewide TMC (US: NTCIP Traffic Signal - SNMPv1) — [mixed use safety warning status interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT ITS Field Devices → roadway dynamic signage status → MaineDOT Statewide TMC (US: NTCIP Message Sign - SNMPv1) — [roadway dynamic signage status interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT ITS Field Devices → signal control status → Maine Link (US: NTCIP Traffic Signal - SNMPv1) — [signal control status interface](https://www.consystec.com/maine2026/web/interface.htm?id=264-294)
- Interface: MaineDOT ITS Field Devices → signal control status → MaineDOT Statewide TMC (US: NTCIP Traffic Signal - SNMPv1) — [signal control status interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT ITS Field Devices → traffic images → MaineDOT Statewide TMC — [traffic images interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT ITS Field Devices → wrong way vehicle detected → MaineDOT Statewide TMC ((None-Data) - Secure Internet (ITS)) — [wrong way vehicle detected interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT Statewide TMC → environmental sensor control → MaineDOT ITS Field Devices (US: NTCIP Environmental Sensors - SNMPv1) — [environmental sensor control interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT Statewide TMC → infrastructure restriction warning control → MaineDOT ITS Field Devices ((None-Data) - Secure Internet (ITS)) — [infrastructure restriction warning control interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT Statewide TMC → intersection safety application info → MaineDOT Connected Vehicle Equipment ((None-Data) - Secure Internet (ITS)) — [intersection safety application info interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-268)
- Interface: MaineDOT Statewide TMC → mixed use safety warning control → MaineDOT ITS Field Devices (US: NTCIP Traffic Signal - SNMPv1) — [mixed use safety warning control interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT Statewide TMC → queue warning information_ud → Private Travelers Vehicles — [queue warning information_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-252)
- Interface: MaineDOT Statewide TMC → road network conditions → 511 Maine (US: TMDD - NTCIP Messaging) — [road network conditions interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-154)
- Interface: MaineDOT Statewide TMC → roadway dynamic signage data → MaineDOT ITS Field Devices (US: NTCIP Message Sign - SNMPv1) — [roadway dynamic signage data interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT Statewide TMC → signal control commands → MaineDOT ITS Field Devices (US: NTCIP Signal System Masters - SNMPv1) — [signal control commands interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: MaineDOT Statewide TMC → speed monitoring control → MaineDOT ITS Field Devices (US: NTCIP Warning Device - SNMPv1) — [speed monitoring control interface](https://www.consystec.com/maine2026/web/interface.htm?id=154-264)
- Interface: Other Vehicle OBEs → vehicle control event → Private Travelers Vehicles (US: SAE Basic Safety Messages - WAVE WSMP) — [vehicle control event interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)
- Interface: Other Vehicle OBEs → vehicle location and motion → Private Travelers Vehicles (US: SAE Basic Safety Messages - WAVE WSMP) — [vehicle location and motion interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)
- Interface: Private Third Party Information Providers → queue warning information_ud → Private Travelers Vehicles — [queue warning information_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-254)
- Interface: Private Travelers Personal Computing Devices → personal location → MPO/Municipal Connected Vehicle Equipment (US: SAE VRU Messages - WAVE WSMP) — [personal location interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-261)
- Interface: Private Travelers Personal Computing Devices → personal location → MaineDOT Connected Vehicle Equipment (US: SAE VRU Messages - WAVE WSMP) — [personal location interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-268)
- Interface: Private Travelers Personal Computing Devices → personal signal service request → MPO/Municipal Connected Vehicle Equipment (US: SAE Other J2735 - Local Unicast Wireless (1609.2)) — [personal signal service request interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-261)
- Interface: Private Travelers Personal Computing Devices → personal signal service request → MaineDOT Connected Vehicle Equipment (US: SAE Other J2735 - Local Unicast Wireless (1609.2)) — [personal signal service request interface](https://www.consystec.com/maine2026/web/interface.htm?id=187-268)
- Interface: Private Travelers Vehicles → intersection infringement info → MPO/Municipal Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [intersection infringement info interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Interface: Private Travelers Vehicles → intersection infringement info → MaineDOT Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [intersection infringement info interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Interface: Private Travelers Vehicles → vehicle control event → Other Vehicle OBEs (US: SAE Basic Safety Messages - WAVE WSMP) — [vehicle control event interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)
- Interface: Private Travelers Vehicles → vehicle environmental data → 511 Maine (US: SAE Weather Info - Secure Wireless Internet (ITS)) — [vehicle environmental data interface](https://www.consystec.com/maine2026/web/interface.htm?id=115-252)
- Interface: Private Travelers Vehicles → vehicle location and motion → MPO/Municipal Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [vehicle location and motion interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-261)
- Interface: Private Travelers Vehicles → vehicle location and motion → MaineDOT Connected Vehicle Equipment (US: SAE Basic Safety Messages - WAVE WSMP) — [vehicle location and motion interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-268)
- Interface: Private Travelers Vehicles → vehicle location and motion → Other Vehicle OBEs (US: SAE Basic Safety Messages - WAVE WSMP) — [vehicle location and motion interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-255)

## Applicable Standards (17)

Communication and data standards referenced by the interfaces above.

- **(None-Data) - Secure Internet (ITS)** — A bundle of standards (RFCs) that groups the common mgmt info bases (MIBs) used to manage IP networks at the transport layer and below using SNMPv3. ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=12106))
- **(None-Data) - WAVE WSMP** — Specifies IEEE 1609.3, IEEE 1609.2 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=244))
- **TPEG2 - Wide Area Broadcast** — Specifies ISO 21219-15, ISO 21219-24, ISO 21219-6, ISO 21219 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=58735))
- **US: NTCIP Environmental Sensors - SNMPv1** — Specifies NTCIP 1201, NTCIP 1204, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=62))
- **US: NTCIP Message Sign - SNMPv1** — Specifies NTCIP 1201, NTCIP 1203, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=54))
- **US: NTCIP Signal Priority - SNMPv3/TLS** — Specifies NTCIP 1201, NTCIP 1202, NTCIP 1211, ISO 15784-2, RFC 6353 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=57))
- **US: NTCIP Signal System Masters - SNMPv1** — Specifies NTCIP 1201, NTCIP 1202, NTCIP 1210, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=121))
- **US: NTCIP Traffic Signal - SNMPv1** — Specifies NTCIP 1201, NTCIP 1202, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=40))
- **US: NTCIP Traffic Signal - SNMPv3/TLS** — Specifies NTCIP 1201, NTCIP 1202, ISO 15784-2, RFC 6353 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=41))
- **US: NTCIP Warning Device - SNMPv1** — Specifies NTCIP 1201, NTCIP 1203, NTCIP 1205, NTCIP 1209, NTCIP 2301 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=102))
- **US: SAE Basic Safety Messages - WAVE WSMP** — Specifies SAE J2735, SAE J2945, IEEE 1609.3, IEEE 1609.2 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=15))
- **US: SAE Other J2735 - Local Unicast Wireless (1609.2)** — Specifies SAE J2735, SAE J2945, IEEE 1609.3, IEEE 1609.2 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=21460))
- **US: SAE Other J2735 - WAVE WSMP** — Specifies SAE J2735, SAE J2945, IEEE 1609.3, IEEE 1609.2 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=66))
- **US: SAE Signal Control Messages - WAVE WSMP** — Specifies SAE J2735, SAE J2945, ISO 19091, IEEE 1609.3, IEEE 1609.2 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=16))
- **US: SAE VRU Messages - WAVE WSMP** — Specifies SAE J2735, SAE J2945, IEEE 1609.3, IEEE 1609.2 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=17))
- **US: SAE Weather Info - Secure Wireless Internet (ITS)** — Specifies SAE J2735, SAE J2945 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=70538))
- **US: TMDD - NTCIP Messaging** — Specifies RFC 9293 ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=142))

## Related Functional Requirements (6 found)

- [Functional Requirements: Vehicle Intersection Warning](https://www.consystec.com/maine2026/web/funreq.htm?id=1)
- [Functional Requirements: Transit Center Paratransit Operations](https://www.consystec.com/maine2026/web/funreq.htm?id=165)
- [Functional Requirements: CV On-Board Trip Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=195)
- [Functional Requirements: Vehicle Basic Safety Communication](https://www.consystec.com/maine2026/web/funreq.htm?id=39)
- [Functional Requirements: Transit Center Fixed-Route Operations](https://www.consystec.com/maine2026/web/funreq.htm?id=390)
- [Functional Requirements: Personal Pedestrian Safety](https://www.consystec.com/maine2026/web/funreq.htm?id=66)

## Deployment Guidance

When planning a deployment in Vehicle Safety:

1. **Identify the service packages** that apply to your use case from the list above.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
