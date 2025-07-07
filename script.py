import json
import pandas as pd

# Create a comprehensive Wazuh to OCSF field mapping table
wazuh_ocsf_mapping = {
    "Wazuh Field": [
        "rule.id", "rule.level", "rule.description", "rule.mitre.id", "rule.mitre.tactic",
        "agent.id", "agent.name", "agent.ip", "location", "decoder.name",
        "timestamp", "full_log", "data.srcip", "data.dstip", "data.srcport",
        "data.dstport", "data.protocol", "data.action", "data.srcuser", "data.command",
        "syscheck.path", "syscheck.size_after", "syscheck.perm_after", "syscheck.uid_after", "syscheck.event"
    ],
    "OCSF Field": [
        "finding.uid", "severity_id", "message", "finding.related_events[].uid", "finding.attack[].tactic.name",
        "device.uid", "device.name", "device.ip", "metadata.product.feature.name", "metadata.log_name",
        "time", "raw_data", "src_endpoint.ip", "dst_endpoint.ip", "src_endpoint.port",
        "dst_endpoint.port", "connection_info.protocol_name", "action_id", "actor.user.name", "process.cmd_line",
        "file.path", "file.size", "file.attributes", "file.owner.uid", "activity_id"
    ],
    "OCSF Event Class": [
        "Detection Finding (2004)", "Base Event", "Base Event", "Detection Finding (2004)", "Detection Finding (2004)",
        "Base Event", "Base Event", "Base Event", "Base Event", "Base Event",
        "Base Event", "Base Event", "Network Activity (4001)", "Network Activity (4001)", "Network Activity (4001)",
        "Network Activity (4001)", "Network Activity (4001)", "Base Event", "Authentication (3002)", "Process Activity (1007)",
        "File System Activity (1001)", "File System Activity (1001)", "File System Activity (1001)", "File System Activity (1001)", "File System Activity (1001)"
    ],
    "Data Type": [
        "String", "Integer (1-6)", "String", "String", "String",
        "String", "String", "String", "String", "String",
        "Timestamp", "String", "String", "String", "Integer",
        "Integer", "String", "Integer (1-6)", "String", "String",
        "String", "Integer", "String", "String", "Integer (1-7)"
    ],
    "Required": [
        "Yes", "Yes", "No", "No", "No",
        "Yes", "No", "No", "No", "No",
        "Yes", "No", "No", "No", "No",
        "No", "No", "Yes", "No", "No",
        "Yes", "No", "No", "No", "Yes"
    ]
}

# Create DataFrame and save to CSV
mapping_df = pd.DataFrame(wazuh_ocsf_mapping)
mapping_df.to_csv('wazuh_ocsf_field_mapping.csv', index=False)

print("Wazuh to OCSF Field Mapping Table:")
print("=" * 60)
print(mapping_df.to_string(index=False))
print(f"\nTotal mappings: {len(mapping_df)}")
print(f"CSV file saved: wazuh_ocsf_field_mapping.csv")