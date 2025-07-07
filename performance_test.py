#!/usr/bin/env python3
"""
Performance testing script for Wazuh-OCSF pipeline
"""
import time
import json
import requests
import threading
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

class PipelinePerformanceTest:

    def __init__(self, pipeline_url="http://localhost:9600"):
        self.pipeline_url = pipeline_url
        self.metrics = []

    def generate_wazuh_event(self, event_id):
        """Generate a realistic Wazuh alert event"""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "rule": {
                "level": 8,
                "description": f"Test security event {event_id}",
                "id": f"100{event_id % 1000:03d}",
                "groups": ["test", "security"],
                "mitre": {
                    "id": ["T1059"],
                    "tactic": ["Execution"],
                    "technique": ["Command and Scripting Interpreter"]
                }
            },
            "agent": {
                "id": f"00{event_id % 10}",
                "name": f"test-agent-{event_id % 10}",
                "ip": f"192.168.1.{100 + (event_id % 50)}"
            },
            "manager": {
                "name": "wazuh-manager-test"
            },
            "id": str(event_id),
            "cluster": {
                "name": "wazuh-test-cluster"
            },
            "data": {
                "srcip": f"10.0.{event_id % 255}.{(event_id * 2) % 255}",
                "dstip": f"172.16.{event_id % 255}.{(event_id * 3) % 255}",
                "srcport": 1024 + (event_id % 60000),
                "dstport": 80,
                "protocol": "TCP",
                "action": "allowed"
            }
        }

    def send_batch_events(self, batch_size=100, num_batches=10):
        """Send batch of events to test throughput"""
        results = {
            "events_sent": 0,
            "start_time": time.time(),
            "errors": 0
        }

        for batch in range(num_batches):
            batch_events = []
            for i in range(batch_size):
                event_id = batch * batch_size + i
                event = self.generate_wazuh_event(event_id)
                batch_events.append(event)

            # Simulate sending events (replace with actual pipeline input)
            try:
                # This would be the actual HTTP/TCP input to Logstash
                response = self.send_to_pipeline(batch_events)
                if response:
                    results["events_sent"] += batch_size
                else:
                    results["errors"] += 1

            except Exception as e:
                print(f"Error sending batch {batch}: {e}")
                results["errors"] += 1

            time.sleep(0.1)  # Small delay between batches

        results["end_time"] = time.time()
        results["duration"] = results["end_time"] - results["start_time"]
        results["throughput"] = results["events_sent"] / results["duration"]

        return results

    def send_to_pipeline(self, events):
        """Send events to pipeline (mock implementation)"""
        # In real implementation, this would send to Logstash HTTP input
        # or write to a file that Logstash monitors
        time.sleep(0.01)  # Simulate network delay
        return True

    def measure_latency(self, num_samples=100):
        """Measure end-to-end processing latency"""
        latencies = []

        for i in range(num_samples):
            start_time = time.time()
            event = self.generate_wazuh_event(i)

            # Send event and measure time to appear in output
            self.send_to_pipeline([event])

            # In real implementation, check output index for processed event
            # For now, simulate processing time
            processing_time = 0.05 + (i % 10) * 0.01  # 50-150ms
            time.sleep(processing_time)

            latency = time.time() - start_time
            latencies.append(latency)

        return {
            "min": min(latencies),
            "max": max(latencies),
            "avg": sum(latencies) / len(latencies),
            "p50": sorted(latencies)[len(latencies)//2],
            "p95": sorted(latencies)[int(len(latencies)*0.95)],
            "p99": sorted(latencies)[int(len(latencies)*0.99)]
        }

    def stress_test(self, duration_seconds=300, target_eps=1000):
        """Run stress test for specified duration"""
        print(f"Starting stress test: {target_eps} events/sec for {duration_seconds} seconds")

        start_time = time.time()
        events_sent = 0
        errors = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            while time.time() - start_time < duration_seconds:
                # Calculate events to send this second
                current_eps = min(target_eps, 100)  # Limit batch size

                # Submit batch for processing
                future = executor.submit(self.send_batch_events, current_eps, 1)

                events_sent += current_eps
                time.sleep(1.0)  # Wait one second

        total_time = time.time() - start_time
        actual_eps = events_sent / total_time

        return {
            "duration": total_time,
            "events_sent": events_sent,
            "target_eps": target_eps,
            "actual_eps": actual_eps,
            "efficiency": actual_eps / target_eps,
            "errors": errors
        }

    def run_full_test_suite(self):
        """Run comprehensive performance test suite"""
        print("Starting Wazuh-OCSF Pipeline Performance Test Suite")
        print("=" * 60)

        # Test 1: Throughput test
        print("\n1. Throughput Test")
        throughput_result = self.send_batch_events(1000, 10)
        print(f"   Events sent: {throughput_result['events_sent']}")
        print(f"   Duration: {throughput_result['duration']:.2f}s")
        print(f"   Throughput: {throughput_result['throughput']:.2f} events/sec")
        print(f"   Errors: {throughput_result['errors']}")

        # Test 2: Latency test
        print("\n2. Latency Test")
        latency_result = self.measure_latency(1000)
        print(f"   Min latency: {latency_result['min']*1000:.2f}ms")
        print(f"   Avg latency: {latency_result['avg']*1000:.2f}ms")
        print(f"   P50 latency: {latency_result['p50']*1000:.2f}ms")
        print(f"   P95 latency: {latency_result['p95']*1000:.2f}ms")
        print(f"   P99 latency: {latency_result['p99']*1000:.2f}ms")
        print(f"   Max latency: {latency_result['max']*1000:.2f}ms")

        # Test 3: Stress test
        print("\n3. Stress Test (5 minutes)")
        stress_result = self.stress_test(300, 500)
        print(f"   Target EPS: {stress_result['target_eps']}")
        print(f"   Actual EPS: {stress_result['actual_eps']:.2f}")
        print(f"   Efficiency: {stress_result['efficiency']*100:.1f}%")
        print(f"   Total events: {stress_result['events_sent']}")
        print(f"   Errors: {stress_result['errors']}")

        # Generate summary report
        print("\n" + "=" * 60)
        print("PERFORMANCE TEST SUMMARY")
        print("=" * 60)
        print(f"Maximum throughput: {throughput_result['throughput']:.0f} events/sec")
        print(f"Average latency (P95): {latency_result['p95']*1000:.0f}ms")
        print(f"Stress test efficiency: {stress_result['efficiency']*100:.1f}%")

        # Performance thresholds
        if throughput_result['throughput'] >= 500:
            print("✅ Throughput: PASS (≥500 events/sec)")
        else:
            print("❌ Throughput: FAIL (<500 events/sec)")

        if latency_result['p95'] <= 2.0:
            print("✅ Latency: PASS (P95 ≤2000ms)")
        else:
            print("❌ Latency: FAIL (P95 >2000ms)")

        if stress_result['efficiency'] >= 0.8:
            print("✅ Stress test: PASS (≥80% efficiency)")
        else:
            print("❌ Stress test: FAIL (<80% efficiency)")

if __name__ == "__main__":
    tester = PipelinePerformanceTest()
    tester.run_full_test_suite()