# cyberark_model.py

cyberark_safes = [
    {
        "name": "Domain Admins Safe",
        "purpose": "Store and manage domain administrator accounts",
        "requires_dual_control": True,
        "psm_required": True,
        "rotation_frequency_days": 1,
    },
    {
        "name": "Break-Glass Safe",
        "purpose": "Emergency access accounts for critical systems",
        "requires_dual_control": True,
        "psm_required": True,
        "rotation_frequency_days": 1,
    },
    {
        "name": "Server Admins Safe",
        "purpose": "Local admin accounts for servers",
        "requires_dual_control": False,
        "psm_required": True,
        "rotation_frequency_days": 7,
    },
]

cyberark_platforms = [
    {
        "name": "Windows Domain Admin Platform",
        "os_type": "Windows",
        "supports_rotation": True,
        "supports_psm": True,
        "typical_use": "Domain admin accounts in AD",
    },
    {
        "name": "Windows Local Admin Platform",
        "os_type": "Windows",
        "supports_rotation": True,
        "supports_psm": True,
        "typical_use": "Local admin accounts on servers/workstations",
    },
    {
        "name": "Break-Glass Platform",
        "os_type": "Mixed",
        "supports_rotation": True,
        "supports_psm": True,
        "typical_use": "Emergency access accounts with strict monitoring",
    },
]
