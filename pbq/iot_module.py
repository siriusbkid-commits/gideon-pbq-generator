"""
GIDEON IoT Security Module
============================
Scenario-based PBQ generator for IoT Security for IT Professionals.
Covers: IoT Architecture, OWASP IoT Top 10, Network Security,
Industrial IoT (IIoT), and Incident Response.

No LLM required - instant generation from randomised templates.
Standalone module - not tied to any specific exam.
"""

import random

IOT_MODULE_INFO = {
    "name": "IoT Security",
    "version": "1.0",
    "description": "Internet of Things Security for IT Professionals",
    "frameworks": ["OWASP IoT Top 10", "NIST SP 800-213", "ENISA IoT Security"],
}

# ================================================================
# SECTION 1 - IOT ARCHITECTURE AND ATTACK SURFACE
# ================================================================

ARCHITECTURE_SCENARIOS = [
    {
        "id": "IOT-ARCH-001",
        "domain": "IoT Architecture",
        "sub_topic": "IoT Attack Surface and Components",
        "difficulty": "beginner",
        "objective": "Understand the IoT attack surface and component security",
        "scenario_template": """
You are a security consultant engaged by a {industry} to assess
the security of their newly deployed IoT infrastructure.

The IoT deployment includes:
  - {num_devices} connected devices across {num_locations} locations
  - Device types: {device_types}
  - Connectivity: {connectivity}
  - Management platform: cloud-based vendor portal
  - Firmware update method: {update_method}
  - Default credentials: not changed on {default_cred_percent}% of devices
  - Network: IoT devices on the same network as corporate systems

Questions:
1. Identify the FIVE main components of an IoT architecture and
   explain the security risks associated with each component.
   Use the devices in this deployment as examples.

2. {default_cred_percent}% of devices still have default credentials.
   Why are default credentials such a critical IoT vulnerability?
   What real world attack demonstrated the catastrophic scale of
   this problem and how many devices were compromised?

3. The IoT devices share a network with corporate systems.
   What specific attack paths does this create? Design a network
   segmentation approach to isolate the IoT devices.

4. The firmware update method is {update_method}. What security
   risks does this method introduce and what is the secure
   alternative approach for IoT firmware updates?

5. Conduct an attack surface analysis for this IoT deployment.
   List at least SIX attack vectors an adversary could exploit
   and rate each as Critical, High, or Medium risk.
""",
        "variables": {
            "industry": [
                "smart building management company",
                "hospital and healthcare provider",
                "retail chain with 50 stores",
                "manufacturing facility",
                "smart city infrastructure operator",
            ],
            "num_devices": ["847", "2,400", "340", "12,000"],
            "num_locations": ["12", "50", "4", "200"],
            "device_types": [
                "IP cameras, access control readers, HVAC sensors and smart locks",
                "medical monitors, infusion pumps, bed sensors and nurse call systems",
                "POS terminals, digital signage, inventory sensors and CCTV",
                "production sensors, conveyor monitors and environmental controls",
            ],
            "connectivity": [
                "WiFi and Zigbee",
                "4G LTE and WiFi",
                "LoRaWAN and WiFi",
                "Ethernet and Zigbee",
            ],
            "update_method": [
                "manual USB updates by technicians",
                "automatic updates from vendor cloud with no verification",
                "no update process exists",
                "updates disabled to avoid downtime",
            ],
            "default_cred_percent": ["67", "43", "89", "55"],
        },
        "frameworks": ["OWASP IoT Top 10", "NIST SP 800-213", "ENISA IoT Guidelines"],
        "real_world_reference": "Mirai botnet 2016 compromised 600,000 IoT devices using default credentials causing major internet outages",
    },
    {
        "id": "IOT-ARCH-002",
        "domain": "IoT Architecture",
        "sub_topic": "IoT Communication Protocols and Security",
        "difficulty": "beginner",
        "objective": "Understand IoT protocol security weaknesses",
        "scenario_template": """
You are reviewing the IoT infrastructure at a {industry}.
A security scan has identified multiple protocol-level vulnerabilities.

The environment uses the following protocols:
  - {protocol_1} for device-to-cloud communication
  - {protocol_2} for device-to-device messaging
  - {protocol_3} for local device discovery
  - Bluetooth Low Energy for mobile device pairing
  - HTTP (not HTTPS) for device management API

Scan findings:
  - {protocol_1} connections use no authentication
  - {protocol_2} broker has no access controls
  - {protocol_3} exposes device information to anyone on the network
  - BLE pairing uses Just Works mode with no PIN
  - HTTP API exposes device credentials in plaintext

Questions:
1. Explain the purpose of {protocol_1} and {protocol_2} in IoT
   architectures. Why are these protocols commonly used and what
   security features do they lack by default?

2. The MQTT broker ({protocol_2}) has no access controls. What can
   an attacker do if they gain access to an unsecured MQTT broker?
   Give THREE specific attack scenarios.

3. {protocol_3} exposes device information to the local network.
   What information does this protocol typically expose and how
   could an attacker use this for reconnaissance?

4. The HTTP management API exposes credentials in plaintext.
   Beyond upgrading to HTTPS what additional API security controls
   should be implemented for IoT device management?

5. Design a secure protocol stack for this IoT deployment.
   For each layer specify the protocol, security mechanism,
   and authentication method you would recommend.
""",
        "variables": {
            "industry": [
                "smart home platform provider",
                "industrial IoT solutions company",
                "healthcare IoT vendor",
                "smart city operator",
            ],
            "protocol_1": ["MQTT", "AMQP", "CoAP", "MQTT over WebSocket"],
            "protocol_2": ["MQTT", "AMQP", "DDS", "MQTT"],
            "protocol_3": ["mDNS/Bonjour", "SSDP/UPnP", "WS-Discovery", "Zeroconf"],
        },
        "frameworks": ["OWASP IoT Top 10", "NIST SP 800-213"],
        "real_world_reference": "Unsecured MQTT brokers are routinely found exposed on the internet with no authentication",
    },
]

