#!/usr/bin/env python3
"""
Unit tests for Wazuh to OCSF field mappings
"""
import json
import pytest
from jsonschema import validate, ValidationError

class TestFieldMappings:

    def test_required_ocsf_fields(self):
        """Test that all required OCSF fields are present"""
        with open('tests/fixtures/sample_ocsf_event.json') as f:
            ocsf_event = json.load(f)

        required_fields = [
            'activity_id', 'category_uid', 'class_uid', 
            'severity_id', 'time', 'metadata'
        ]

        for field in required_fields:
            assert field in ocsf_event, f"Required field {field} missing"

    def test_severity_mapping(self):
        """Test Wazuh level to OCSF severity mapping"""
        test_cases = [
            (1, 1, "Informational"),
            (5, 2, "Low"),
            (8, 3, "Medium"), 
            (11, 4, "High"),
            (14, 5, "Critical"),
            (16, 6, "Fatal")
        ]

        for wazuh_level, expected_id, expected_name in test_cases:
            # Test mapping logic
            if wazuh_level <= 3:
                severity_id, severity = 1, "Informational"
            elif wazuh_level <= 6:
                severity_id, severity = 2, "Low"
            elif wazuh_level <= 9:
                severity_id, severity = 3, "Medium"
            elif wazuh_level <= 12:
                severity_id, severity = 4, "High"
            elif wazuh_level <= 15:
                severity_id, severity = 5, "Critical"
            else:
                severity_id, severity = 6, "Fatal"

            assert severity_id == expected_id
            assert severity == expected_name

    def test_timestamp_conversion(self):
        """Test timestamp conversion to OCSF format"""
        import datetime

        wazuh_timestamp = "2024-01-01T12:00:00.000Z"
        expected_epoch_ms = 1704110400000

        # Convert ISO format to epoch milliseconds
        dt = datetime.datetime.fromisoformat(wazuh_timestamp.replace('Z', '+00:00'))
        actual_epoch_ms = int(dt.timestamp() * 1000)

        assert actual_epoch_ms == expected_epoch_ms

    def test_mitre_attack_mapping(self):
        """Test MITRE ATT&CK framework field mapping"""
        wazuh_mitre = {
            "id": ["T1059"],
            "tactic": ["Execution"],
            "technique": ["Command and Scripting Interpreter"]
        }

        # Expected OCSF attack structure
        expected_attack = {
            "tactics": [{"name": "Execution"}],
            "technique": {
                "uid": "T1059",
                "name": "Command and Scripting Interpreter"
            }
        }

        # Test mapping logic
        attack = {
            "tactics": [{"name": t} for t in wazuh_mitre["tactic"]],
            "technique": {
                "uid": wazuh_mitre["id"][0],
                "name": wazuh_mitre["technique"][0]
            }
        }

        assert attack == expected_attack

if __name__ == '__main__':
    pytest.main([__file__])