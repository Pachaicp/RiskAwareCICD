
from dataclasses import dataclass, asdict


@dataclass
class Release:
    code_change_size: int
    tests_passed: bool
    database_breaking_change: bool
    previous_deployment_failed: bool
    security_check_passed: bool


def analyze_release(release: Release) -> dict:
    risk_score = 0
    reasons = []

    # Mandatory safety checks
    if not release.tests_passed:
        reasons.append("Automated tests failed")

    if not release.security_check_passed:
        reasons.append("Security check failed")

    # Risk scoring
    if release.code_change_size > 100:
        risk_score += 30
        reasons.append("Large code change")
    elif release.code_change_size > 30:
        risk_score += 15
        reasons.append("Medium-sized code change")

    if release.database_breaking_change:
        risk_score += 40
        reasons.append("Breaking database change detected")

    if release.previous_deployment_failed:
        risk_score += 20
        reasons.append("Previous deployment failed")

    # Failed mandatory checks always block deployment
    if not release.tests_passed or not release.security_check_passed:
        risk_level = "HIGH"
        decision = "BLOCK"
    elif risk_score >= 40:
        risk_level = "HIGH"
        decision = "BLOCK"
    elif risk_score >= 15:
        risk_level = "MEDIUM"
        decision = "REQUIRES_APPROVAL"
    else:
        risk_level = "LOW"
        decision = "DEPLOY"

    if not reasons:
        reasons.append("No configured risk factors detected")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
    }


if __name__ == "__main__":
    example = Release(
        code_change_size=10,
        tests_passed=True,
        database_breaking_change=False,
        previous_deployment_failed=False,
        security_check_passed=True,
    )

    print(analyze_release(example))