# ================================================================
# SECTION 2 - OWASP IOT TOP 10 SCENARIOS
# ================================================================

OWASP_SCENARIOS = [
    {
        "id": "IOT-OWASP-001",
        "domain": "OWASP IoT Top 10",
        "sub_topic": "Weak Passwords and Insecure Update Mechanisms",
        "difficulty": "beginner",
        "objective": "Apply OWASP IoT Top 10 to real world scenarios",
        "scenario_template": """
You are conducting an IoT security assessment for a {industry}.
During your assessment you discover the following issues:

Finding 1 — Weak Credentials:
  - {num_devices} devices use the default password: {default_password}
  - Admin interface accessible from the internet on port {admin_port}
  - No account lockout after failed login attempts
  - Credentials transmitted over HTTP

Finding 2 — Insecure Update Mechanism:
  - Firmware downloaded from {update_source}
  - No cryptographic signature verification on firmware
  - Update process can be triggered by any device on the network
  - Last firmware update: {last_update}
  - Known critical vulnerability in current firmware: {known_cve}

Questions:
1. Finding 1 maps to OWASP IoT Top 10 item I1 - Weak Passwords.
   Explain why weak default passwords are so prevalent in IoT devices
   and why manufacturers have historically not addressed this.
   What regulations are now requiring change?

2. An attacker discovers the admin interface on port {admin_port}.
   Walk through the attack steps from initial discovery to full
   device compromise. What tools would they use at each step?

3. Finding 2 maps to OWASP IoT Top 10 item I5 - Use of Insecure
   or Outdated Components. The known vulnerability {known_cve} has
   a public exploit available. What is your immediate recommendation
   and what is the risk if patching is delayed?

4. The update mechanism has no signature verification. Explain how
   an attacker could perform a malicious firmware update attack.
   What would a signed firmware update process look like?

5. Write a prioritised remediation plan for both findings with
   timelines, responsible parties, and success criteria.
   Which finding is more critical and why?
""",
        "variables": {
            "industry": [
                "hotel chain with smart room controls",
                "hospital with connected medical devices",
                "manufacturing plant with IoT sensors",
                "retail chain with smart shelf systems",
            ],
            "num_devices": ["340", "1,200", "89", "2,400"],
            "default_password": ["admin/admin", "root/root", "admin/1234", "user/password"],
            "admin_port": ["80", "8080", "443", "8443"],
            "update_source": [
                "HTTP (unencrypted) vendor server",
                "an S3 bucket with public read access",
                "a vendor FTP server with no authentication",
            ],
            "last_update": ["3 years ago", "never", "5 years ago", "18 months ago"],
            "known_cve": ["CVE-2021-20090", "CVE-2022-27255", "CVE-2023-1380"],
        },
        "frameworks": ["OWASP IoT Top 10", "NIST SP 800-213"],
        "real_world_reference": "Mirai botnet exploited default credentials. Firmware signing is now required by UK PSTI Act 2024",
    },
    {
        "id": "IOT-OWASP-002",
        "domain": "OWASP IoT Top 10",
        "sub_topic": "Insecure Network Services and Ecosystem Interfaces",
        "difficulty": "beginner",
        "objective": "Identify and remediate insecure IoT network services",
        "scenario_template": """
During an IoT penetration test of a {industry} you run a port scan
against a sample of {num_devices} IoT devices and find:

Device type: {device_type}
Open ports found on most devices:
  - Port 23 (Telnet) — no encryption, accepts default credentials
  - Port 80 (HTTP) — web management interface
  - Port 554 (RTSP) — video stream, no authentication required
  - Port 9999 — unknown service, banner shows {banner_info}
  - Port 5555 (ADB) — Android Debug Bridge enabled

Cloud management interface findings:
  - API endpoint: https://api.{vendor_domain}.com/v1/devices
  - API accepts requests with no authentication token
  - API returns full device list including location data for ALL customers
  - Password reset link does not expire

Questions:
1. Map each open port to the relevant OWASP IoT Top 10 category.
   For each port explain the specific risk it represents.

2. Port 554 RTSP streams require no authentication. For {device_type}
   devices what is the real world privacy and security impact of
   unauthenticated video access? Name a real incident where this
   occurred at scale.

3. The ADB port (5555) is enabled on production IoT devices.
   What is ADB, why is it dangerous on production devices, and
   what level of access does it provide to an attacker?

4. The cloud API returns ALL customer device data with no authentication.
   This is OWASP IoT Top 10 I3 - Insecure Ecosystem Interfaces.
   What data privacy regulations are violated and what are the
   potential financial penalties?

5. Design a secure network service baseline for {device_type} devices.
   Specify which services should be enabled, disabled, and hardened
   in a production deployment.
""",
        "variables": {
            "industry": [
                "smart home device manufacturer",
                "IP camera vendor",
                "connected baby monitor company",
                "smart TV manufacturer",
            ],
            "num_devices": ["50", "20", "100", "35"],
            "device_type": [
                "IP security cameras",
                "smart home hubs",
                "connected baby monitors",
                "smart TVs",
            ],
            "banner_info": [
                "BusyBox v1.19.4 — Linux embedded shell",
                "Dropbear SSH — outdated version",
                "lighttpd/1.4.35",
            ],
            "vendor_domain": ["smartcam", "iotdevice", "connectedhome", "smarthub"],
        },
        "frameworks": ["OWASP IoT Top 10", "NIST SP 800-213", "GDPR", "UK PSTI Act"],
        "real_world_reference": "Shodan regularly finds millions of unauthenticated RTSP streams and open Telnet ports on IoT devices",
    },
]

