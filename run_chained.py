import json
import sys
import os
from datetime import datetime

from pbq.generator import PBQGenerator, PBQContext
from llm_factory import get_llm


# ============================================================
# INLINE SCENARIO VALIDATOR (replaces scenario_validator.py)
# ============================================================

def validate_scenario(scenario: dict):
    """
    Minimal scenario validator to ensure required fields exist.
    Prevents crashes during PBQ generation.
    """
    if not isinstance(scenario, dict):
        raise ValueError("Scenario must be a JSON object.")

    if "id" not in scenario:
        raise ValueError("Scenario missing required field: 'id'")

    if "metadata" not in scenario:
        raise ValueError("Scenario missing required field: 'metadata'")

    if "title" not in scenario["metadata"]:
        raise ValueError("Scenario metadata missing required field: 'title'")


# ============================================================
# SCENARIO TYPE DETECTION
# ============================================================

def is_sign_in_scenario(s: dict) -> bool:
    """
    Determines whether the scenario is an Azure AD sign-in scenario.
    """
    required_fields = [
        "location",
        "previous_location",
        "device",
        "mfa",
        "privilege_level",
        "sign_in_result"
    ]
    return all(field in s for field in required_fields)


# ============================================================
# IAM ANALYSIS MODULES (Azure AD only)
# ============================================================

def analyze_identity_risk(s):
    """
    IAM risk analysis for Azure AD sign-in scenarios.
    """
    risk_factors = []

    if s["location"] != s["previous_location"]:
        risk_factors.append("Impossible travel or unusual location change detected.")

    if s["mfa"] == "failed":
        risk_factors.append("MFA failure prior to successful sign-in.")

    if s["device"] == "unknown":
        risk_factors.append("Sign-in from unknown or unmanaged device.")

    if s["privilege_level"] in ["admin", "global_admin"]:
        risk_factors.append("Privileged account sign-in.")

    return {
        "risk_factors": risk_factors,
        "sign_in_result": s["sign_in_result"]
    }


def evaluate_conditional_access(s, iam_result):
    """
    Conditional Access evaluation for Azure AD scenarios.
    """
    if not iam_result:
        return None

    ca_findings = []

    if "Impossible travel" in " ".join(iam_result["risk_factors"]):
        ca_findings.append("CA policy should block or require MFA for location anomalies.")

    if s["device"] == "unknown":
        ca_findings.append("CA should require compliant or hybrid-joined devices.")

    return {"ca_findings": ca_findings}


def evaluate_pim(s, iam_result):
    """
    PIM evaluation for Azure AD scenarios.
    """
    if not iam_result:
        return None

    pim_findings = []

    if s["privilege_level"] in ["admin", "global_admin"]:
        pim_findings.append("Privileged role activation should require justification and approval.")

    return {"pim_findings": pim_findings}


# ============================================================
# PAM / GOVERNANCE / COMPLIANCE (ALL SCENARIOS)
# ============================================================

def evaluate_pam(s, iam_result):
    pam_findings = []

    if "CyberArk" in json.dumps(s):
        pam_findings.append("CyberArk PSM session detected — review session recording and commands executed.")

    if "privileged" in json.dumps(s).lower():
        pam_findings.append("Privileged access detected — ensure least privilege and session monitoring.")

    return {"pam_findings": pam_findings}


def evaluate_governance(s, iam_result, pam_result):
    gov_findings = []

    gov_findings.append("Ensure privileged access follows least privilege and separation of duties.")
    gov_findings.append("Verify joiner/mover/leaver processes for privileged accounts.")

    if pam_result and "CyberArk" in json.dumps(s):
        gov_findings.append("Ensure CyberArk governance controls (dual control, session monitoring) are enforced.")

    return {"governance_findings": gov_findings}


def evaluate_compliance(s, iam_result, pam_result):
    comp_findings = []

    comp_findings.append("Verify logging and monitoring meet regulatory requirements (SOX, ISO 27001).")
    comp_findings.append("Ensure incident response procedures exist for privileged account misuse.")

    if pam_result and "CyberArk" in json.dumps(s):
        comp_findings.append("Validate CyberArk audit logs are retained per compliance policy.")

    return {"compliance_findings": comp_findings}


# ============================================================
# PBQ CONTEXT BUILDER
# ============================================================

def build_pbq_context(scenario, iam_result, ca_result, pim_result, pam_result, gov_result, comp_result):
    return PBQContext(
        scenario_id=scenario["id"],
        title=scenario["metadata"]["title"],
        summary=scenario["metadata"].get("summary", ""),
        actors=scenario["metadata"].get("actors", []),
        systems=scenario["metadata"].get("systems", []),
        risks_findings=scenario["metadata"].get("risks", []),
        controls_in_scope=scenario["metadata"].get("controls", []),
        learning_objectives=scenario["metadata"].get("learning_objectives", []),
        difficulty=scenario["metadata"].get("difficulty", "medium"),
        category=scenario["metadata"].get("category", "Identity & Access Management")
    )


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_chained.py <scenario.json>")
        sys.exit(1)

    scenario_file = sys.argv[1]

    with open(scenario_file, "r") as f:
        scenario = json.load(f)

    validate_scenario(scenario)

    print(f"\nRunning scenario: {scenario_file}\n")

    # Detect scenario type
    if is_sign_in_scenario(scenario):
        print("Detected Azure AD sign-in scenario.\n")
        iam_result = analyze_identity_risk(scenario)
        ca_result = evaluate_conditional_access(scenario, iam_result)
        pim_result = evaluate_pim(scenario, iam_result)
    else:
        print("Detected non-sign-in scenario (CyberArk / PAM / Governance).\n")
        iam_result = None
        ca_result = None
        pim_result = None

    pam_result = evaluate_pam(scenario, iam_result)
    gov_result = evaluate_governance(scenario, iam_result, pam_result)
    comp_result = evaluate_compliance(scenario, iam_result, pam_result)

    # PBQ generation
    llm = get_llm()
    generator = PBQGenerator(llm)

    ctx = build_pbq_context(scenario, iam_result, ca_result, pim_result, pam_result, gov_result, comp_result)

    pbq_id = f"pbq_{scenario['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Ensure output directory exists regardless of working directory
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    out_file = os.path.join(OUTPUT_DIR, f"{pbq_id}.json")

    pbq = generator.generate_pbq(ctx, pbq_id)

    if pbq:
        out_json = pbq.to_json()
        with open(out_file, "w") as f:
            json.dump(out_json, f, indent=2)
        print(f"\nPBQ saved to {out_file}\n")
    else:
        print("\nPBQ generation failed.\n")

