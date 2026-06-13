"""
GIDEON OT/ICS Security Module
==============================
Scenario-based PBQ generator for OT/ICS Security for IT Professionals.
Covers: Architecture, Threat Landscape, Frameworks, Defensive Controls,
Incident Response, and IT/OT Convergence.

No LLM required - instant generation from randomised templates.
Standalone module - not tied to any specific exam.
"""

import random

OT_MODULE_INFO = {
    "name": "OT/ICS Security",
    "version": "1.0",
    "description": "Operational Technology and Industrial Control Systems Security",
    "frameworks": ["IEC 62443", "NIST SP 800-82", "MITRE ATT&CK for ICS"],
}

# ================================================================
# SECTION 1 - OT/ICS ARCHITECTURE SCENARIOS
# ================================================================

ARCHITECTURE_SCENARIOS = [
    {
        "id": "OT-ARCH-001",
        "domain": "OT/ICS Architecture",
        "sub_topic": "Purdue Model and Network Segmentation",
        "difficulty": "beginner",
        "objective": "Understand the Purdue Enterprise Reference Architecture",
        "scenario_template": """
You are an IT security professional transitioning into an OT security role
at a {industry} company. Your manager asks you to review the network
architecture of the facility.

The current architecture shows:
  - Level 0: Field devices — {field_devices} on the plant floor
  - Level 1: Controllers — {controllers} managing physical processes
  - Level 2: Supervisory — {hmi_system} SCADA/HMI systems
  - Level 3: Operations — Manufacturing execution systems (MES)
  - Level 4/5: Enterprise — Corporate IT network with internet access

The review reveals:
  - Levels 0-2 have DIRECT network connectivity to Level 4/5
  - Engineering workstations at Level 2 browse the internet
  - No DMZ exists between OT and IT networks
  - Remote vendor access connects directly to Level 1 controllers

Questions:
1. What is the Purdue Model and why is it the foundation of OT network
   security architecture? Explain each level briefly.

2. Identify THREE critical security violations in the architecture described
   above. For each violation explain the specific risk it introduces.

3. A {attack_type} attack enters through the corporate IT network at Level 5.
   Given the current architecture, explain how it could propagate to Level 0
   field devices and what physical consequences could result in a {industry}.

4. Design a secure architecture recommendation including:
   - Where to place a DMZ
   - What controls to implement at each boundary
   - How to handle vendor remote access securely

5. Why is the principle of least privilege MORE critical in OT environments
   than in traditional IT environments?
""",
        "variables": {
            "industry": [
                "water treatment facility",
                "electricity generation plant",
                "oil and gas pipeline operator",
                "pharmaceutical manufacturing plant",
                "food and beverage manufacturer",
            ],
            "field_devices": [
                "sensors, actuators and motor drives",
                "pressure sensors, flow meters and valves",
                "temperature sensors and safety instrumentation",
            ],
            "controllers": [
                "PLCs (Programmable Logic Controllers)",
                "RTUs (Remote Terminal Units)",
                "DCS (Distributed Control System) controllers",
            ],
            "hmi_system": [
                "Wonderware",
                "Ignition",
                "Siemens WinCC",
                "Rockwell FactoryTalk",
            ],
            "attack_type": [
                "ransomware",
                "nation-state APT",
                "supply chain",
                "spear-phishing",
            ],
        },
        "frameworks": ["IEC 62443-3-3", "NIST SP 800-82", "Purdue Model"],
        "real_world_reference": "Similar architecture flaws contributed to the 2021 Oldsmar Water Treatment attack",
        "answers": """
MODEL ANSWERS - OT-ARCH-001 (Instructor Mode)

Q1. The Purdue Model divides OT networks into levels 0-5. Levels 0-2 are OT
    (field devices, controllers, supervisory). Level 3 is operations. Levels
    4-5 are enterprise IT. It is foundational because it defines where security
    boundaries must exist between OT and IT.

Q2. Three critical violations:
    - Direct Level 0-2 to Level 4-5 connectivity allows malware to move
      freely from IT into OT with no security boundary.
    - Internet browsing on Level 2 engineering workstations exposes OT
      systems to phishing and drive-by download attacks.
    - Vendor remote access direct to Level 1 controllers bypasses all
      security controls and monitoring.

Q3. Ransomware entering at Level 5 can traverse to Level 0 via the flat
    network, potentially manipulating physical processes. In an electricity
    generation plant this could cause turbine damage, power outages, or
    safety system failures with potential for physical harm.

Q4. Secure architecture recommendations:
    - Place a DMZ between Level 3 and Level 4 with data diodes for
      one-way data flow where possible.
    - Implement application-aware firewalls at each level boundary.
    - Use a jump server or PAM solution for all vendor remote access
      with session recording and time-limited access.

Q5. In OT environments least privilege is more critical because
    unauthorised commands to physical devices can cause equipment damage,
    process disruption, or safety incidents. Unlike IT where the worst
    case is data loss, OT failures can harm people and infrastructure.
""",
    },
    {
        "id": "OT-ARCH-002",
        "domain": "OT/ICS Architecture",
        "sub_topic": "Industrial Protocols and IT/OT Differences",
        "difficulty": "beginner",
        "objective": "Understand industrial protocols and how they differ from IT protocols",
        "scenario_template": """
You are reviewing network traffic captures from an OT environment at a
{industry}. Your SIEM has flagged unusual traffic patterns.

The network capture shows the following protocols in use:
  - {protocol_1} on port {port_1} between HMI and PLCs
  - {protocol_2} traffic between RTUs and the control centre
  - EtherNet/IP traffic on the production floor network
  - Standard TCP/IP traffic on the IT network

A security scan reveals:
  - {protocol_1} has NO authentication or encryption
  - {protocol_2} transmits commands in plaintext
  - PLCs respond to ANY device that sends correctly formatted commands
  - No protocol whitelisting is in place on network switches

Questions:
1. Explain why {protocol_1} and {protocol_2} were designed without
   authentication or encryption. What were the original design priorities
   of industrial protocols compared to IT protocols?

2. An attacker who gains network access sends crafted {protocol_1} commands
   directly to a PLC controlling {critical_process}. What could they do
   and what is the potential physical consequence?

3. Why is applying standard IT security controls like TLS encryption to
   OT protocols often problematic? Name at least THREE specific challenges.

4. What network-level compensating controls would you implement to protect
   these legacy protocols WITHOUT modifying the PLCs or protocols themselves?

5. Compare the security priorities of IT systems (CIA triad) with OT systems.
   Why is the order of priorities different and what does this mean for
   your security approach?
""",
        "variables": {
            "industry": [
                "power generation facility",
                "water treatment plant",
                "manufacturing facility",
                "oil refinery",
            ],
            "protocol_1": ["Modbus TCP", "DNP3", "Profibus", "OPC DA"],
            "port_1": ["502", "20000", "102", "135"],
            "protocol_2": ["DNP3", "IEC 60870-5-104", "Modbus RTU", "PROFINET"],
            "critical_process": [
                "chemical dosing in the water treatment process",
                "turbine speed control in power generation",
                "pressure regulation in the gas pipeline",
                "temperature control in the reactor vessel",
            ],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-4-2"],
        "real_world_reference": "Modbus and DNP3 lack authentication by design — this was exploited in multiple ICS attacks",
        "answers": """
MODEL ANSWERS - OT-ARCH-002 (Instructor Mode)

Q1. Industrial protocols like Modbus and DNP3 were designed in the 1970-80s
    for isolated networks where reliability and speed were priorities.
    Security was not considered because systems were air-gapped. IT protocols
    were designed for open networks and built security in from the start.

Q2. An attacker sending crafted Modbus commands could manipulate valve
    positions, pump speeds or pressure setpoints. In a gas pipeline this
    could cause overpressure, equipment damage, explosion risk or
    environmental damage from uncontrolled releases.

Q3. Three challenges applying TLS to OT protocols:
    - Legacy PLCs lack processing power for encryption overhead.
    - Real-time control systems cannot tolerate encryption latency.
    - Vendor support contracts may prohibit protocol modifications.

Q4. Compensating controls without modifying PLCs:
    - Deploy unidirectional security gateways (data diodes).
    - Implement OT-aware firewalls with Modbus deep packet inspection.
    - Use VLANs to isolate OT protocols from IT network segments.
    - Deploy protocol whitelisting on managed switches.

Q5. IT priorities are Confidentiality, Integrity, Availability (CIA).
    OT priorities are Safety, Availability, Integrity, Confidentiality (SAIC).
    Availability is critical in OT because downtime means production loss
    or safety incidents. Confidentiality is least important as OT data
    is operational not sensitive.
""",
    },
]

# ================================================================
# SECTION 2 - THREAT LANDSCAPE SCENARIOS
# ================================================================

THREAT_SCENARIOS = [
    {
        "id": "OT-THREAT-001",
        "domain": "OT/ICS Threat Landscape",
        "sub_topic": "Stuxnet and Nation-State ICS Attacks",
        "difficulty": "beginner",
        "objective": "Understand advanced nation-state threats targeting ICS",
        "scenario_template": """
You are presenting a threat briefing to the board of directors of a
{industry}. They have asked you to explain the threat landscape for
OT/ICS environments following a government advisory warning of
increased nation-state activity targeting critical infrastructure.

Background context for your briefing:
  - Your organisation operates {ot_assets} connected to a corporate network
  - You have {remote_access} remote access connections for vendor maintenance
  - Your OT systems run {os_version} operating systems
  - Your last OT-specific security assessment was {last_assessment} ago

Questions:
1. Explain the significance of Stuxnet as a watershed moment in OT/ICS
   security. What made it technically unprecedented and what did it prove
   about the vulnerability of industrial control systems?

2. Using the MITRE ATT&CK for ICS framework, describe the typical attack
   lifecycle of a nation-state actor targeting a {industry}.
   Map at least 5 specific tactics from Initial Access to Impact.

3. Your organisation has {os_version} systems that cannot be patched.
   A critical vulnerability has been published affecting this OS version.
   What compensating controls do you recommend to the board?

4. The government advisory mentions {threat_actor} as an active threat.
   What specific OT/ICS attack techniques is this group known to use
   and how would you detect them in your environment?

5. Write a 3-paragraph board-level summary of the OT threat landscape
   that is accurate but avoids technical jargon. Focus on business risk
   and consequence rather than technical detail.
""",
        "variables": {
            "industry": [
                "electricity transmission company",
                "water utility",
                "natural gas pipeline operator",
                "nuclear facility operator",
                "port and logistics operator",
            ],
            "ot_assets": [
                "47 PLCs and 12 SCADA servers",
                "200+ field devices and 8 HMI workstations",
                "15 RTUs across 6 remote sites",
            ],
            "remote_access": [
                "12 active vendor VPN",
                "8 third-party maintenance",
                "5 vendor jump server",
            ],
            "os_version": [
                "Windows XP embedded",
                "Windows Server 2008",
                "Windows 7 embedded",
            ],
            "last_assessment": ["3 years", "5 years", "never conducted a formal"],
            "threat_actor": [
                "Sandworm (Russia)",
                "Volt Typhoon (China)",
                "Lazarus Group (North Korea)",
                "XENOTIME (Russia)",
            ],
        },
        "frameworks": ["MITRE ATT&CK for ICS", "NIST SP 800-82"],
        "real_world_reference": "Stuxnet 2010, Ukraine power grid 2015/2016, Colonial Pipeline 2021",
        "answers": """
MODEL ANSWERS - OT-THREAT-001 (Instructor Mode)

Q1. Stuxnet was the first known cyberweapon designed to cause physical
    damage. It used four zero-day vulnerabilities, targeted Siemens PLCs
    specifically, and caused centrifuges to destroy themselves while
    reporting normal operation. It proved nation-states could use cyber
    tools to cause physical infrastructure damage.

Q2. MITRE ATT&CK for ICS attack lifecycle:
    - Initial Access T0817: Spear-phishing or supply chain compromise.
    - Execution T0807: Native API abuse on engineering workstations.
    - Persistence T0891: Hardcoded credentials in OT systems.
    - Lateral Movement T0812: Remote services to reach OT network.
    - Impact T0813: Denial of control or manipulation of setpoints.

Q3. Compensating controls for unpatched systems:
    - Network segmentation isolating vulnerable systems.
    - Application whitelisting preventing unauthorised code execution.
    - Enhanced monitoring for anomalous behaviour on legacy systems.
    - Physical security controls limiting physical access.

Q4. Response depends on the specific threat actor named. Generally
    nation-state actors use living-off-the-land techniques, target
    safety systems, and conduct lengthy reconnaissance before impact.
    Detection focuses on anomalous authentication, unusual OT protocol
    commands and unexpected network connections.

Q5. Board summary should explain that critical infrastructure faces
    nation-state cyber threats, consequences include physical damage
    and safety incidents, and investment in OT security is essential
    to protect operations, people and regulatory compliance.
""",
    },
    {
        "id": "OT-THREAT-002",
        "domain": "OT/ICS Threat Landscape",
        "sub_topic": "Ransomware in OT Environments",
        "difficulty": "beginner",
        "objective": "Understand ransomware impact and response in OT environments",
        "scenario_template": """
It is {time} on a {day}. You are the OT Security Manager at a {industry}.
Your IT team reports ransomware has been detected on the corporate network.

Current situation:
  - Ransomware variant: {ransomware_variant}
  - IT systems affected: {it_systems} confirmed encrypted
  - OT network status: Currently appears unaffected
  - IT/OT connection: A single firewall separates IT from OT networks
  - Production status: {production_status}
  - Your OT backups: {backup_status}

The ransomware group has a known capability to pivot from IT to OT networks.
A ransom note demands {ransom_amount} within 72 hours.

Questions:
1. What is your IMMEDIATE first decision regarding the OT network in the
   next 15 minutes? Justify your answer considering both security and
   operational safety requirements.

2. The Colonial Pipeline incident is often cited as a warning for OT
   operators. What actually caused Colonial Pipeline to shut down OT
   operations and what lesson does this hold for your situation?

3. Your production line is currently {production_status}. What are the
   safety implications of an emergency OT network shutdown versus
   allowing production to continue with potential ransomware risk?

4. The ransomware group threatens to release stolen data AND has
   indicated capability to manipulate {critical_system} if ransom
   is not paid. How does this double extortion change your response?

5. Develop a 5-step OT-specific ransomware response plan that addresses:
   - OT/IT isolation decision criteria
   - Safety system protection
   - Evidence preservation
   - Recovery prioritisation
   - Communication to regulators and public
""",
        "variables": {
            "time": ["02:30 Saturday", "Friday 17:45", "Monday 08:15"],
            "day": ["Saturday morning", "Friday afternoon", "Monday morning"],
            "industry": [
                "petroleum refinery",
                "water treatment utility",
                "food processing plant",
                "automotive manufacturer",
                "hospital with building management systems",
            ],
            "ransomware_variant": ["BlackCat/ALPHV", "LockBit 3.0", "Cl0p", "BlackBasta"],
            "it_systems": ["14 servers and 200 workstations", "all domain controllers", "the ERP and email systems"],
            "production_status": [
                "running at full capacity with hazardous chemicals in process",
                "mid-batch with product that cannot be safely paused",
                "in a planned shutdown window with systems in safe state",
            ],
            "backup_status": [
                "last OT backup was 6 months ago on a network share now encrypted",
                "immutable cloud backups from 48 hours ago",
                "offline tape backups from last week stored off-site",
            ],
            "ransom_amount": [".5 million", " million", ",000"],
            "critical_system": [
                "safety instrumented systems controlling pressure relief valves",
                "chemical dosing systems in the water treatment process",
                "temperature controls in the reactor",
            ],
        },
        "frameworks": ["NIST SP 800-82", "ICS-CERT advisories"],
        "real_world_reference": "Colonial Pipeline 2021, Norsk Hydro 2019, TRITON/TRISIS malware targeting Safety Instrumented Systems",
        "answers": """
MODEL ANSWERS - OT-THREAT-002 (Instructor Mode)

Q1. The immediate OT decision is to isolate OT from IT at the firewall
    boundary while keeping OT running if it is safe to do so.
    Shutting down OT prematurely can itself cause safety incidents
    if processes are in a state that requires controlled shutdown.

Q2. Colonial Pipeline did not shut down because OT was infected.
    They shut down OT proactively because their billing and IT systems
    were compromised making it impossible to safely manage pipeline
    operations. The lesson is that IT/OT dependencies can force OT
    shutdowns even when OT itself is unaffected.

Q3. If production is running with hazardous materials in process an
    emergency shutdown may be more dangerous than a controlled one.
    The safety team must assess whether the current process state
    can be safely held, paused or must continue to completion before
    any cybersecurity response affects physical operations.

Q4. Double extortion changes the response because even paying the
    ransom does not prevent data publication. It also raises the
    stakes considerably if threat actors can manipulate safety systems.
    The priority shifts to containment and safety system protection
    over recovery of encrypted systems.

Q5. OT ransomware response plan:
    1. Activate incident response team including OT engineers and safety.
    2. Assess OT network status and isolate from IT if safe to do so.
    3. Preserve forensic evidence before any remediation.
    4. Notify regulators within required timeframe.
    5. Begin recovery from immutable backups prioritising safety systems.
""",
    },
]

# ================================================================
# SECTION 3 - DEFENSIVE CONTROLS SCENARIOS
# ================================================================

DEFENSIVE_SCENARIOS = [
    {
        "id": "OT-DEF-001",
        "domain": "OT/ICS Defensive Controls",
        "sub_topic": "IEC 62443 Security Zones and Conduits",
        "difficulty": "beginner",
        "objective": "Apply IEC 62443 framework to design OT security zones",
        "scenario_template": """
You have been hired as an OT security consultant for a {industry}.
The organisation wants to achieve IEC 62443 compliance.

Current environment:
  - {num_sites} operational sites across {region}
  - Each site has: field devices, PLCs, SCADA servers, historian, and HMI
  - A central control room connects to all sites via {wan_connection}
  - {num_vendors} third-party vendors require remote access for maintenance
  - The organisation has no current security zones defined

You have been asked to design a zone and conduit model per IEC 62443-3-2.

Questions:
1. Explain the concept of Security Zones and Conduits in IEC 62443.
   How do they differ from traditional IT network segmentation concepts?

2. Define the Security Levels (SL 1-4) in IEC 62443.
   What Security Level would you recommend for each of the following
   and justify your answer:
   - Field device network (PLCs and sensors)
   - SCADA/HMI network
   - Historian server
   - Vendor remote access conduit

3. Design a zone and conduit diagram (describe in text) for one site
   of the {industry}. Include at least 4 zones and 3 conduits with
   security controls at each conduit boundary.

4. {num_vendors} vendors require remote access. Using IEC 62443 principles
   design a secure vendor access architecture. What controls must be in
   place before a vendor is permitted to connect?

5. The organisation asks: "What is the business case for IEC 62443
   compliance?" Write a one-paragraph justification addressing:
   regulatory requirements, insurance implications, and incident
   liability reduction.
""",
        "variables": {
            "industry": [
                "water utility with 8 pumping stations",
                "electricity distributor with substations",
                "gas pipeline operator",
                "chemical processing plant",
            ],
            "num_sites": ["8", "12", "4", "22"],
            "region": ["the North Island of New Zealand", "the UK", "Australia", "Southeast Asia"],
            "wan_connection": [
                "MPLS private WAN",
                "4G/LTE cellular links",
                "a mix of fibre and satellite",
            ],
            "num_vendors": ["6", "12", "4", "18"],
        },
        "frameworks": ["IEC 62443-3-2", "IEC 62443-3-3", "NIST SP 800-82"],
        "real_world_reference": "IEC 62443 is the primary international standard for OT/ICS security",
        "answers": """
MODEL ANSWERS - OT-DEF-001 (Instructor Mode)

Q1. Security Zones group assets with similar security requirements.
    Conduits are the communication paths between zones with defined
    security controls. Unlike IT VLANs, zones and conduits consider
    the safety and availability requirements of OT systems and
    define security levels based on consequence of compromise.

Q2. Security Levels:
    - Field device network: SL2 - targeted attacks possible.
    - SCADA/HMI network: SL2-3 - sophisticated attacks likely.
    - Historian server: SL2 - important but not safety critical.
    - Vendor remote access conduit: SL3 - high risk entry point
      requiring strong authentication and monitoring.

Q3. Zone design example: Field Device Zone contains PLCs and sensors.
    Control Zone contains HMIs and engineering workstations.
    Operations Zone contains historian and MES systems.
    DMZ Zone bridges OT and IT. Conduits between zones implement
    firewalls, protocol filtering and authentication controls.

Q4. Vendor access architecture: dedicated vendor DMZ with jump server.
    MFA required for all vendor connections. Session recording enabled.
    Access limited to approved systems only. Time-limited credentials.
    All vendor activities logged and reviewed post-session.

Q5. Business case for IEC 62443:
    Compliance reduces cyber insurance premiums and demonstrates due
    diligence to regulators. In the event of an incident non-compliance
    increases liability exposure. Many operators now require IEC 62443
    compliance from their suppliers and partners.
""",
    },
    {
        "id": "OT-DEF-002",
        "domain": "OT/ICS Defensive Controls",
        "sub_topic": "OT Asset Inventory and Vulnerability Management",
        "difficulty": "beginner",
        "objective": "Understand OT-specific vulnerability management challenges",
        "scenario_template": """
You are the OT security lead at a {industry}. A new CISO has joined
from an IT background and wants to implement the same vulnerability
management programme used for IT systems across the OT environment.

The proposed IT-style programme includes:
  - Weekly authenticated vulnerability scans of all OT assets
  - 30-day SLA for critical patch deployment
  - Automated patch deployment via SCCM
  - Quarterly penetration testing of all systems

Your OT environment includes:
  - {num_assets} OT assets across the facility
  - {legacy_systems} running end-of-life operating systems
  - PLCs with firmware last updated {last_update}
  - {safety_systems} safety instrumented systems (SIS)
  - Several systems with vendor support contracts prohibiting unauthorised changes

Questions:
1. Explain to the CISO why active vulnerability scanning of OT networks
   is potentially DANGEROUS. What specific risks does scanning introduce
   in an OT environment that do not exist in IT?

2. The CISO insists on a 30-day critical patch SLA. Why is this
   unrealistic for OT environments? What is a more appropriate
   patching approach and timeline for OT systems?

3. {legacy_systems} cannot be patched as the vendor no longer provides
   updates. Using the NIST SP 800-82 framework, describe the compensating
   controls you would implement and the formal risk acceptance process required.

4. The {safety_systems} safety instrumented systems are in scope.
   Why do SIS systems require a completely separate security and
   change management approach? What could go wrong if standard IT
   patching processes are applied?

5. Design an OT-appropriate vulnerability management programme that
   satisfies the CISO's security objectives while respecting OT
   operational constraints. Include: discovery methods, prioritisation
   criteria, patching approach, and exception handling.
""",
        "variables": {
            "industry": [
                "petroleum refinery",
                "electricity generation plant",
                "water treatment utility",
                "pharmaceutical manufacturer",
            ],
            "num_assets": ["340", "127", "89", "520"],
            "legacy_systems": [
                "47 Windows XP embedded systems",
                "12 Windows Server 2003 historians",
                "23 unsupported embedded Linux devices",
            ],
            "last_update": ["4 years ago", "7 years ago", "never since installation"],
            "safety_systems": ["4 critical", "8", "2 high-integrity"],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-2-3", "CISA advisories"],
        "real_world_reference": "The TRITON/TRISIS attack specifically targeted Safety Instrumented Systems in 2017",
        "answers": """
MODEL ANSWERS - OT-DEF-002 (Instructor Mode)

Q1. Active scanning sends network packets that OT devices must respond
    to. Legacy PLCs and RTUs may crash, freeze or behave unexpectedly
    when receiving unexpected network traffic. A crashed PLC during
    production can cause safety incidents and unplanned downtime.

Q2. A 30-day SLA is unrealistic for OT because patches must be tested
    in a replica environment, vendor approval may be required, and
    maintenance windows in OT are typically quarterly or annual.
    A risk-based approach with compensating controls during extended
    patching cycles is more appropriate.

Q3. For unsupported legacy systems the risk acceptance process requires:
    formal risk assessment documenting the vulnerability and likelihood,
    compensating controls implemented and documented, sign-off by the
    CISO and operations manager, regular review of the accepted risk,
    and a remediation roadmap even if timelines are long.

Q4. Four validation methods after patching:
    - Re-scan to confirm vulnerability is no longer detected.
    - Functional testing to confirm OT system operates correctly.
    - Vendor confirmation that patch was successfully applied.
    - Log review confirming no errors during patch process.

Q5. Exception management for failed patches:
    Track in a risk register with asset owner, date identified,
    reason for failure and compensating controls in place.
    Review exceptions monthly and escalate unresolved exceptions
    to management after 90 days.
""",
    },
]

# ================================================================
# SECTION 4 - INCIDENT RESPONSE SCENARIOS
# ================================================================

INCIDENT_RESPONSE_SCENARIOS = [
    {
        "id": "OT-IR-001",
        "domain": "OT/ICS Incident Response",
        "sub_topic": "OT Incident Detection and Response",
        "difficulty": "beginner",
        "objective": "Apply OT-specific incident response procedures",
        "scenario_template": """
You are the OT Security Manager at a {industry}. Your OT monitoring
system has generated the following alerts over the past 2 hours:

Alert 1 [{time_1}]:
  Unusual Modbus TCP traffic from Engineering Workstation EWS-{ews_id}
  to PLC-{plc_id} — 847 read requests in 60 seconds (normal: 2-3/minute)

Alert 2 [{time_2}]:
  New device {unknown_ip} appeared on the OT network
  MAC address does not match any authorised asset inventory entry

Alert 3 [{time_3}]:
  PLC-{plc_id} ladder logic program modified
  Change not associated with any approved change request
  Modified by: EWS-{ews_id}

Alert 4 [{time_4}]:
  {safety_system} safety setpoint for {critical_parameter} changed
  New value: {new_value} (normal operating range: {normal_range})
  Authorisation: NONE recorded in change management system

Production is currently running at full capacity.
Physical safety implications of the setpoint change: {safety_implication}

Questions:
1. Triage these four alerts in priority order. Which represents the most
   immediate physical safety risk and why?

2. Alert 4 shows an unauthorised safety setpoint change. What is your
   IMMEDIATE response in the next 5 minutes? Consider both cybersecurity
   and physical safety in your answer.

3. The unknown device {unknown_ip} appeared after Alert 1.
   What does this sequence of events suggest about the attack chain?
   Map it to MITRE ATT&CK for ICS tactics.

4. You must decide whether to shut down production to investigate.
   List the factors you must consider and who must be involved in
   this decision. Why is this decision more complex than an equivalent
   IT incident?

5. Write your initial incident notification to:
   a) Plant operations manager (safety focus)
   b) CISO (security focus)
   c) Regulatory authority (compliance focus)
   Each should be 3-4 sentences appropriate for that audience.
""",
        "variables": {
            "industry": [
                "chemical processing plant",
                "water treatment facility",
                "electricity generation plant",
                "oil refinery",
            ],
            "time_1": ["14:22:04", "02:11:33", "09:44:17"],
            "time_2": ["14:23:11", "02:12:08", "09:45:02"],
            "time_3": ["14:31:44", "02:19:55", "09:52:38"],
            "time_4": ["14:33:02", "02:21:11", "09:54:14"],
            "ews_id": ["03", "07", "12"],
            "plc_id": ["14", "07", "22"],
            "unknown_ip": ["10.10.OT.247", "192.168.100.199", "172.16.50.88"],
            "safety_system": ["high-pressure", "temperature", "chemical dosing"],
            "critical_parameter": ["reactor pressure relief", "boiler temperature limit", "chlorine dosing rate"],
            "new_value": ["340 PSI (was 280 PSI)", "485°C (was 420°C)", "12 mg/L (was 4 mg/L)"],
            "normal_range": ["200-280 PSI", "350-420°C", "1-4 mg/L"],
            "safety_implication": [
                "pressure exceeding relief valve rating risks catastrophic vessel failure",
                "temperature exceeding design limits risks equipment damage and fire",
                "chlorine overdose at this level is toxic to humans at point of use",
            ],
        },
        "frameworks": ["MITRE ATT&CK for ICS", "NIST SP 800-82", "ICS-CERT"],
        "real_world_reference": "TRITON/TRISIS malware targeted safety instrumented systems in a Middle East petrochemical facility 2017",
        "answers": """
MODEL ANSWERS - OT-IR-001 (Instructor Mode)

Q1. Alert priority order: Alert 4 (safety setpoint change) is most
    critical as it represents immediate physical safety risk.
    Alert 3 (PLC logic modification) is second. Alert 1 (reconnaissance
    scanning) is third. Alert 2 (unknown device) is fourth but
    likely related to the other alerts.

Q2. Immediate response to safety setpoint change:
    Notify operations and safety team immediately. Do not change the
    setpoint back without engineering authorisation as the process
    may have adapted. Verify physical safety status at the affected
    equipment. Initiate emergency change process to restore correct
    setpoint through approved channels.

Q3. The sequence suggests reconnaissance (Alert 1), attacker device
    introduction (Alert 2), PLC program modification (Alert 3),
    safety system manipulation (Alert 4). This maps to MITRE ATT&CK
    for ICS: Discovery, Lateral Movement, Modify Control Logic,
    and Manipulation of Control.

Q4. The production shutdown decision requires operations manager,
    safety officer, and CISO involvement. Factors include:
    current process safety state, risk of continuing versus stopping,
    regulatory requirements for safety system integrity, and
    whether the attack is still active or has been contained.

Q5. Three notifications:
    Operations: focus on safety status, what systems are affected,
    and operational impact. CISO: focus on attack vector, scope of
    compromise, and containment status. Regulator: focus on incident
    timeline, safety systems affected, and actions taken.
""",
    },
]

# ================================================================
# COMBINED POOL
# ================================================================

ALL_OT_SCENARIOS = (
    ARCHITECTURE_SCENARIOS +
    THREAT_SCENARIOS +
    DEFENSIVE_SCENARIOS +
    INCIDENT_RESPONSE_SCENARIOS
)

OT_DOMAIN_MAP = {
    "architecture":        ARCHITECTURE_SCENARIOS,
    "threats":             THREAT_SCENARIOS,
    "defensive":           DEFENSIVE_SCENARIOS,
    "incident_response":   INCIDENT_RESPONSE_SCENARIOS,
}

# ================================================================
# GENERATOR
# ================================================================

def generate_ot_scenario(domain_filter=None, difficulty_filter=None):
    if domain_filter and domain_filter in OT_DOMAIN_MAP:
        pool = OT_DOMAIN_MAP[domain_filter]
    else:
        pool = ALL_OT_SCENARIOS

    if difficulty_filter:
        filtered = [s for s in pool if s["difficulty"] == difficulty_filter]
        if filtered:
            pool = filtered
        # else fall back to full domain pool

    template = random.choice(pool)
    scenario_text = template["scenario_template"]

    for var_name, options in template.get("variables", {}).items():
        chosen = random.choice(options)
        scenario_text = scenario_text.replace("{" + var_name + "}", chosen)

    return {
        "module":      "OT/ICS Security",
        "id":          template["id"],
        "domain":      template["domain"],
        "sub_topic":   template["sub_topic"],
        "objective":   template["objective"],
        "difficulty":  template["difficulty"],
        "frameworks":  ", ".join(template.get("frameworks", [])),
        "real_world":  template.get("real_world_reference", ""),
        "scenario":    scenario_text.strip(),
        "answers":     template.get("answers", ""),
    }


def get_random_ot_scenario():
    return generate_ot_scenario()


def display_ot_scenario(s: dict, student_mode: bool = True):
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  GIDEON - OT/ICS Security Module")
    print(f"  ID         : {s.get('id', 'N/A')}")
    print(f"  Domain     : {s.get('domain', 'N/A')}")
    print(f"  Sub-topic  : {s.get('sub_topic', 'N/A')}")
    print(f"  Objective  : {s.get('objective', 'N/A')}")
    print(f"  Difficulty : {s.get('difficulty', 'N/A').upper()}")
    print(f"  Frameworks : {s.get('frameworks', 'N/A')}")
    print(f"  Real World : {s.get('real_world', 'N/A')}")
    mode_label = "STUDENT MODE" if student_mode else "INSTRUCTOR MODE"
    print(f"  Mode       : {mode_label}")
    print(sep)
    print(s.get("scenario", "No scenario generated."))
    if not student_mode and s.get("answers"):
        print(f"\n{sep}")
        print(s.get("answers", ""))
    print(f"\n{sep}\n")




# ================================================================
# ADDITIONAL ARCHITECTURE SCENARIOS
# ================================================================

ARCHITECTURE_SCENARIOS += [
    {
        "id": "OT-ARCH-003",
        "domain": "OT/ICS Architecture",
        "sub_topic": "IT/OT Convergence Risks",
        "difficulty": "beginner",
        "objective": "Understand the security risks of IT/OT convergence",
        "scenario_template": """
You are a cybersecurity consultant engaged by a {industry} to assess
the risks of their planned IT/OT convergence project.

The project plan includes:
  - Connecting OT historian servers directly to the corporate cloud
  - Deploying Microsoft 365 on engineering workstations at Level 2
  - Implementing remote monitoring via a commercial IoT platform
  - Using standard IT patch management tools across OT systems
  - Sharing Active Directory authentication between IT and OT

Business justification: Real-time production data in the cloud will
save {cost_saving} annually in operational efficiency.

Questions:
1. Explain the concept of IT/OT convergence. What business benefits
   drive organisations to converge their IT and OT networks?

2. Identify FIVE specific security risks introduced by this convergence
   plan. For each risk explain the potential operational consequence.

3. The plan includes sharing Active Directory between IT and OT.
   Why is this particularly dangerous? What happened in the
   {real_incident} incident that illustrates this risk?

4. How would you redesign this convergence project to achieve the
   business benefits while maintaining OT security? What architecture
   pattern would you recommend?

5. The business is focused on the {cost_saving} annual saving.
   What is the potential financial cost of a successful OT cyberattack
   that disrupts production for 2 weeks? Build your business case
   for secure convergence.
""",
        "variables": {
            "industry": [
                "water utility",
                "electricity distributor",
                "manufacturing company",
                "mining operation",
            ],
            "cost_saving": [".4 million", ",000", ".1 million", ".2 million"],
            "real_incident": [
                "Colonial Pipeline 2021",
                "Norsk Hydro 2019",
                "Oldsmar Water Treatment 2021",
            ],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-2-1"],
        "real_world_reference": "IT/OT convergence is the primary driver of increased OT attack surface",
        "answers": """
MODEL ANSWERS - OT-ARCH-003 (Instructor Mode)

Q1. IT/OT convergence connects operational technology networks to IT
    systems and the internet for efficiency and data analytics.
    Business benefits include predictive maintenance, real-time production
    visibility, reduced operational costs and remote management capability.

Q2. Five security risks:
    - Cloud historian connection creates internet-facing OT data path.
    - Microsoft 365 on Level 2 workstations introduces phishing risk.
    - IoT platform creates additional attack surface into OT network.
    - IT patch management tools can disrupt OT systems not designed
      for automated updates.
    - Shared Active Directory means IT credential compromise gives
      OT network access.

Q3. Shared Active Directory is dangerous because a compromised IT
    account gains OT access. Colonial Pipeline attackers used a
    compromised VPN account to access both IT and OT networks leading
    to the shutdown of fuel supply to the US East Coast.

Q4. Recommended architecture uses a secure DMZ with data historian
    in a demilitarised zone. OT data flows one-way to the historian.
    IT systems read from the historian but cannot write back to OT.
    A separate OT Active Directory with no trust relationship to IT AD.

Q5. A 2-week OT production outage costs: lost production revenue,
    emergency response costs, regulatory fines, reputation damage
    and potential liability. For most industrial operators this
    exceeds the annual saving making the security investment essential.
""",
    },
    {
        "id": "OT-ARCH-004",
        "domain": "OT/ICS Architecture",
        "sub_topic": "SCADA and HMI Security",
        "difficulty": "beginner",
        "objective": "Understand SCADA and HMI architecture and security requirements",
        "scenario_template": """
You are reviewing the SCADA system at a {industry}. The system
provides operators with visibility and control of all physical processes.

Current SCADA architecture:
  - HMI workstations: {num_hmi} running {os_version}
  - SCADA server: single server, no redundancy
  - Historian: stores {years} years of process data
  - Remote access: operators can access HMI via {remote_method}
  - Authentication: shared username/password, no MFA
  - Last security review: {last_review}

Recent incidents reported by operators:
  - HMI screens occasionally show unexpected values
  - One workstation rebooted unexpectedly during a shift
  - A vendor remotely connected and made changes without prior notice

Questions:
1. What is the difference between SCADA, DCS, HMI, and Historian?
   Explain each component and its role in the OT architecture.

2. The three operator-reported incidents could indicate a cyberattack
   in progress. For each incident explain what malicious activity
   it might represent and how you would investigate.

3. Shared credentials with no MFA on SCADA systems is a critical
   vulnerability. Why is implementing MFA on OT systems more
   complex than on IT systems? What solutions exist?

4. The SCADA server has no redundancy. Beyond cybersecurity what
   does this represent and how does redundancy also improve
   security resilience?

5. Design a secure remote access solution for operators that
   maintains operational capability while eliminating the current
   security risks. Include authentication, session monitoring,
   and access controls.
""",
        "variables": {
            "industry": [
                "water treatment facility",
                "electricity substation operator",
                "gas distribution network",
                "oil pipeline operator",
            ],
            "num_hmi": ["4", "8", "12", "3"],
            "os_version": ["Windows 7", "Windows 10", "Windows Server 2012"],
            "years": ["7", "12", "4", "15"],
            "remote_method": [
                "RDP directly over the internet",
                "a commercial remote desktop tool",
                "VPN with shared credentials",
            ],
            "last_review": ["never", "5 years ago", "3 years ago"],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-3-3"],
        "real_world_reference": "Shared HMI credentials were a factor in the 2021 Oldsmar Florida water treatment attack",
        "answers": """
MODEL ANSWERS - OT-ARCH-004 (Instructor Mode)

Q1. SCADA monitors and controls distributed processes remotely.
    DCS manages complex continuous processes at one site.
    HMI is the operator interface showing process graphics and controls.
    Historian stores time-series process data for analysis and reporting.

Q2. Three incident investigations:
    - Unexpected HMI values: could indicate unauthorised PLC program
      changes or network man-in-the-middle attack on OT traffic.
    - Unexpected reboot: could indicate malware infection, remote
      access misuse or ransomware beginning encryption process.
    - Unauthorised vendor connection: could indicate compromised vendor
      credentials or supply chain attack via vendor remote access.

Q3. MFA on OT systems is complex because legacy HMI software may not
    support modern authentication. Solutions include hardware tokens,
    smart cards, or PAM solutions that add MFA at the jump server
    level without modifying the HMI application itself.

Q4. SCADA redundancy improves security resilience by eliminating single
    points of failure that attackers can target. A redundant system
    allows failover during an incident and supports patching one node
    while the other remains operational.

Q5. Secure remote access design: dedicated jump server in OT DMZ with
    MFA required for all connections. Session recording for all remote
    sessions. Time-limited access with automatic disconnection.
    Vendor access approved per change request with defined scope.
""",
    },
]

# ================================================================
# ADDITIONAL THREAT SCENARIOS - BEGINNER FRIENDLY
# ================================================================

THREAT_SCENARIOS += [
    {
        "id": "OT-THREAT-003",
        "domain": "OT/ICS Threat Landscape",
        "sub_topic": "Introduction to OT Threats for IT Professionals",
        "difficulty": "beginner",
        "objective": "Understand the OT threat landscape from an IT professional perspective",
        "scenario_template": """
You are an IT security professional who has just been assigned
responsibility for OT security at a {industry}. Your first task
is to brief the operations team on the current threat landscape.

Key facts for your briefing:
  - Your facility operates {critical_function}
  - A successful cyberattack could affect {impact_area}
  - Your OT systems have been in operation for {system_age} years
  - The facility has never experienced a confirmed OT cyberattack
  - IT security controls are mature but OT security is immature

Questions:
1. Explain to a non-technical operations audience why OT systems
   that have worked safely for {system_age} years are now at increased
   cyber risk. What has changed in the threat environment?

2. What are the THREE most likely threat actor types targeting
   a {industry} and what are their motivations for each?

3. Explain the difference between a cyberattack impact in IT versus OT.
   Why is an OT attack on {critical_function} potentially more serious
   than a ransomware attack on the corporate IT network?

4. Your operations team says: "We are not connected to the internet
   so we cannot be attacked." How do you respond to this air gap myth?
   Provide at least THREE ways attackers can reach air-gapped OT systems.

5. What are the FIRST THREE OT security improvements you would
   recommend to management that would have the highest impact
   for the lowest cost and operational disruption?
""",
        "variables": {
            "industry": ["water treatment facility"],
            "critical_function": ["water treatment for 200,000 residents"],
            "impact_area": ["public health and safety"],
            "system_age": ["15", "20", "8", "25"],
        },
        "variable_sets": [
            {"industry": "water treatment facility", "critical_function": "water treatment for 200,000 residents", "impact_area": "public health and safety"},
            {"industry": "electricity generation plant", "critical_function": "electricity generation for 50,000 homes", "impact_area": "regional electricity supply"},
            {"industry": "food processing facility", "critical_function": "food production for major supermarket chains", "impact_area": "national food supply chain"},
            {"industry": "hospital with building management systems", "critical_function": "HVAC and medical gas systems for 500 patients", "impact_area": "patient safety"},
        ],
        "frameworks": ["NIST SP 800-82", "CISA advisories"],
        "real_world_reference": "Stuxnet proved air-gapped systems can be compromised. Oldsmar showed remote access risks.",
        "answers": """
MODEL ANSWERS - OT-THREAT-003 (Instructor Mode)

Q1. OT systems built years ago operated in isolation with no internet
    connectivity. IT/OT convergence, remote access requirements and
    supply chain complexity have connected these systems to the internet
    creating attack paths that did not previously exist.

Q2. Three threat actor types targeting critical infrastructure:
    - Nation-states seeking geopolitical leverage or pre-positioning.
    - Ransomware groups motivated by financial extortion.
    - Hacktivists motivated by political or environmental causes.

Q3. An OT attack on critical infrastructure can cause physical damage,
    safety incidents, environmental harm and loss of essential services
    to the public. IT ransomware causes data loss and operational
    disruption which is recoverable. OT attacks can harm people.

Q4. The air gap myth is false. Attackers reach air-gapped systems via:
    - Infected USB drives introduced by employees or vendors.
    - Compromised vendor laptops connected during maintenance.
    - Supply chain attacks on software or hardware components.

Q5. Three highest impact low disruption improvements:
    - Asset inventory to know what OT devices exist.
    - Network segmentation separating OT from IT networks.
    - Vendor remote access controls with MFA and session recording.
""",
    },
    {
        "id": "OT-THREAT-004",
        "domain": "OT/ICS Threat Landscape",
        "sub_topic": "Supply Chain Attacks on OT",
        "difficulty": "beginner",
        "objective": "Understand supply chain attack vectors targeting OT environments",
        "scenario_template": """
You are the OT security manager at a {industry}. A government advisory
has warned that threat actors are targeting OT vendors and using
compromised vendor software and remote access to attack end users.

Your vendor landscape includes:
  - {num_vendors} active vendor remote access connections
  - {scada_vendor} SCADA software updated {last_update}
  - {plc_vendor} PLCs with firmware updated by vendor technicians
  - Third party managed security service with network access
  - Cloud-based historian from a SaaS vendor

Questions:
1. Explain what a supply chain attack is in the context of OT security.
   How does the SolarWinds attack serve as a warning for OT operators
   even though it primarily targeted IT systems?

2. A vendor technician requests remote access to update firmware on
   your {plc_vendor} PLCs. What security controls and verification
   steps should be in place BEFORE granting access?

3. Your {scada_vendor} SCADA vendor releases an urgent security patch.
   What is your process for evaluating and deploying this patch
   in an OT environment? Why can you not simply deploy it immediately?

4. List FIVE specific controls to reduce supply chain risk across
   your vendor landscape. For each control explain what risk it mitigates.

5. How would you detect a compromised vendor remote access session
   that is performing malicious actions while appearing legitimate?
   What monitoring controls would you implement?
""",
        "variables": {
            "industry": [
                "water utility",
                "electricity generator",
                "manufacturing facility",
                "oil and gas operator",
            ],
            "num_vendors": ["8", "14", "6", "22"],
            "scada_vendor": ["Wonderware", "Ignition", "Siemens WinCC", "Rockwell FactoryTalk"],
            "last_update": ["6 months ago", "2 years ago", "last week"],
            "plc_vendor": ["Siemens S7", "Allen-Bradley", "Schneider Electric Modicon"],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-2-1", "CISA supply chain guidance"],
        "real_world_reference": "SolarWinds 2020 demonstrated supply chain attack scale. Multiple ICS vendors have been compromised.",
        "answers": """
MODEL ANSWERS - OT-THREAT-004 (Instructor Mode)

Q1. A supply chain attack compromises a vendor or software provider
    to use their trusted access as an entry point. SolarWinds showed
    that trusted software updates can deliver malware at scale.
    OT operators trust vendor remote access and software updates
    creating identical risks to those exploited in SolarWinds.

Q2. Before granting vendor remote access:
    - Verify identity using MFA and approved credentials.
    - Confirm a valid change request exists for the work.
    - Restrict access to only the specific systems required.
    - Enable session recording for the entire connection.
    - Set automatic time limit on the access window.

Q3. OT patch evaluation process:
    - Obtain patch from vendor through verified secure channel.
    - Test in a non-production environment that mirrors production.
    - Review vendor release notes for OT compatibility issues.
    - Schedule during planned maintenance window.
    - Have rollback plan ready before deploying.

Q4. Five supply chain controls:
    - Vendor risk assessments before granting any network access.
    - Just-in-time access provisioning for vendor connections.
    - Software integrity verification using cryptographic hashing.
    - Network monitoring for anomalous vendor session behaviour.
    - Contractual security requirements for all OT vendors.

Q5. Detection of compromised vendor sessions requires behavioural
    baselines. Alerts should fire on access outside approved windows,
    commands outside the approved scope, connections to unexpected
    systems and data volumes exceeding normal maintenance activity.
""",
    },
]

# ================================================================
# ADDITIONAL DEFENSIVE SCENARIOS
# ================================================================

DEFENSIVE_SCENARIOS += [
    {
        "id": "OT-DEF-003",
        "domain": "OT/ICS Defensive Controls",
        "sub_topic": "OT Network Monitoring and Anomaly Detection",
        "difficulty": "beginner",
        "objective": "Understand passive monitoring approaches for OT networks",
        "scenario_template": """
You are implementing a security monitoring programme for a {industry}.
The operations team is resistant to any active scanning or agents
on OT systems due to availability concerns.

Current monitoring state:
  - No OT-specific monitoring tools deployed
  - IT SIEM receives no OT data
  - No asset inventory of OT devices exists
  - Network switches have no logging enabled
  - The last {months} months of activity are completely unaudited

You have been given budget to deploy ONE monitoring solution.

Questions:
1. Why is passive monitoring preferred over active scanning in OT
   environments? Explain the specific risks that active scanning
   introduces to PLCs, RTUs, and other OT devices.

2. Compare these OT monitoring approaches and recommend one for
   this environment:
   a) Passive network TAP with OT-aware deep packet inspection
   b) Span port mirroring to an OT SIEM
   c) Agent-based endpoint monitoring on HMI workstations
   d) Firewall log analysis only

3. OT-aware monitoring tools like Claroty, Dragos, or Nozomi Networks
   can passively identify assets and protocols. What specific
   indicators of compromise would you configure alerts for
   in a {industry}?

4. Your monitoring tool detects a new unauthorised device on the
   OT network communicating with a PLC using Modbus TCP.
   Walk through your investigation and response steps.

5. How would you present the value of OT monitoring to a CFO
   who sees it as unnecessary cost? Build a business case using
   industry incident data and insurance implications.
""",
        "variables": {
            "industry": [
                "water treatment utility",
                "electricity distributor",
                "manufacturing facility",
                "oil pipeline operator",
            ],
            "months": ["6", "12", "18", "36"],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-3-3", "CISA"],
        "real_world_reference": "Passive monitoring tools like Dragos and Claroty are designed specifically for OT environments",
        "answers": """
MODEL ANSWERS - OT-DEF-003 (Instructor Mode)

Q1. Passive monitoring only listens to network traffic without sending
    any packets. Active scanning sends probes that OT devices must
    respond to. Legacy OT devices can crash or malfunction when
    receiving unexpected network traffic making passive monitoring
    essential in production OT environments.

Q2. Recommended approach is passive network TAP with OT-aware deep
    packet inspection. This provides full visibility without risk to
    OT devices, understands industrial protocols like Modbus and DNP3,
    and can identify assets passively without any active scanning.

Q3. OT monitoring alerts for this environment should include:
    new device appearing on OT network, unexpected protocol commands,
    communication between devices that do not normally communicate,
    engineering workstation connecting to field devices outside
    maintenance windows, and large data transfers from OT systems.

Q4. When an unauthorised device is detected: identify the device using
    passive fingerprinting, check physical access logs for the area,
    isolate the network segment if the device is unknown,
    capture traffic from the device for analysis, and escalate to
    incident response if malicious activity is confirmed.

Q5. Business case for OT monitoring:
    The average cost of an OT security incident is significantly higher
    than the cost of monitoring tools. Cyber insurance increasingly
    requires OT monitoring as a condition of coverage. Regulators in
    critical infrastructure sectors are mandating OT visibility.
""",
    },
]

# ================================================================
# ADDITIONAL INCIDENT RESPONSE SCENARIOS
# ================================================================

INCIDENT_RESPONSE_SCENARIOS += [
    {
        "id": "OT-IR-002",
        "domain": "OT/ICS Incident Response",
        "sub_topic": "OT Incident Response Planning",
        "difficulty": "beginner",
        "objective": "Understand OT-specific incident response planning requirements",
        "scenario_template": """
You have been asked to develop an OT Incident Response Plan for a
{industry}. The organisation currently has an IT incident response
plan but no OT-specific procedures.

Organisational context:
  - {num_staff} operational staff across {num_shifts} shifts
  - IT security team has no OT knowledge
  - OT engineers have no cybersecurity training
  - {regulator} is the primary regulatory body
  - No OT incident has ever been formally declared

Questions:
1. Explain THREE key differences between IT and OT incident response
   that must be reflected in your OT IR plan. Why can you not simply
   apply your existing IT IR plan to OT incidents?

2. An OT incident often requires a decision between CYBERSECURITY
   response (isolate and investigate) and OPERATIONAL SAFETY response
   (keep running to maintain safety). How does your IR plan address
   this conflict? Who has authority to make this call?

3. Your OT engineers understand the process but not cybersecurity.
   Your IT security team understands cybersecurity but not the process.
   How do you structure your OT IR team to bridge this gap?

4. {regulator} requires notification of significant cyber incidents
   within {notification_time}. What constitutes a notifiable OT
   incident and what information must be included in the notification?

5. Design a one-page OT Incident Response Checklist that operational
   staff can follow in the first 30 minutes of a suspected OT
   cyber incident. Use plain language suitable for non-security staff.
""",
        "variables": {
            "industry": [
                "water utility",
                "electricity network operator",
                "gas pipeline company",
                "food manufacturer",
            ],
            "num_staff": ["45", "120", "28", "200"],
            "num_shifts": ["3", "2", "4"],
            "regulator": [
                "the New Zealand GCSB and NCSC",
                "CISA in the United States",
                "the UK NCSC",
                "the Australian ASD",
            ],
            "notification_time": ["72 hours", "24 hours", "immediately"],
        },
        "frameworks": ["NIST SP 800-82", "IEC 62443-2-1", "CISA ICS-CERT"],
        "real_world_reference": "Most OT operators have no OT-specific IR plan — a critical gap exposed by Colonial Pipeline",
        "answers": """
MODEL ANSWERS - OT-IR-002 (Instructor Mode)

Q1. Three IT vs OT IR differences:
    - OT IR must consider physical safety before cybersecurity response.
    - OT systems cannot be simply shut down without safety assessment.
    - OT forensics requires specialised tools that do not disrupt
      production and OT engineers must be part of the response team.

Q2. The conflict is resolved by establishing clear decision authority.
    The safety officer has veto over any cybersecurity action that
    creates safety risk. A pre-defined decision matrix should specify
    when OT can be isolated versus when safety requires it to continue
    operating despite cyber risk.

Q3. Effective OT IR team bridges the gap by pairing OT engineers who
    understand the process with IT security analysts who understand
    the attack. A joint command structure with both disciplines
    represented at the decision-making level is essential.

Q4. Notifiable incidents typically include confirmed compromise of
    OT systems, safety system manipulation, or significant operational
    impact. Notification must include incident timeline, systems
    affected, actions taken and potential impact on services.

Q5. First 30 minutes checklist for non-security staff:
    1. Do not touch or reboot any affected systems.
    2. Call the security team and operations manager immediately.
    3. Note exactly what you observed and when.
    4. Preserve any unusual printouts or screen displays.
    5. Restrict access to the affected area.
    6. Do not discuss the incident on email or phone.
""",
    },
]

# Rebuild combined pool after additions
ALL_OT_SCENARIOS.clear()
ALL_OT_SCENARIOS.extend(
    ARCHITECTURE_SCENARIOS +
    THREAT_SCENARIOS +
    DEFENSIVE_SCENARIOS +
    INCIDENT_RESPONSE_SCENARIOS
)


# ================================================================
# SECTION 5 - AI AND AGENTIC AI THREAT SCENARIOS
# ================================================================

AI_THREAT_SCENARIOS = [
    {
        "id": "OT-AI-001",
        "domain": "AI and Agentic AI Threats",
        "sub_topic": "Agentic AI as an OT Attack Tool",
        "difficulty": "beginner",
        "objective": "Understand how agentic AI changes the OT threat landscape",
        "scenario_template": """
You are the OT Security Manager at a {industry}. A threat intelligence
briefing warns that a nation-state group is using agentic AI tools
to conduct autonomous reconnaissance and attacks against critical
infrastructure OT environments.

The briefing states the agentic AI can:
  - Autonomously map OT networks and identify device types
  - Learn industrial protocols by analysing captured traffic
  - Identify high-consequence targets within OT environments
  - Execute targeted attacks without human direction
  - Adapt its tactics based on defensive responses

Your environment includes:
  - {num_assets} OT assets across {num_sites} sites
  - {legacy_systems} running end-of-life operating systems
  - IT/OT connectivity via a {connection_type}
  - OT monitoring: {monitoring_status}

Questions:
1. Explain how agentic AI differs from traditional malware in its
   approach to attacking OT environments. What makes it particularly
   dangerous against legacy industrial control systems?

2. Your environment has {legacy_systems} running end-of-life systems.
   Why does this significantly increase your vulnerability to
   agentic AI attacks compared to modern systems?

3. The agentic AI can learn industrial protocols from captured traffic.
   What specific OT protocols in your environment could it learn and
   what malicious actions could it take once it understands them?

4. What defensive controls would you implement immediately to reduce
   the risk of agentic AI lateral movement through your OT network?
   Focus on controls that work regardless of the AI sophistication level.

5. Your board asks: "Can we detect an agentic AI attacker in our
   OT network?" What is your honest answer and what detection
   capabilities would you need to improve detection probability?
""",
        "variables": {
            "industry": [
                "electricity generation company",
                "water treatment utility",
                "oil and gas pipeline operator",
                "pharmaceutical manufacturer",
            ],
            "num_assets": ["340", "127", "520", "89"],
            "num_sites": ["8", "4", "12", "2"],
            "legacy_systems": [
                "47 Windows XP embedded systems",
                "12 Windows Server 2008 historians",
                "23 unsupported embedded Linux devices",
            ],
            "connection_type": [
                "historian server in a DMZ",
                "direct firewall with multiple permitted rules",
                "vendor remote access VPN",
            ],
            "monitoring_status": [
                "no OT-specific monitoring deployed",
                "basic firewall logging only",
                "passive monitoring on one site only",
            ],
        },
        "frameworks": ["MITRE ATT&CK for ICS", "NIST AI RMF", "CISA AI guidance"],
        "real_world_reference": "Nation-state groups are actively researching agentic AI for offensive OT operations",
        "answers": """
MODEL ANSWERS - OT-AI-001 (Instructor Mode)

Q1. Agentic AI differs from traditional malware in three key ways:
    Traditional malware follows fixed programmed attack patterns.
    Agentic AI autonomously adapts its tactics based on what it
    discovers. It can reason about the environment, make decisions,
    and change approach when defences are encountered. Against legacy
    OT systems with slow human response times this creates a
    significant defensive gap as the AI can operate faster than
    any human analyst can respond.

Q2. End-of-life systems cannot be patched meaning known vulnerabilities
    remain permanently exploitable. Agentic AI can automatically
    identify EoL system versions from network traffic and banner
    information then select and deploy appropriate exploits from
    public databases. Human attackers require expertise to exploit
    specific vulnerabilities. AI can do this automatically at scale.

Q3. Common OT protocols the AI could learn include Modbus TCP,
    DNP3 and EtherNet/IP. Once learned it could send unauthorised
    write commands to PLCs, manipulate setpoints, disable safety
    functions, or cause process disruptions by injecting malicious
    commands that appear legitimate to unprotected devices.

Q4. Immediate controls: network segmentation limiting lateral movement,
    OT protocol whitelisting allowing only approved commands between
    approved devices, disable all unnecessary network connectivity,
    implement AI-powered OT monitoring to detect anomalous behaviour
    at machine speed, and increase physical security at all OT sites.

Q5. Honest answer: detection probability is currently low without
    dedicated OT monitoring. To improve: deploy AI-powered passive
    OT monitoring establishing communication baselines, implement
    anomaly detection on all OT protocol traffic, and create alerts
    for any new device or unexpected communication path.
""",
    },
    {
        "id": "OT-AI-002",
        "domain": "AI and Agentic AI Threats",
        "sub_topic": "Adversarial AI and Sensor Data Manipulation",
        "difficulty": "beginner",
        "objective": "Understand adversarial attacks against AI systems in OT environments",
        "scenario_template": """
A {industry} has deployed an AI-powered system that automatically
adjusts {process_parameter} based on real-time sensor readings.
The system has been operating successfully for {operating_period}.

A security researcher reports that the AI system is vulnerable to
adversarial input attacks. By feeding carefully crafted false
readings to {num_sensors} sensors the attacker could cause the
AI to make dangerous automated adjustments without any operator
awareness.

Current safeguards:
  - AI makes automatic adjustments within defined limits
  - Operators monitor a dashboard but rarely intervene
  - Physical safety systems exist but are set at extreme limits
  - No sensor data validation or cross-checking is implemented
  - No anomaly detection on sensor readings themselves

Questions:
1. Explain what an adversarial AI attack is in the context of
   OT environments. How does feeding false sensor data to an
   AI system differ from traditional sensor spoofing attacks?

2. The AI operates within defined limits. Why does this not
   adequately protect against adversarial sensor manipulation
   in a {industry} context?

3. What immediate technical controls would you implement to
   validate sensor data integrity before the AI processes it?
   Describe at least THREE specific validation approaches.

4. The physical safety systems are set at extreme limits.
   Why is this insufficient as the primary safeguard against
   AI adversarial attacks on {process_parameter} control?

5. Design a human-in-the-loop framework for this AI system
   that maintains operational efficiency while ensuring human
   oversight of safety-critical automated decisions.
""",
        "variables": {
            "industry": [
                "water treatment facility",
                "chemical processing plant",
                "pharmaceutical manufacturer",
                "food processing facility",
            ],
            "process_parameter": [
                "chemical dosing rates",
                "reactor temperature and pressure",
                "mixing ratios and temperatures",
                "pasteurisation temperatures",
            ],
            "operating_period": ["6 months", "2 years", "18 months", "3 years"],
            "num_sensors": ["12", "8", "24", "6"],
        },
        "frameworks": ["NIST AI RMF", "IEC 62443", "NIST SP 800-82"],
        "real_world_reference": "The Oldsmar water treatment attack demonstrated direct manipulation of chemical dosing - AI control amplifies this risk",
        "answers": """
MODEL ANSWERS - OT-AI-002 (Instructor Mode)

Q1. An adversarial AI attack specifically targets the AI decision-making
    process by crafting inputs that cause incorrect outputs while
    appearing normal. Traditional sensor spoofing sends obviously
    false values. Adversarial attacks send carefully calculated values
    that stay within normal ranges but cause the AI model to make
    dangerous decisions due to how AI models process edge-case inputs.

Q2. Operating within defined limits does not protect against gradual
    adversarial manipulation that stays within those limits while
    causing harmful cumulative effects. In a water treatment facility
    for example dosing rates could be manipulated to dangerous levels
    through small incremental changes that each individually appear
    within acceptable bounds.

Q3. Three sensor validation approaches:
    - Cross-check multiple independent sensors measuring the same
      parameter and alert when readings diverge significantly.
    - Implement physical sample testing to periodically verify
      sensor readings against independent laboratory measurements.
    - Apply statistical process control to detect sensor readings
      that deviate from expected process behaviour patterns.

Q4. Extreme physical safety limits mean the safety system only
    intervenes at catastrophic levels. Adversarial attacks aim to
    cause harm at levels below these extreme limits where the
    safety system does not activate. The gap between AI operating
    limits and physical safety system limits is the attack space.

Q5. Human-in-the-loop framework: AI makes routine adjustments
    autonomously within tight bounds, alerts operators for any
    adjustment exceeding 10% of normal range requiring acknowledgement,
    requires human approval for any adjustment to safety-critical
    parameters, and escalates automatically when multiple sensors
    show correlated unusual readings.
""",
    },
    {
        "id": "OT-AI-003",
        "domain": "AI and Agentic AI Threats",
        "sub_topic": "AI-Powered OT Defence and Anomaly Detection",
        "difficulty": "beginner",
        "objective": "Understand how AI can be used defensively in OT environments",
        "scenario_template": """
You are implementing an AI-powered security monitoring programme
for a {industry}. The organisation has {num_assets} OT assets
and has never had dedicated OT security monitoring before.

The AI monitoring platform you are deploying will:
  - Passively analyse all OT network traffic
  - Learn normal communication patterns over {baseline_period}
  - Generate alerts when deviations are detected
  - Integrate with your existing IT SIEM
  - Provide asset discovery and inventory

Initial deployment challenges:
  - {challenge_1}
  - {challenge_2}
  - Operations team concerned about false positives disrupting work
  - Limited OT security expertise on the team

Questions:
1. Explain the difference between AI-powered anomaly detection
   and traditional signature-based OT monitoring. Why is AI
   particularly valuable in OT environments with legacy protocols?

2. The baseline learning period is {baseline_period}. What factors
   in the OT environment could cause the AI to learn an incorrect
   baseline and how would you ensure baseline accuracy?

3. The operations team is concerned about false positives.
   How would you address this concern and what processes would
   you implement to tune the AI model over time?

4. The AI monitoring integrates with your IT SIEM. What specific
   OT security events should generate the highest priority alerts
   and why?

5. After {baseline_period} of learning the AI generates its first
   high-confidence alert showing an engineering workstation
   communicating with a PLC using an unusual Modbus function code
   at 2AM. Walk through your investigation and response process.
""",
        "variables": {
            "industry": [
                "electricity distribution company",
                "water utility",
                "gas pipeline operator",
                "manufacturing facility",
            ],
            "num_assets": ["127", "340", "89", "520"],
            "baseline_period": ["30 days", "60 days", "90 days", "45 days"],
            "challenge_1": [
                "Multiple legacy protocols including Modbus and DNP3",
                "12 different vendor platforms with proprietary protocols",
                "Sites spread across a wide geographic area",
            ],
            "challenge_2": [
                "No existing network documentation or diagrams",
                "Unknown asset inventory at remote sites",
                "Inconsistent network architecture across sites",
            ],
        },
        "frameworks": ["NIST AI RMF", "NIST SP 800-82", "IEC 62443-3-3"],
        "real_world_reference": "Dragos Claroty and Nozomi Networks use AI to detect OT threats that signature-based tools miss",
        "answers": """
MODEL ANSWERS - OT-AI-003 (Instructor Mode)

Q1. Traditional signature-based monitoring requires known attack
    signatures to detect threats. It cannot detect novel attacks
    or techniques without known patterns. AI anomaly detection
    learns what normal looks like for the specific environment and
    detects any deviation including completely novel attack techniques.
    In OT environments with legacy protocols that lack built-in
    security AI anomaly detection provides detection capability
    that signatures alone cannot achieve.

Q2. Baseline accuracy risks: scheduled maintenance activities
    creating unusual but legitimate traffic during the baseline
    period, seasonal process variations, legacy devices with
    inconsistent communication patterns. Ensure accuracy by:
    documenting all maintenance scheduled during baseline period,
    extending baseline to capture full operational cycle,
    and having OT engineers review and validate the learned baseline.

Q3. Address false positive concerns: start with alerting only
    on highest-confidence anomalies, create a feedback process
    where operators mark false positives to improve the model,
    tune alert thresholds progressively as confidence grows,
    and track false positive rate as a key metric reporting
    improvements to operations management monthly.

Q4. Highest priority OT alerts: new unauthorised device on OT
    network, engineering workstation communicating with PLC
    outside maintenance windows, unknown Modbus function codes,
    safety system parameter changes without change request,
    and any communication to/from external IP addresses.

Q5. Investigation process: check change management records for
    any approved 2AM maintenance, review workstation event logs
    for user login activity, examine the specific Modbus function
    code sent and what register it targeted, check PLC audit log
    for any resulting configuration changes, and if no legitimate
    explanation isolate the workstation and escalate to incident
    response.
""",
    },
]

# Add to OT_DOMAIN_MAP
OT_DOMAIN_MAP["ai_threats"] = AI_THREAT_SCENARIOS
ALL_OT_SCENARIOS.extend(AI_THREAT_SCENARIOS)

if __name__ == "__main__":
    print("GIDEON - OT/ICS Security Module Test")
    print(f"Total scenarios: {len(ALL_OT_SCENARIOS)}")
    for domain in OT_DOMAIN_MAP:
        print(f"  {domain:20} : {len(OT_DOMAIN_MAP[domain])} templates")
    print()
    s = get_random_ot_scenario()
    display_ot_scenario(s)
