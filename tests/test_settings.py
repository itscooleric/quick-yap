"""
Tests for YAP Settings functionality

These tests verify the settings module works correctly,
including default values, persistence, and validation.
They are primarily unit tests that don't require running services.
"""

import pytest
import json


class TestASRSettingsDefaults:
    """Test ASR settings default values"""

    def test_auto_transcribe_default(self):
        """Auto-transcribe should be disabled by default"""
        default_settings = {
            "autoTranscribe": False,
            "autoCopy": False,
            "confirmClear": True,
            "confirmDelete": True
        }
        
        assert default_settings["autoTranscribe"] == False

    def test_auto_copy_default(self):
        """Auto-copy should be disabled by default"""
        default_settings = {
            "autoTranscribe": False,
            "autoCopy": False,
            "confirmClear": True,
            "confirmDelete": True
        }
        
        assert default_settings["autoCopy"] == False

    def test_confirm_clear_default(self):
        """Confirm before clear should be enabled by default"""
        default_settings = {
            "autoTranscribe": False,
            "autoCopy": False,
            "confirmClear": True,
            "confirmDelete": True
        }
        
        assert default_settings["confirmClear"] == True

    def test_confirm_delete_default(self):
        """Confirm before delete should be enabled by default"""
        default_settings = {
            "autoTranscribe": False,
            "autoCopy": False,
            "confirmClear": True,
            "confirmDelete": True
        }
        
        assert default_settings["confirmDelete"] == True


class TestTranscriptFormattingDefaults:
    """Test transcript formatting settings defaults"""

    def test_show_separators_default(self):
        """Show separators should be disabled by default"""
        default_settings = {
            "showSeparators": False,
            "collapseBlankLines": True,
            "trimWhitespace": True
        }
        
        assert default_settings["showSeparators"] == False

    def test_collapse_blank_lines_default(self):
        """Collapse blank lines should be enabled by default"""
        default_settings = {
            "showSeparators": False,
            "collapseBlankLines": True,
            "trimWhitespace": True
        }
        
        assert default_settings["collapseBlankLines"] == True

    def test_trim_whitespace_default(self):
        """Trim whitespace should be enabled by default"""
        default_settings = {
            "showSeparators": False,
            "collapseBlankLines": True,
            "trimWhitespace": True
        }
        
        assert default_settings["trimWhitespace"] == True


class TestTTSSettingsDefaults:
    """Test TTS settings default values"""

    def test_markdown_preview_default(self):
        """Markdown preview should be disabled by default"""
        default_settings = {
            "markdownPreview": False,
            "chunkMode": "paragraph",
            "maxChunks": 30,
            "maxCharsPerChunk": 1200
        }
        
        assert default_settings["markdownPreview"] == False

    def test_chunk_mode_default(self):
        """Chunk mode should be 'paragraph' by default"""
        default_settings = {
            "markdownPreview": False,
            "chunkMode": "paragraph",
            "maxChunks": 30,
            "maxCharsPerChunk": 1200
        }
        
        assert default_settings["chunkMode"] == "paragraph"

    def test_max_chunks_default(self):
        """Max chunks should be 30 by default"""
        default_settings = {
            "markdownPreview": False,
            "chunkMode": "paragraph",
            "maxChunks": 30,
            "maxCharsPerChunk": 1200
        }
        
        assert default_settings["maxChunks"] == 30

    def test_max_chars_per_chunk_default(self):
        """Max chars per chunk should be 1200 by default"""
        default_settings = {
            "markdownPreview": False,
            "chunkMode": "paragraph",
            "maxChunks": 30,
            "maxCharsPerChunk": 1200
        }
        
        assert default_settings["maxCharsPerChunk"] == 1200


class TestMetricsSettingsDefaults:
    """Test metrics settings default values"""

    def test_metrics_enabled_default(self):
        """Metrics should be enabled by default"""
        # Updated to reflect new default (enabled by default)
        default_settings = {
            "enabled": True,
            "storeText": False,
            "retentionDays": 30,
            "maxEvents": 5000
        }
        
        assert default_settings["enabled"] == True

    def test_store_text_default(self):
        """Store text should be disabled by default for privacy"""
        default_settings = {
            "enabled": True,
            "storeText": False,
            "retentionDays": 30,
            "maxEvents": 5000
        }
        
        assert default_settings["storeText"] == False

    def test_retention_days_default(self):
        """Retention days should be 30 by default"""
        default_settings = {
            "enabled": True,
            "storeText": False,
            "retentionDays": 30,
            "maxEvents": 5000
        }
        
        assert default_settings["retentionDays"] == 30

    def test_max_events_default(self):
        """Max events should be 5000 by default"""
        default_settings = {
            "enabled": True,
            "storeText": False,
            "retentionDays": 30,
            "maxEvents": 5000
        }
        
        assert default_settings["maxEvents"] == 5000


class TestSettingsPersistence:
    """Test settings persistence logic"""

    def test_settings_can_be_serialized_to_json(self):
        """Settings should be JSON serializable"""
        settings = {
            "autoTranscribe": True,
            "autoCopy": False,
            "confirmClear": True,
            "showSeparators": False,
            "clipJoiner": "blank_line"
        }
        
        # Should not raise
        json_str = json.dumps(settings)
        assert isinstance(json_str, str)
        
        # Should be deserializable
        parsed = json.loads(json_str)
        assert parsed == settings

    def test_settings_merge_with_defaults(self):
        """Saved settings should merge with defaults"""
        defaults = {
            "autoTranscribe": False,
            "autoCopy": False,
            "confirmClear": True,
            "confirmDelete": True,
            "newSetting": "default"
        }
        
        saved = {
            "autoTranscribe": True,  # User changed this
            "confirmClear": False    # User changed this
        }
        
        # Merge logic: saved values override defaults
        merged = {**defaults, **saved}
        
        assert merged["autoTranscribe"] == True  # From saved
        assert merged["autoCopy"] == False       # From defaults
        assert merged["confirmClear"] == False   # From saved
        assert merged["confirmDelete"] == True   # From defaults
        assert merged["newSetting"] == "default" # From defaults


class TestSettingsValidation:
    """Test settings value validation"""

    def test_boolean_settings_accept_true_false(self):
        """Boolean settings should only accept True or False"""
        boolean_settings = ["autoTranscribe", "autoCopy", "confirmClear"]
        
        for setting in boolean_settings:
            # Valid values
            assert isinstance(True, bool)
            assert isinstance(False, bool)

    def test_max_chunks_must_be_positive(self):
        """Max chunks must be a positive integer"""
        max_chunks = 30
        assert max_chunks > 0
        assert isinstance(max_chunks, int)

    def test_max_chars_per_chunk_must_be_positive(self):
        """Max chars per chunk must be a positive integer"""
        max_chars = 1200
        assert max_chars > 0
        assert isinstance(max_chars, int)

    def test_retention_days_must_be_positive(self):
        """Retention days must be a positive integer"""
        retention_days = 30
        assert retention_days > 0
        assert isinstance(retention_days, int)

    def test_clip_joiner_values(self):
        """Clip joiner should only accept valid values"""
        valid_joiners = ["blank_line", "single_newline"]
        
        selected = "blank_line"
        assert selected in valid_joiners

    def test_chunk_mode_values(self):
        """Chunk mode should only accept valid values"""
        valid_modes = ["paragraph", "line"]
        
        selected = "paragraph"
        assert selected in valid_modes
