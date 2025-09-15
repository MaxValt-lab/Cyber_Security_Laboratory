from risk_engine import RiskEngine

def test_risk_assessment():
    engine = RiskEngine("risk_policy.json")
    event = {
        "type": "unauthorized_access",
        "source": "external",
        "severity": "high"
    }
    report = engine.assess_event(event)
    assert report["risk_score"] == 75
    assert "unauthorized_access" in report["tags"]
    assert "external" in report["tags"]
    assert "high" in report["tags"]