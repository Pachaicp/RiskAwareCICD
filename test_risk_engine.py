from risk_engine import Release, analyze_release


def test_safe_release():
    release = Release(10, True, False, False, True)
    result = analyze_release(release)

    assert result["risk_level"] == "LOW"
    assert result["decision"] == "DEPLOY"


def test_medium_risk_requires_approval():
    release = Release(40, True, False, False, True)
    result = analyze_release(release)

    assert result["risk_level"] == "MEDIUM"
    assert result["decision"] == "REQUIRES_APPROVAL"


def test_breaking_database_change_is_blocked():
    release = Release(10, True, True, False, True)
    result = analyze_release(release)

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "BLOCK"


def test_failed_tests_block_release():
    release = Release(10, False, False, False, True)
    result = analyze_release(release)

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "BLOCK"


def test_failed_security_check_blocks_release():
    release = Release(10, True, False, False, False)
    result = analyze_release(release)

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "BLOCK"


def test_high_risk_release_is_blocked():
    release = Release(
        code_change_size=10,
        tests_passed=True,
        database_breaking_change=True,
        previous_deployment_failed=False,
        security_check_passed=True,
    )

    result = analyze_release(release)

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "BLOCK"
