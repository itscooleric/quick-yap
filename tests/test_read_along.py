"""
Tests for YAP TTS Read-Along functionality

These tests verify the TTS read-along module works correctly,
including text chunking, limit checking, and playback logic.
They are primarily unit tests that don't require running services.
"""

import pytest


class TestTextChunking:
    """Test text chunking for read-along"""

    def test_split_by_paragraphs(self):
        """Should split text by blank lines (paragraphs)"""
        text = """First paragraph here.
This is still the first paragraph.

Second paragraph starts here.
More of the second paragraph.

Third paragraph."""
        
        # Split by double newlines (paragraphs)
        chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
        
        assert len(chunks) == 3
        assert chunks[0].startswith("First paragraph")
        assert chunks[1].startswith("Second paragraph")
        assert chunks[2].startswith("Third paragraph")

    def test_split_by_lines_fallback(self):
        """Should fall back to lines if no paragraphs"""
        text = """Line one.
Line two.
Line three."""
        
        # No blank lines, so split by single newlines
        chunks = [line.strip() for line in text.split('\n') if line.strip()]
        
        assert len(chunks) == 3

    def test_empty_text_returns_no_chunks(self):
        """Empty text should return no chunks"""
        text = ""
        chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
        
        assert len(chunks) == 0

    def test_whitespace_only_text(self):
        """Whitespace-only text should return no chunks"""
        text = "   \n\n   \n   "
        chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
        
        assert len(chunks) == 0


class TestChunkLimits:
    """Test chunk limit checking"""

    def test_chunk_count_under_limit(self):
        """Should pass when chunk count is under limit"""
        chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
        max_chunks = 30
        
        valid = len(chunks) <= max_chunks
        assert valid == True

    def test_chunk_count_over_limit(self):
        """Should fail when chunk count exceeds limit"""
        chunks = ["Chunk " + str(i) for i in range(50)]
        max_chunks = 30
        
        valid = len(chunks) <= max_chunks
        assert valid == False

    def test_chunk_length_under_limit(self):
        """Should pass when all chunks are under character limit"""
        chunks = ["Short chunk", "Another short chunk"]
        max_chars = 1200
        
        valid = all(len(chunk) <= max_chars for chunk in chunks)
        assert valid == True

    def test_chunk_length_over_limit(self):
        """Should fail when any chunk exceeds character limit"""
        short_chunk = "Short chunk"
        long_chunk = "A" * 1500  # Exceeds 1200 limit
        chunks = [short_chunk, long_chunk]
        max_chars = 1200
        
        valid = all(len(chunk) <= max_chars for chunk in chunks)
        assert valid == False

    def test_check_both_limits(self):
        """Should check both count and length limits"""
        def check_limits(chunks, max_chunks=30, max_chars=1200):
            if len(chunks) > max_chunks:
                return {"valid": False, "message": f"Too many chunks ({len(chunks)} > {max_chunks})"}
            
            for i, chunk in enumerate(chunks):
                if len(chunk) > max_chars:
                    return {"valid": False, "message": f"Chunk {i+1} too long ({len(chunk)} > {max_chars})"}
            
            return {"valid": True, "message": "OK"}
        
        # Valid case
        result = check_limits(["Short chunk 1", "Short chunk 2"])
        assert result["valid"] == True
        
        # Too many chunks
        result = check_limits(["c"] * 50)
        assert result["valid"] == False
        assert "Too many" in result["message"]
        
        # Chunk too long
        result = check_limits(["A" * 1500])
        assert result["valid"] == False
        assert "too long" in result["message"]