# ================================================================
# SECTION 3 - IOT NETWORK SECURITY
# ================================================================

NETWORK_SCENARIOS = [
    {
        "id": "IOT-NET-001",
        "domain": "IoT Network Security",
        "sub_topic": "IoT Network Segmentation and Monitoring",
        "difficulty": "beginner",
        "objective": "Design and implement IoT network security controls",
        "scenario_template": """
You are the security architect for a {industry}. The organisation
has deployed {num_devices} IoT devices and wants to improve security.

Current network state:
  - All IoT devices on the main corporate network (192.168.1.0/24)
  - IoT devices can communicate freely with servers and workstations
  - No traffic monitoring on IoT device communications
  - IoT devices have unrestricted internet access
  - A compromised IP camera was recently used to pivot to a file server

Planned IoT expansion: {expansion_plan}

Questions:
1. The compromised camera pivot attack succeeded because of flat
   network architecture. Explain the concept of IoT network
   segmentation and why it is the most important IoT security control.

2. Design a segmented network architecture for this {industry}.
   Include: IoT VLAN design, firewall rules between segments,
   DNS filtering for IoT devices, and internet access controls.

3. What IoT-specific network monitoring would you implement?
   Explain what baseline normal IoT traffic looks like and what
   anomalies would indicate compromise for {device_category} devices.

4. The planned expansion {expansion_plan} introduces new device types.
   What onboarding security process should every new IoT device go
   through before connecting to the network?

5. A new IoT device from {vendor_type} vendor requests network access.
   Write a security assessment checklist of 10 questions you would
   ask before approving the device for deployment.
""",
        "variables": {
            "industry": [
                "law firm with smart office controls",
                "school with connected classroom devices",
                "hospital with building management IoT",
                "hotel chain with smart room technology",
            ],
            "num_devices": ["120", "450", "800", "2,000"],
            "expansion_plan": [
                "adding 500 smart parking sensors across 3 car parks",
                "deploying connected medical devices in 20 new wards",
                "installing smart energy monitors in 100 rooms",
                "adding AI-powered security cameras at all entrances",
            ],
            "device_category": [
                "IP cameras and access control",
                "medical monitoring devices",
                "HVAC and building management",
                "point of sale terminals",
            ],
            "vendor_type": ["Chinese", "budget", "unverified", "new"],
        },
        "frameworks": ["NIST SP 800-213", "ENISA IoT Security Guidelines"],
        "real_world_reference": "The Target breach 2013 began with a compromised HVAC contractor - IoT pivot attacks are well documented",
    },
    {
        "id": "IOT-NET-002",
        "domain": "IoT Network Security",
        "sub_topic": "IoT Device Identity and Authentication",
        "difficulty": "intermediate",
        "objective": "Implement device identity and authentication for IoT",
        "scenario_template": """
You are implementing a zero trust security model for IoT devices
at a {industry}. The organisation has {num_devices} devices from
{num_vendors} different vendors.

Current authentication state:
  - Devices authenticate using shared API keys stored in firmware
  - Same API key used across all devices of the same model
  - No device identity certificates deployed
  - Device-to-cloud communication uses username/password
  - No mutual TLS (mTLS) implemented
  - Compromised API key found on a public GitHub repository

Questions:
1. Explain the concept of device identity in IoT security.
   Why is a unique cryptographic identity per device important
   and what are the consequences of shared credentials as shown
   in this scenario?

2. The shared API key was found on GitHub. What is the immediate
   impact of this exposure across all {num_devices} devices and
   what is your immediate response?

3. Compare these IoT device authentication approaches and recommend
   one for this deployment:
   a) Username and password per device
   b) API keys per device
   c) X.509 certificates with PKI
   d) Hardware security modules (HSM)

4. Explain mutual TLS (mTLS) and why it is particularly valuable
   for IoT device authentication. What does it protect against
   that one-way TLS does not?

5. Design a device identity lifecycle management process covering:
   device provisioning, certificate rotation, device retirement,
   and compromised device response for a fleet of {num_devices} devices.
""",
        "variables": {
            "industry": [
                "energy utility with smart meters",
                "logistics company with asset trackers",
                "agricultural IoT platform",
                "smart city infrastructure operator",
            ],
            "num_devices": ["50,000", "12,000", "4,500", "100,000"],
            "num_vendors": ["8", "12", "4", "20"],
        },
        "frameworks": ["NIST SP 800-213", "OWASP IoT Top 10", "IEC 62443"],
        "real_world_reference": "Shared IoT credentials in firmware have been found on GitHub repeatedly exposing entire device fleets",
    },
]

