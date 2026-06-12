from crewai import Task
from cyberark_model import cyberark_safes, cyberark_platforms

# ---------------------------------------------------------
# 1. Identity Threat Analyst Task (STATIC — scenario injected later)
# ---------------------------------------------------------
evaluate_signin_task = Task(
    description=(
        "Evaluate the following mock sign-in event for identity risk. "
        "Consider impossible travel, unfamiliar device, atypical location, "
        "failed attempts, privilege level, and user history.\n\n"
        "The scenario details will be injected at runtime."
    ),
    expected_output=(
        "A clear identity risk assessment including risk level, key indicators, "
        "and a Zero Trust recommended action (allow, allow with conditions, block)."
    ),
    agent=None,
)

# ---------------------------------------------------------
# 2. Conditional Access Evaluation Task
# ---------------------------------------------------------
evaluate_conditional_access_task = Task(
    description=(
        "Using the sign-in scenario AND any context provided by previous tasks "
        "(such as risk levels, device trust, or analyst findings), evaluate the "
        "Conditional Access policy and determine the effective access decision.\n\n"
        "Consider:\n"
        "- User risk\n"
        "- Sign-in risk\n"
        "- Device trust\n"
        "- Location\n"
        "- Privilege level\n"
        "- Policy conditions\n"
        "- Grant controls\n"
    ),
    expected_output=(
        "A structured decision including:\n"
        "- Effective decision (Allow, Block, Require MFA, Other)\n"
        "- Which policy conditions were triggered\n"
        "- How previous task context influenced the decision\n"
        "- Any recommended policy improvements"
    ),
    agent=None,
)

# ---------------------------------------------------------
# 3. Privileged Access Review Task
# ---------------------------------------------------------
privileged_access_review_task = Task(
    description=(
        "Using the sign-in scenario, analyst findings, and Conditional Access decision, "
        "evaluate whether the user's privileged role assignment is appropriate.\n\n"
        "Consider:\n"
        "- Privilege level\n"
        "- Role assignment type\n"
        "- Activity context\n"
        "- Identity risk\n"
        "- Conditional Access decision\n"
        "- Zero Trust principles\n"
    ),
    expected_output=(
        "A structured privileged access review including:\n"
        "- Privilege risk level (Low/Medium/High)\n"
        "- Key privilege risk indicators\n"
        "- Recommended action (Retain, Remove, Require justification, Temporary elevation only)\n"
        "- Zero Trust justification\n"
        "- Any recommended governance improvements"
    ),
    agent=None,
)

# ---------------------------------------------------------
# 4. CyberArk-Enhanced PIM/PAM Evaluation Task
# ---------------------------------------------------------
pim_evaluation_task = Task(
    description=(
        "Given the identity risk assessment, Conditional Access decision, and "
        "privileged access review, evaluate how privileged access should be managed "
        "using PIM/PAM principles (e.g., Entra PIM and CyberArk-style controls).\n\n"
        "You have access to a CyberArk-style model of safes and platforms:\n"
        f"- Safes: {cyberark_safes}\n"
        f"- Platforms: {cyberark_platforms}\n\n"
        "Decide whether:\n"
        "- Privileged roles should be permanent or eligible\n"
        "- Access should be just-in-time and time-bound\n"
        "- Approval is required for elevation\n"
        "- Any existing standing privileges should be removed or reduced\n"
        "- Break-glass accounts are appropriate and how they should be controlled\n"
        "- Which safe and platform the account should be mapped to"
    ),
    expected_output=(
        "A PIM/PAM decision including:\n"
        "- Recommended model (permanent vs eligible vs JIT)\n"
        "- Recommended duration and conditions for elevation\n"
        "- Whether approval is required and by whom\n"
        "- Any roles or assignments that should be removed or reduced\n"
        "- Recommended CyberArk safe and platform mapping\n"
        "- How this maps to Entra PIM and CyberArk-style controls"
    ),
    agent=None,
)

# ---------------------------------------------------------
# 5. Governance & Guardrails Task
# ---------------------------------------------------------
governance_guardrails_task = Task(
    description=(
        "Review the full IAM decision pipeline, including:\n"
        "- Identity risk assessment\n"
        "- Conditional Access decision\n"
        "- Privileged access review\n\n"
        "Your job is to act as a governance and guardrails layer. "
        "Determine whether the overall outcome is acceptable under a strict Zero Trust "
        "security posture. If anything is too risky (e.g., high user risk, permanent "
        "Global Administrator role, untrusted location, lack of MFA), you must recommend "
        "a stricter action such as blocking access, revoking privileges, or triggering "
        "an incident response.\n\n"
        "Be conservative. Prefer security over convenience."
    ),
    expected_output=(
        "A governance decision including:\n"
        "- Overall governance verdict (Accept, Accept with conditions, Reject)\n"
        "- Key governance concerns\n"
        "- Required changes (e.g., block access, remove role, enforce MFA, require JIT)\n"
        "- Alignment with Zero Trust and organizational security policy"
    ),
    agent=None,
)

# ---------------------------------------------------------
# 6. Compliance & AI Governance Task
# ---------------------------------------------------------
compliance_ai_governance_task = Task(
    description=(
        "Review the full IAM pipeline output, including:\n"
        "- Identity risk assessment\n"
        "- Conditional Access decision\n"
        "- Privileged access review\n"
        "- Governance & guardrails verdict\n\n"
        "Evaluate how well these outcomes align with common security and AI governance "
        "frameworks such as NIST CSF, NIST AI RMF, ISO 27001, SOC 2, and Zero Trust "
        "principles. Identify any compliance or governance gaps and recommend concrete "
        "controls or process improvements.\n\n"
        "Assume this system may be used as part of an AI-assisted IAM decision engine."
    ),
    expected_output=(
        "A compliance and AI governance summary including:\n"
        "- Overall alignment (Well aligned / Partially aligned / Poorly aligned)\n"
        "- Key compliance and governance risks\n"
        "- Recommended controls or process changes\n"
        "- How this supports secure and responsible AI-assisted IAM"
    ),
    agent=None,
)