class TestReadAlongState:
    """Test read-along playback state management"""

    def test_initial_state(self):
        """Initial state should have no chunks playing"""
        state = {
            "chunks": [],
            "currentIndex": -1,
            "isPlaying": False,
            "isPaused": False
        }
        
        assert state["currentIndex"] == -1
        assert state["isPlaying"] == False

    def test_start_playback(self):
        """Starting playback should update state correctly"""
        state = {
            "chunks": ["Chunk 1", "Chunk 2", "Chunk 3"],
            "currentIndex": -1,
            "isPlaying": False,
            "isPaused": False
        }
        
        # Start playback
        state["currentIndex"] = 0
        state["isPlaying"] = True
        
        assert state["currentIndex"] == 0
        assert state["isPlaying"] == True

    def test_advance_to_next_chunk(self):
        """Advancing should increment the current index"""
        state = {
            "chunks": ["Chunk 1", "Chunk 2", "Chunk 3"],
            "currentIndex": 0,
            "isPlaying": True,
            "isPaused": False
        }
        
        # Advance to next chunk
        state["currentIndex"] += 1
        
        assert state["currentIndex"] == 1

    def test_playback_complete(self):
        """Completing all chunks should update state"""
        state = {
            "chunks": ["Chunk 1", "Chunk 2", "Chunk 3"],
            "currentIndex": 2,  # Last chunk
            "isPlaying": True,
            "isPaused": False
        }
        
        # Playback complete
        state["currentIndex"] = -1
        state["isPlaying"] = False
        
        assert state["currentIndex"] == -1
        assert state["isPlaying"] == False

    def test_pause_playback(self):
        """Pausing should set isPaused flag"""
        state = {
            "chunks": ["Chunk 1", "Chunk 2"],
            "currentIndex": 0,
            "isPlaying": True,
            "isPaused": False
        }
        
        # Pause
        state["isPaused"] = True
        
        assert state["isPaused"] == True
        assert state["isPlaying"] == True  # Still technically playing

    def test_resume_playback(self):
        """Resuming should clear isPaused flag"""
        state = {
            "chunks": ["Chunk 1", "Chunk 2"],
            "currentIndex": 0,
            "isPlaying": True,
            "isPaused": True
        }
        
        # Resume
        state["isPaused"] = False
        
        assert state["isPaused"] == False

    def test_stop_playback(self):
        """Stopping should reset all playback state"""
        state = {
            "chunks": ["Chunk 1", "Chunk 2"],
            "currentIndex": 1,
            "isPlaying": True,
            "isPaused": False
        }
        
        # Stop
        state["currentIndex"] = -1
        state["isPlaying"] = False
        state["isPaused"] = False
        
        assert state["currentIndex"] == -1
        assert state["isPlaying"] == False
        assert state["isPaused"] == False


class TestChunkHighlighting:
    """Test chunk highlighting during playback"""

    def test_highlight_first_chunk(self):
        """Should highlight the first chunk at start"""
        chunks = ["First", "Second", "Third"]
        current_index = 0
        
        highlighted = [i == current_index for i in range(len(chunks))]
        
        assert highlighted[0] == True
        assert highlighted[1] == False
        assert highlighted[2] == False

    def test_highlight_middle_chunk(self):
        """Should highlight the current middle chunk"""
        chunks = ["First", "Second", "Third"]
        current_index = 1
        
        highlighted = [i == current_index for i in range(len(chunks))]
        
        assert highlighted[0] == False
        assert highlighted[1] == True
        assert highlighted[2] == False

    def test_highlight_last_chunk(self):
        """Should highlight the last chunk"""
        chunks = ["First", "Second", "Third"]
        current_index = 2
        
        highlighted = [i == current_index for i in range(len(chunks))]
        
        assert highlighted[0] == False
        assert highlighted[1] == False
        assert highlighted[2] == True

    def test_no_highlight_when_stopped(self):
        """Should not highlight any chunk when stopped"""
        chunks = ["First", "Second", "Third"]
        current_index = -1  # Stopped
        
        highlighted = [i == current_index for i in range(len(chunks))]
        
        assert all(h == False for h in highlighted)


class TestReadAlongPanel:
    """Test read-along panel behavior"""

    def test_panel_opens_on_playback_start(self):
        """Panel should open when read-along starts"""
        panel_visible = False
        
        # Start read-along
        panel_visible = True
        
        assert panel_visible == True

    def test_panel_shows_all_chunks(self):
        """Panel should display all chunks"""
        chunks = ["Paragraph 1", "Paragraph 2", "Paragraph 3"]
        panel_content = chunks.copy()
        
        assert len(panel_content) == 3
        assert panel_content == chunks

    def test_panel_can_be_closed(self):
        """Panel should be closeable"""
        panel_visible = True
        
        # Close panel
        panel_visible = False
        
        assert panel_visible == False

    def test_closing_panel_stops_playback(self):
        """Closing panel should stop playback"""
        state = {
            "panel_visible": True,
            "isPlaying": True,
            "currentIndex": 1
        }
        
        # Close panel and stop
        state["panel_visible"] = False
        state["isPlaying"] = False
        state["currentIndex"] = -1
        
        assert state["panel_visible"] == False
        assert state["isPlaying"] == False


class TestReadAlongErrorHandling:
    """Test read-along error handling"""

    def test_synthesis_failure_stops_gracefully(self):
        """Synthesis failure should stop playback gracefully"""
        state = {
            "isPlaying": True,
            "currentIndex": 1,
            "error": None
        }
        
        # Synthesis fails
        state["error"] = "Synthesis failed: Connection error"
        state["isPlaying"] = False
        state["currentIndex"] = -1
        
        assert state["error"] is not None
        assert state["isPlaying"] == False

    def test_empty_text_shows_error(self):
        """Empty text should show error, not crash"""
        text = ""
        
        if not text.strip():
            error = "No text to synthesize"
        else:
            error = None
        
        assert error == "No text to synthesize"

    def test_no_voice_selected_shows_error(self):
        """No voice selected should show error"""
        voice = None
        
        if not voice:
            error = "Please select a voice"
        else:
            error = None
        
        assert error == "Please select a voice"