# ================================================================
# SECTION 4 - INDUSTRIAL IOT (IIOT)
# ================================================================

IIOT_SCENARIOS = [
    {
        "id": "IOT-IIOT-001",
        "domain": "Industrial IoT (IIoT)",
        "sub_topic": "IIoT Security and OT/IoT Convergence",
        "difficulty": "intermediate",
        "objective": "Understand the security implications of IIoT deployments",
        "scenario_template": """
A {industry} is deploying an Industrial IoT platform to connect
{num_sensors} sensors across the production environment to a
cloud analytics platform for predictive maintenance.

The IIoT architecture:
  - {num_sensors} sensors connected via {connectivity} to edge gateways
  - Edge gateways transmit data to {cloud_platform} cloud platform
  - Data includes: equipment performance, temperature, vibration, pressure
  - Maintenance engineers access analytics via mobile app from anywhere
  - The IIoT network connects to the existing OT/SCADA network
  - No security assessment performed before deployment

Concern raised by OT engineer:
  "Adding internet-connected sensors to our production environment
   creates a new attack path directly into our control systems."

Questions:
1. The OT engineer raises a valid concern. Explain how an IIoT
   deployment creates new attack paths into OT environments that
   did not previously exist.

2. What is the difference between IoT and IIoT from a security
   perspective? Why are the consequences of an IIoT security
   incident potentially more severe than a standard IoT incident?

3. The edge gateways connect both to the internet and the OT network.
   What security controls must be implemented on edge gateways
   to prevent them becoming a pivot point into OT systems?

4. Maintenance engineers access the system via mobile app from anywhere.
   What identity and access management controls should govern
   this remote access to an industrial environment?

5. Conduct a risk assessment of this IIoT deployment. Identify
   the top 5 risks, rate each by likelihood and impact, and
   provide a specific mitigation for each.
""",
        "variables": {
            "industry": [
                "oil refinery",
                "pharmaceutical manufacturer",
                "automotive assembly plant",
                "food and beverage producer",
            ],
            "num_sensors": ["2,400", "800", "4,000", "1,200"],
            "connectivity": [
                "LoRaWAN and industrial Ethernet",
                "4G LTE and WiFi",
                "Zigbee and industrial Ethernet",
                "5G private network",
            ],
            "cloud_platform": [
                "Microsoft Azure IoT Hub",
                "AWS IoT Core",
                "Google Cloud IoT",
                "a third-party vendor platform",
            ],
        },
        "frameworks": ["IEC 62443", "NIST SP 800-82", "NIST SP 800-213"],
        "real_world_reference": "IIoT deployments are increasingly targeted as entry points into OT environments",
    },
]

