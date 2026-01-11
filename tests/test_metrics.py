"""
Tests for YAP Metrics Service API endpoints

These tests verify that the metrics service is working correctly,
including configuration, event recording, summary, and history endpoints.
"""

import pytest
import requests
import os
import json
from datetime import datetime

# Determine base URL from environment or use default for local testing
METRICS_BASE_URL = os.getenv('METRICS_BASE_URL', 'http://localhost:8091')


class TestMetricsHealth:
    """Test metrics health endpoint"""

    def test_health_endpoint_returns_200(self):
        """Health endpoint should return 200 OK"""
        response = requests.get(f'{METRICS_BASE_URL}/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Health endpoint should return JSON with status"""
        response = requests.get(f'{METRICS_BASE_URL}/health')
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'ok'
        assert 'metrics_enabled' in data


class TestMetricsConfig:
    """Test metrics configuration endpoint"""

    def test_config_endpoint_returns_200(self):
        """Config endpoint should return 200 OK"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/config')
        assert response.status_code == 200

    def test_config_endpoint_returns_config_values(self):
        """Config endpoint should return configuration values"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/config')
        data = response.json()
        assert 'enabled' in data
        assert 'store_text' in data
        assert 'retention_days' in data
        assert 'max_events' in data


class TestMetricsEventRecording:
    """Test metrics event recording endpoint"""

    def test_record_asr_event(self):
        """Should successfully record an ASR event"""
        event = {
            "event_type": "asr_transcribe",
            "duration_seconds": 12.5,
            "input_chars": 0,
            "output_chars": 150,
            "status": "success"
        }
        
        response = requests.post(
            f'{METRICS_BASE_URL}/api/metrics/event',
            json=event,
            headers={'Content-Type': 'application/json'}
        )
        
        # May be 503 if metrics disabled, or 200 if enabled
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data
        assert data['event_type'] == 'asr_transcribe'
        assert data['duration_seconds'] == 12.5

    def test_record_tts_event(self):
        """Should successfully record a TTS event"""
        event = {
            "event_type": "tts_synthesize",
            "duration_seconds": 5.3,
            "input_chars": 100,
            "output_chars": 0,
            "status": "success"
        }
        
        response = requests.post(
            f'{METRICS_BASE_URL}/api/metrics/event',
            json=event,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert data['event_type'] == 'tts_synthesize'

    def test_record_event_with_metadata(self):
        """Should record event with metadata"""
        event = {
            "event_type": "asr_record",
            "duration_seconds": 30.0,
            "status": "success",
            "metadata": {"source": "test", "model": "whisper-tiny"}
        }
        
        response = requests.post(
            f'{METRICS_BASE_URL}/api/metrics/event',
            json=event,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert data['metadata'] is not None
        assert data['metadata']['source'] == 'test'

    def test_record_event_requires_event_type(self):
        """Should require event_type field"""
        event = {
            "duration_seconds": 10.0
        }
        
        response = requests.post(
            f'{METRICS_BASE_URL}/api/metrics/event',
            json=event,
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return 422 for validation error
        if response.status_code != 503:  # Not disabled
            assert response.status_code == 422


class TestMetricsSummary:
    """Test metrics summary endpoint"""

    def test_summary_endpoint_returns_200(self):
        """Summary endpoint should return 200 OK"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/summary')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200

    def test_summary_with_range_today(self):
        """Summary should accept today range"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/summary?range=today')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert data['range'] == 'today'

    def test_summary_with_range_7d(self):
        """Summary should accept 7d range"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/summary?range=7d')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert data['range'] == '7d'

    def test_summary_returns_expected_fields(self):
        """Summary should return expected statistic fields"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/summary')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        data = response.json()
        assert 'total_events' in data
        assert 'asr_events' in data
        assert 'tts_events' in data
        assert 'asr_seconds_recorded' in data
        assert 'tts_seconds_generated' in data


class TestMetricsHistory:
    """Test metrics history endpoint"""

    def test_history_endpoint_returns_200(self):
        """History endpoint should return 200 OK"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/history')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200

    def test_history_with_pagination(self):
        """History should support pagination"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/history?limit=10&offset=0')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert 'events' in data
        assert 'total' in data
        assert 'limit' in data
        assert 'offset' in data

    def test_history_filter_by_event_type(self):
        """History should support filtering by event type"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/history?event_type=asr_transcribe')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        # All events should be of the filtered type
        for event in data['events']:
            assert event['event_type'] == 'asr_transcribe'


class TestMetricsExport:
    """Test metrics export endpoint"""

    def test_export_endpoint_returns_200(self):
        """Export endpoint should return 200 OK"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/export')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200

    def test_export_returns_json_with_events(self):
        """Export should return JSON with events array"""
        response = requests.get(f'{METRICS_BASE_URL}/api/metrics/export')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        data = response.json()
        assert 'exported_at' in data
        assert 'total_events' in data
        assert 'events' in data
        assert isinstance(data['events'], list)


class TestMetricsClear:
    """Test metrics clear history endpoint"""

    def test_clear_history_endpoint(self):
        """Clear history endpoint should work"""
        response = requests.delete(f'{METRICS_BASE_URL}/api/metrics/history')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True

    def test_clear_text_only(self):
        """Should support clearing only stored text"""
        response = requests.delete(f'{METRICS_BASE_URL}/api/metrics/history?clear_text_only=true')
        
        if response.status_code == 503:
            pytest.skip("Metrics collection is disabled")
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        assert 'text' in data['message'].lower()
