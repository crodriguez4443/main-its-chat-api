# Sustainable Transport (ST)

Congestion pricing, transit incentives, emissions management. (also: road pricing, cordon pricing, value pricing, dynamic pricing, tolling for congestion)

## Service Packages in This Architecture

### Sustainable Transport
*Congestion pricing, transit incentives, alternative fuel support, eco-traffic metering, roadside lighting, eco-lanes, eco-approach at signals, low emissions zone management (also: road pricing, cordon pricing, value pricing, dynamic pricing, tolling for congestion)*

- [Service Package mpSH1_ST04-02(Co-Mun)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH1_ST04-02(Co-Mun))
- [Service Package mpSH3_ST04-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_ST04-01(MaineDOT))
- [Service Package mpSH109_ST05-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH109_ST05-01(MaineDOT))
- [Service Package mpSH109_ST05-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH109_ST05-02(MaineDOT))
- [Service Package mpSH1_ST05-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH1_ST05-02(MaineDOT))
- [Service Package mpSH3_ST05-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH3_ST05-01(MaineDOT))
- [Service Package mpSH5_ST05-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_ST05-01(MaineDOT))
- [Service Package mpSH5_ST05-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH5_ST05-02(MaineDOT))
- [Service Package mpSH83_ST05-01(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH83_ST05-01(MaineDOT))
- [Service Package mpSH83_ST05-02(MaineDOT)](https://www.consystec.com/maine2026/web/spinstance.htm?id=/mpSH83_ST05-02(MaineDOT))

## Key Elements (10 total)

| Element | Status | Stakeholder |
|---------|--------|-------------|
| [511 Maine](https://www.consystec.com/maine2026/web/element.htm?id=115) | Existing | Maine Department of Transportation |
| [County/Municipal ITS Field Equipment](https://www.consystec.com/maine2026/web/element.htm?id=45) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal TOCs](https://www.consystec.com/maine2026/web/element.htm?id=51) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [County/Municipal Website](https://www.consystec.com/maine2026/web/element.htm?id=52) | Existing | County/Municipal Traffic and Maintenance Agencies |
| [Electric Vehicle Charging Stations](https://www.consystec.com/maine2026/web/element.htm?id=270) | Planned | Electric Vehicle Charging Organizations |
| [MaineDOT ITS Field Devices](https://www.consystec.com/maine2026/web/element.htm?id=264) | Planned | Maine Department of Transportation |
| [MaineDOT Regional Facilities](https://www.consystec.com/maine2026/web/element.htm?id=119) | Existing | Maine Department of Transportation |
| [MaineDOT Statewide TMC](https://www.consystec.com/maine2026/web/element.htm?id=154) | Existing | Maine Department of Transportation |
| [Private Third Party Information Providers](https://www.consystec.com/maine2026/web/element.htm?id=254) | Existing | Private Traffic Data Provider |
| [Private Travelers Vehicles](https://www.consystec.com/maine2026/web/element.htm?id=252) | Existing | Private Travelers |

## Interfaces (2 data flows)

Real information flows between elements in this service area, in the form *Source Element → information flow → Destination Element*. Each links to its interface specification.

- County/Municipal Website → electric charging services inventory → Private Travelers Vehicles ((None-Data) - Secure Wireless Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=52-252)
- Private Third Party Information Providers → electric charging services inventory → Private Travelers Vehicles ((None-Data) - Secure Wireless Internet (ITS)) — [interface](https://www.consystec.com/maine2026/web/interface.htm?id=252-254)

## Applicable Standards (1)

Communication and data standards referenced by the interfaces above.

- **(None-Data) - Secure Wireless Internet (ITS)** — A bundle of standards (RFCs) that groups the common mgmt info bases (MIBs) used to manage IP networks at the transport layer and below using SNMPv3. ([standard](https://www.consystec.com/maine2026/web/solution.htm?id=55280))

## Related Functional Requirements (2 found)

- [Functional Requirements: RSE Situation Monitoring](https://www.consystec.com/maine2026/web/funreq.htm?id=180)
- [Functional Requirements: TMC Traffic Network Performance Evaluation](https://www.consystec.com/maine2026/web/funreq.htm?id=384)

## Deployment Guidance

When planning a deployment in Sustainable Transport:

1. **Identify the service packages** that apply to your use case from the list above.
2. **Review the elements** — these are the systems and devices you will need. Check their Status (Existing vs Planned) to understand what is already deployed.
3. **Look up the functional requirements** — these define WHAT each element must do. They map directly to RFP/RFI specification sections.
4. **Check the interfaces** — these define HOW elements communicate. Each interface specifies data flows and applicable standards.
5. **Reference the standards** — for each interface, the architecture specifies which standards (NTCIP, TMDD, SAE, IEEE, etc.) should be used.

For a DOT preparing an RFI/RFP, the functional requirements are your specification backbone. Each requirement can be traced from service package → element → functional requirement → interface → standard.