# ================================================================
# SECTION 5 - IOT INCIDENT RESPONSE
# ================================================================

INCIDENT_SCENARIOS = [
    {
        "id": "IOT-IR-001",
        "domain": "IoT Incident Response",
        "sub_topic": "IoT Compromise Detection and Response",
        "difficulty": "beginner",
        "objective": "Respond effectively to IoT security incidents",
        "scenario_template": """
You are the security manager at a {industry}. Your network monitoring
tool has generated the following alerts over the past hour:

Alert 1: IoT device {device_ip} generating {traffic_volume} outbound
         traffic to IP {external_ip} — normal is under 10MB/day
Alert 2: {num_devices_scanning} IoT devices performing internal
         port scans against corporate network
Alert 3: New device {unknown_device} appeared on IoT VLAN —
         not in asset inventory
Alert 4: IP camera {camera_id} login from {foreign_country} —
         camera is physically located in your {location}

The devices affected are: {device_types}

Questions:
1. Triage these four alerts in priority order. Which represents
   the most critical immediate risk and why?

2. Alert 1 shows massive outbound traffic from one IoT device.
   What are the THREE most likely explanations and how would
   you quickly determine which is correct?

3. Alerts 1 and 2 together suggest a specific attack scenario.
   What has likely happened and what is the attacker attempting
   to do with the compromised IoT devices?

4. For Alert 4 — the camera login from {foreign_country} —
   what is your immediate response? Can you simply change the
   password and consider it resolved? Why or why not?

5. Write an IoT-specific incident response checklist for the
   first 30 minutes of a suspected IoT compromise. Include
   containment steps that minimise operational disruption.
""",
        "variables": {
            "industry": [
                "law firm",
                "hospital",
                "school",
                "retail company",
                "manufacturing facility",
            ],
            "device_ip": ["192.168.10.47", "10.10.5.88", "172.16.20.33"],
            "traffic_volume": ["4.7GB", "12GB", "8.2GB"],
            "external_ip": ["185.220.101.47", "103.75.190.22", "91.108.4.150"],
            "num_devices_scanning": ["14", "47", "8"],
            "unknown_device": ["192.168.10.199", "10.10.5.250", "172.16.20.199"],
            "camera_id": ["CAM-LOBBY-01", "CAM-SERVER-03", "CAM-ENTRANCE-02"],
            "foreign_country": ["Russia", "China", "North Korea"],
            "location": ["Auckland office", "London headquarters", "Sydney data centre"],
            "device_types": [
                "IP cameras and access control readers",
                "smart building sensors and HVAC controllers",
                "connected printers and smart displays",
            ],
        },
        "frameworks": ["NIST SP 800-213", "OWASP IoT Top 10"],
        "real_world_reference": "Compromised IoT devices are frequently used as botnet nodes for DDoS attacks and network pivoting",
    },
    {
        "id": "IOT-IR-002",
        "domain": "IoT Incident Response",
        "sub_topic": "IoT Botnet and DDoS Response",
        "difficulty": "intermediate",
        "objective": "Understand and respond to IoT botnet activity",
        "scenario_template": """
Your ISP has notified you that {num_devices} IoT devices on your
network are participating in a DDoS attack against {target}.
The devices have been compromised and are part of a botnet.

Affected devices: {device_types} across {num_locations} locations
Attack traffic: {attack_volume} outbound UDP traffic
Botnet variant: suspected {botnet_name} or variant
Initial infection vector: {infection_vector}

Your internet connection is being throttled by your ISP due to
the attack traffic. Normal business operations are impacted.

Questions:
1. Explain how IoT botnets like Mirai work. How do they initially
   compromise devices, how do they maintain persistence, and how
   are they controlled by attackers?

2. Your ISP is threatening to null-route your IP block if the
   attack traffic continues. What immediate network-level actions
   do you take to stop the outbound attack traffic?

3. {num_devices} devices are compromised across {num_locations}
   locations. You cannot physically visit all locations immediately.
   How do you remotely identify, isolate, and remediate compromised
   devices at scale?

4. After containment, forensic analysis shows the infection vector
   was {infection_vector}. What systematic changes to your IoT
   security programme would prevent reinfection?

5. The incident has caused {business_impact}. Write a post-incident
   report summary including: root cause, timeline, impact, remediation
   steps taken, and lessons learned.
""",
        "variables": {
            "num_devices": ["340", "89", "1,200", "47"],
            "target": ["a government website", "a competitor organisation", "a cloud provider", "a financial institution"],
            "device_types": [
                "IP cameras and DVR systems",
                "smart routers and NAS devices",
                "IP cameras and smart TVs",
            ],
            "num_locations": ["12", "4", "50", "3"],
            "attack_volume": ["2.3Gbps", "800Mbps", "4.7Gbps"],
            "botnet_name": ["Mirai", "Mozi", "BotenaGo", "RapperBot"],
            "infection_vector": [
                "default credentials never changed on deployment",
                "a known firmware vulnerability unpatched for 18 months",
                "an exposed Telnet service with weak credentials",
            ],
            "business_impact": [
                "4 hours of degraded internet connectivity and reputational damage",
                "participation in a criminal DDoS attack creating legal liability",
                "ISP suspension of service for 24 hours",
            ],
        },
        "frameworks": ["NIST SP 800-213", "CISA IoT guidance"],
        "real_world_reference": "Mirai botnet 2016 used 600,000 compromised IoT devices to generate 1.2Tbps DDoS — largest recorded at the time",
    },
]

