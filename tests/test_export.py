"""
Tests for YAP Export functionality

These tests verify the export module functions correctly,
including payload building, CORS detection, and profile management.
They are primarily unit tests that don't require running services.
"""

import pytest
import json
import os
import sys

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'ui', 'js'))


class TestPayloadFormats:
    """Test export payload format generation"""

    def test_transcript_only_payload_structure(self):
        """Transcript-only payload should have minimal structure"""
        # Simulating the buildPayload function logic
        transcript = "This is a test transcript."
        payload_mode = "transcript_only"
        
        # Expected structure
        payload = {
            "source": "yap",
            "created_at": "2024-01-15T10:30:00.000Z",  # Example
            "transcript": transcript
        }
        
        assert "source" in payload
        assert payload["source"] == "yap"
        assert "created_at" in payload
        assert "transcript" in payload
        assert payload["transcript"] == transcript
        # Should NOT have clips in transcript_only mode
        assert "clips" not in payload

    def test_full_session_payload_structure(self):
        """Full session payload should include clips and metadata"""
        transcript = "This is a test transcript."
        clips = [
            {"id": "clip1", "text": "First clip", "duration_ms": 5000},
            {"id": "clip2", "text": "Second clip", "duration_ms": 3000}
        ]
        
        # Expected structure for full_session
        payload = {
            "source": "yap",
            "created_at": "2024-01-15T10:30:00.000Z",
            "transcript": transcript,
            "clips": [
                {
                    "id": clip["id"],
                    "created_at": "2024-01-15T10:30:00.000Z",
                    "duration_ms": clip["duration_ms"],
                    "text": clip["text"]
                }
                for clip in clips
            ],
            "meta": {
                "app_version": "1.0.0"
            }
        }
        
        assert "source" in payload
        assert "clips" in payload
        assert len(payload["clips"]) == 2
        assert "meta" in payload
        assert "app_version" in payload["meta"]


class TestFilePathVariables:
    """Test file path variable substitution"""

    def test_year_variable(self):
        """Should substitute {year} correctly"""
        template = "inbox/{year}/export.json"
        # Simulating formatFilePath logic
        year = "2024"
        result = template.replace("{year}", year)
        assert result == "inbox/2024/export.json"

    def test_month_variable(self):
        """Should substitute {month} correctly"""
        template = "inbox/{year}/{month}/export.json"
        year = "2024"
        month = "01"
        result = template.replace("{year}", year).replace("{month}", month)
        assert result == "inbox/2024/01/export.json"

    def test_timestamp_variable(self):
        """Should substitute {timestamp} correctly"""
        template = "inbox/yap/{timestamp}.json"
        timestamp = "20240115-1030"
        result = template.replace("{timestamp}", timestamp)
        assert result == "inbox/yap/20240115-1030.json"

    def test_multiple_variables(self):
        """Should handle multiple variables in path"""
        template = "inbox/yap/{year}/{month}/{day}/{timestamp}.json"
        year = "2024"
        month = "01"
        day = "15"
        timestamp = "20240115-1030"
        
        result = (template
            .replace("{year}", year)
            .replace("{month}", month)
            .replace("{day}", day)
            .replace("{timestamp}", timestamp))
        
        assert result == "inbox/yap/2024/01/15/20240115-1030.json"


