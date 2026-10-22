# Performance Management (PM)

Regional planning data, scenario modeling, emissions monitoring.

## Service Packages in This Architecture

### Performance Management
*Planning data, performance dashboards, emissions tracking, loading zone management*

- [Service Package mpSH21_PM01-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH21_PM01-01(Transit))
- [Service Package mpSH3_PM01-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_PM01-02(MaineDOT))
- [Service Package PM01-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/PM01-01(Transit))
- [Service Package PM01-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/PM01-02(MaineDOT))
- [Service Package mpSH21_PM02-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH21_PM02-01(Transit))
- [Service Package mpSH3_PM02-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_PM02-02(MaineDOT))
- [Service Package PM02-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/PM02-01(Transit))
- [Service Package PM02-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/PM02-02(MaineDOT))
- [Service Package mpSH21_PM03-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH21_PM03-01(Transit))
- [Service Package mpSH26_PM03-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH26_PM03-01(Transit))
- [Service Package mpSH26_PM03-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH26_PM03-02(MaineDOT))
- [Service Package mpSH3_PM03-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_PM03-02(MaineDOT))
- [Service Package PM03-01(Transit)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/PM03-01(Transit))
- [Service Package PM03-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/PM03-02(MaineDOT))

## Key Elements (12 total)

| Element | Status | Stakeholder |
|---------|--------|-------------|
| [511 Maine](https://www.consystec.com/maine2026/web/element.htm?id=115) | Existing | Maine Department of Transportation |
| [Financial Institution](https://www.consystec.com/maine2026/web/element.htm?id=60) | Existing | Financial Institution |
| [Local Transit Operations Centers](https://www.consystec.com/maine2026/web/element.htm?id=69) | Existing | Local Transit Agencies |
| [Local Transit Parking Systems](https://www.consystec.com/maine2026/web/element.htm?id=290) | Planned | Local Transit Agencies |
| [Local Transit Payment Device](https://www.consystec.com/maine2026/web/element.htm?id=292) | Planned | Local Transit Agencies |
| [Local Transit Stations and Shelters](https://www.consystec.com/maine2026/web/element.htm?id=273) | Planned | Local Transit Agencies |
| [Local Transit Traveler Information Systems](https://www.consystec.com/maine2026/web/element.htm?id=70) | Planned | Local Transit Agencies |
| [MaineDOT Ferries Operations Centers](https://www.consystec.com/maine2026/web/element.htm?id=297) | Planned | Maine Department of Transportation |
| [MaineDOT Ferries Payment Device](https://www.consystec.com/maine2026/web/element.htm?id=299) | Planned | Maine Department of Transportation |
| [MaineDOT Ferries Stations](https://www.consystec.com/maine2026/web/element.htm?id=300) | Planned | Maine Department of Transportation |
| [MaineDOT Ferries Traveler Information Systems](https://www.consystec.com/maine2026/web/element.htm?id=301) | Planned | Maine Department of Transportation |
| [MaineDOT Parking Systems](https://www.consystec.com/maine2026/web/element.htm?id=298) | Planned | Maine Department of Transportation |

## Interfaces (12 data flows)

Real information flows between elements in this service area, in the form *Source Element → information flow → Destination Element*. Each links to its interface specification.

- Interface: Financial Institution → settlement → Local Transit Operations Centers — [settlement interface](https://www.consystec.com/maine2026/web/interface.htm?id=60-69)
- Interface: Financial Institution → settlement → MaineDOT Ferries Operations Centers — [settlement interface](https://www.consystec.com/maine2026/web/interface.htm?id=60-297)
- Interface: Local Transit Operations Centers → parking area transit information_ud → Local Transit Stations and Shelters — [parking area transit information_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=69-273)
- Interface: Local Transit Operations Centers → parking payment instructions → Local Transit Parking Systems ((None-Data) - Secure Internet (ITS)) — [parking payment instructions interface](https://www.consystec.com/maine2026/web/interface.htm?id=69-290)
- Interface: Local Transit Operations Centers → payment request → Financial Institution — [payment request interface](https://www.consystec.com/maine2026/web/interface.htm?id=60-69)
- Interface: Local Transit Parking Systems → parking payment transactions → Local Transit Operations Centers ((None-Data) - Secure Internet (ITS)) — [parking payment transactions interface](https://www.consystec.com/maine2026/web/interface.htm?id=69-290)
- Interface: Local Transit Parking Systems → request for payment → Local Transit Payment Device — [request for payment interface](https://www.consystec.com/maine2026/web/interface.htm?id=290-292)
- Interface: MaineDOT Ferries Operations Centers → parking area transit information_ud → MaineDOT Ferries Stations — [parking area transit information_ud interface](https://www.consystec.com/maine2026/web/interface.htm?id=297-300)
- Interface: MaineDOT Ferries Operations Centers → parking payment instructions → MaineDOT Parking Systems ((None-Data) - Secure Internet (ITS)) — [parking payment instructions interface](https://www.consystec.com/maine2026/web/interface.htm?id=297-298)
- Interface: MaineDOT Ferries Operations Centers → payment request → Financial Institution — [payment request interface](https://www.consystec.com/maine2026/web/interface.htm?id=60-297)
- Interface: MaineDOT Parking Systems → parking payment transactions → MaineDOT Ferries Operations Centers ((None-Data) - Secure Internet (ITS)) — [parking payment transactions interface](https://www.consystec.com/maine2026/web/interface.htm?id=297-298)
- Interface: MaineDOT Parking Systems → request for payment → MaineDOT Ferries Payment Device — [request for payment interface](https://www.consystec.com/maine2026/web/interface.htm?id=298-299)

## Applicable Standards (1)

Communication and data standards referenced by the interfaces above.

- **(None-Data) - Secure Internet (ITS)** — A bundle of standards (RFCs) that groups the common mgmt info bases (MIBs) used to manage IP networks at the transport layer and below using SNMPv3. ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=12106))

## Related Functional Requirements (10 found)

- [Functional Requirements: Transit Center Paratransit Operations](https://www.consystec.com/maine2026/web/funreq.htm?id=165)
- [Functional Requirements: RSE Situation Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=180)
- [Functional Requirements: TIC Freight-Specific Travel Planning](https://www.consystec.com/maine2026/web/funreq.htm?id=196)
- [Functional Requirements: Archive Situation Data Archival](https://www.consystec.com/maine2026/web/funreq.htm?id=219)
- [Functional Requirements: Parking Coordination](https://www.consystec.com/maine2026/web/funreq.htm?id=337)
- [Functional Requirements: Roadway Data Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=350)
- [Functional Requirements: TMC Traffic Network Performance Evaluation](https://www.consystec.com/maine2026/web/funreq.htm?id=384)
- [Functional Requirements: Personal Trip Planning and Route Guidance](https://www.consystec.com/maine2026/web/funreq.htm?id=9)
- [Functional Requirements: TIC Trip Planning](https://www.consystec.com/maine2026/web/funreq.htm?id=96)
- [Functional Requirements: Roadway Data Collection](https://www.consystec.com/maine2026/web/funreq.htm?id=_el82)

## Deployment Guidance

When planning a deployment in Performance Management:

1. **Identify the service packages** that apply to your use case from the list above.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