# ================================================================
# COMBINED POOL
# ================================================================

ALL_IOT_SCENARIOS = (
    ARCHITECTURE_SCENARIOS +
    OWASP_SCENARIOS +
    NETWORK_SCENARIOS +
    IIOT_SCENARIOS +
    INCIDENT_SCENARIOS
)

IOT_DOMAIN_MAP = {
    "architecture":        ARCHITECTURE_SCENARIOS,
    "owasp":               OWASP_SCENARIOS,
    "network":             NETWORK_SCENARIOS,
    "iiot":                IIOT_SCENARIOS,
    "incident_response":   INCIDENT_SCENARIOS,
}

# ================================================================
# GENERATOR
# ================================================================

def generate_iot_scenario(domain_filter=None, difficulty_filter=None):
    if domain_filter and domain_filter in IOT_DOMAIN_MAP:
        pool = IOT_DOMAIN_MAP[domain_filter]
    else:
        pool = ALL_IOT_SCENARIOS

    if difficulty_filter:
        filtered = [s for s in pool if s["difficulty"] == difficulty_filter]
        if filtered:
            pool = filtered

    if not pool:
        pool = ALL_IOT_SCENARIOS

    template = random.choice(pool)
    scenario_text = template["scenario_template"]

    for var_name, options in template.get("variables", {}).items():
        chosen = random.choice(options)
        scenario_text = scenario_text.replace("{" + var_name + "}", chosen)

    return {
        "module":      "IoT Security",
        "id":          template["id"],
        "domain":      template["domain"],
        "sub_topic":   template["sub_topic"],
        "objective":   template["objective"],
        "difficulty":  template["difficulty"],
        "frameworks":  ", ".join(template.get("frameworks", [])),
        "real_world":  template.get("real_world_reference", ""),
        "scenario":    scenario_text.strip(),
    }


def get_random_iot_scenario():
    return generate_iot_scenario()


def display_iot_scenario(s: dict):
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  GIDEON - IoT Security Module")
    print(f"  ID         : {s.get('id', 'N/A')}")
    print(f"  Domain     : {s.get('domain', 'N/A')}")
    print(f"  Sub-topic  : {s.get('sub_topic', 'N/A')}")
    print(f"  Objective  : {s.get('objective', 'N/A')}")
    print(f"  Difficulty : {s.get('difficulty', 'N/A').upper()}")
    print(f"  Frameworks : {s.get('frameworks', 'N/A')}")
    print(f"  Real World : {s.get('real_world', 'N/A')}")
    print(sep)
    print(s.get("scenario", "No scenario generated."))
    print(f"\n{sep}\n")


if __name__ == "__main__":
    print("GIDEON - IoT Security Module Test")
    print(f"Total scenarios: {len(ALL_IOT_SCENARIOS)}")
    for domain in IOT_DOMAIN_MAP:
        print(f"  {domain:20} : {len(IOT_DOMAIN_MAP[domain])} templates")
    print()
    s = get_random_iot_scenario()
    display_iot_scenario(s)