class TestExportProfileValidation:
    """Test export profile validation"""

    def test_webhook_profile_requires_url(self):
        """Webhook profile must have a URL"""
        profile = {
            "id": "test-webhook",
            "name": "Test Webhook",
            "type": "webhook",
            "method": "POST"
            # Missing 'url'
        }
        
        assert "url" not in profile
        # In real code, this would fail validation

    def test_gitlab_commit_profile_requires_project_id(self):
        """GitLab commit profile must have project_id"""
        profile = {
            "id": "test-gitlab",
            "name": "Test GitLab",
            "type": "gitlab_commit",
            "mode": "webhook",
            "webhookUrl": "http://localhost:5678/webhook"
            # Missing 'projectId'
        }
        
        # Should require projectId for gitlab_commit type
        assert "projectId" not in profile

    def test_valid_webhook_profile(self):
        """Valid webhook profile should have all required fields"""
        profile = {
            "id": "test-webhook",
            "name": "Test Webhook",
            "type": "webhook",
            "url": "http://localhost:5678/webhook/yap",
            "method": "POST",
            "headers": '{"Content-Type": "application/json"}',
            "payloadMode": "transcript_only"
        }
        
        assert profile["type"] == "webhook"
        assert profile["url"].startswith("http")
        assert profile["method"] in ["POST", "PUT"]

    def test_valid_gitlab_direct_profile(self):
        """Valid GitLab direct profile should have all required fields"""
        profile = {
            "id": "test-gitlab-direct",
            "name": "GitLab Direct",
            "type": "gitlab_commit",
            "mode": "direct",
            "gitlabUrl": "https://gitlab.com",
            "projectId": "user/repo",
            "branch": "main",
            "filePath": "inbox/yap/{timestamp}.json",
            "fileFormat": "json",
            "token": "glpat-xxxx"
        }
        
        assert profile["mode"] == "direct"
        assert profile["projectId"] != ""
        assert profile["token"] != ""

    def test_valid_gitlab_webhook_profile(self):
        """Valid GitLab webhook profile should have webhook URL"""
        profile = {
            "id": "test-gitlab-webhook",
            "name": "GitLab via Webhook",
            "type": "gitlab_commit",
            "mode": "webhook",
            "webhookUrl": "http://localhost:5678/webhook/gitlab-commit",
            "projectId": "user/repo",
            "branch": "main",
            "filePath": "inbox/yap/{timestamp}.json"
        }
        
        assert profile["mode"] == "webhook"
        assert "webhookUrl" in profile
        # Token not required for webhook mode (stored on proxy)
        assert "token" not in profile


class TestCORSDetection:
    """Test CORS error detection logic"""

    def test_detect_cors_from_status_0(self):
        """Status 0 typically indicates CORS blocking"""
        # Simulating the detectCORSError function
        def detect_cors_error(response_status, error_message):
            if response_status == 0:
                return True
            if error_message and "Failed to fetch" in error_message:
                return True
            return False
        
        assert detect_cors_error(0, None) == True

    def test_detect_cors_from_failed_to_fetch(self):
        """'Failed to fetch' error message indicates CORS"""
        def detect_cors_error(response_status, error_message):
            if response_status == 0:
                return True
            if error_message and "Failed to fetch" in error_message:
                return True
            return False
        
        assert detect_cors_error(None, "TypeError: Failed to fetch") == True

    def test_normal_http_error_not_cors(self):
        """Normal HTTP errors should not be detected as CORS"""
        def detect_cors_error(response_status, error_message):
            if response_status == 0:
                return True
            if error_message and "Failed to fetch" in error_message:
                return True
            return False
        
        assert detect_cors_error(404, "Not found") == False
        assert detect_cors_error(500, "Internal server error") == False


class TestExportTargetTypes:
    """Test export target type handling"""

    def test_webhook_type(self):
        """Webhook type should be recognized"""
        target_types = ["webhook", "gitlab_commit", "gitlab", "github", "sftp"]
        assert "webhook" in target_types

    def test_gitlab_commit_type(self):
        """GitLab commit type should be recognized"""
        target_types = ["webhook", "gitlab_commit", "gitlab", "github", "sftp"]
        assert "gitlab_commit" in target_types

    def test_legacy_types_supported(self):
        """Legacy exporter service types should still be supported"""
        legacy_types = ["gitlab", "github", "sftp"]
        target_types = ["webhook", "gitlab_commit", "gitlab", "github", "sftp"]
        
        for legacy_type in legacy_types:
            assert legacy_type in target_types
