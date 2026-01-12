# YAP User Guide

Complete guide to using the YAP web interface for speech-to-text and text-to-speech tasks.

## Table of Contents

- [Quick Start](#quick-start)
- [ASR Tab - Speech to Text](#asr-tab---speech-to-text)
- [TTS Tab - Text to Speech](#tts-tab---text-to-speech)
- [Export Tab](#export-tab)
- [Data Tab](#data-tab)
- [Settings](#settings)
- [Keyboard Shortcuts](#keyboard-shortcuts)

## Quick Start

1. **Access YAP**: Navigate to your YAP instance at `https://app.localhost` (or your configured domain)
2. **Record Audio**: Click the "Record" button in the ASR tab
3. **Transcribe**: Click "Transcribe All" to convert your audio to text
4. **Copy/Export**: Use the Copy button or Export to save your transcript

## ASR Tab - Speech to Text

The ASR (Automatic Speech Recognition) tab provides browser-based audio recording and AI-powered transcription.

### Recording Audio

**Recording Controls:**
- **Record** - Start capturing audio from your microphone
- **Stop** - Stop the current recording
- **Space Bar** - Quick toggle record/stop

**What Happens:**
- A waveform visualization shows your audio input levels
- A timer displays the recording duration
- Each recording is saved as a separate "clip"

**Recording Tips:**
- Ensure microphone permissions are granted in your browser
- HTTPS or localhost is required for microphone access
- Speak clearly and at a consistent volume
- Each clip can be transcribed independently

### Transcribing Audio

**Transcription Options:**
- **Transcribe All** - Process all untranscribed clips at once
- **Ctrl+Enter** - Keyboard shortcut for transcribe all
- Individual clip transcription is also available

**Transcription Process:**
1. Audio is sent to the Whisper ASR backend
2. Processing status shows "working" for each clip
3. Transcribed text appears in the Transcript panel
4. Each clip's status updates to "transcribed" when complete

### Managing Clips

Each recorded clip displays:
- Duration (e.g., "0:15")
- Status badge (recorded/working/transcribed/error)
- Action buttons (play/delete)

**Clip Actions:**
- **Play** - Listen to the audio clip
- **Delete** - Remove the clip (confirmation optional)
- Click clip to expand and view details

### Transcript Panel

The transcript panel shows the combined text from all transcribed clips.

**Transcript Controls:**
- **Copy** - Copy all text to clipboard (Ctrl+Shift+C)
- **Download .txt** - Save transcript as a text file
- **Export** - Send to GitLab, GitHub, or SFTP (see [Export Guide](EXPORT.md))

### Transcript Formatting

Configure transcript formatting in Settings:

**Separator Options:**
- Show clip separators (`--- Clip N ---`)
- Between clips: blank line or single newline

**Whitespace Cleanup:**
- Collapse multiple blank lines
- Trim leading/trailing whitespace
- Normalize whitespace
- Line break mode: paragraphs or single line

### Auto-Features

**Auto-Transcribe:**
- Enable in Settings
- Automatically transcribes when recording stops
- Useful for continuous workflow

**Auto-Copy:**
- Enable in Settings
- Automatically copies transcript after transcription completes
- Works with auto-transcribe for one-click workflow

## TTS Tab - Text to Speech

The TTS (Text-to-Speech) tab converts written text into natural-sounding speech using Piper TTS.

### Text Input

**Input Methods:**
1. **Type or Paste** - Enter text directly in the text area
2. **Upload File** - Load a `.txt` or `.md` file

**Character Counter:**
- Shows current text length
- Helps estimate synthesis time

### Voice Selection

**Available Voices:**
- Voice list populated from your Piper models directory
- Examples: en_GB-cori-high, en_US-amy-medium
- Your last selected voice is remembered

**Voice Naming:**
- Format: `language_region-name-quality`
- Quality levels: low, medium, high
- Higher quality = better sound, slower synthesis

### Speaking Rate

**Rate Slider:**
- Range: 0.5× to 2.0×
- Default: 1.0× (normal speed)
- Lower values = slower speech
- Higher values = faster speech

### Markdown Preview

**Plain vs Markdown Toggle:**
- **Plain** - Shows raw text with formatting characters
- **Markdown** - Renders formatted markdown with headings, lists, links, etc.

**When to Use Markdown:**
- Viewing structured documents
- Checking formatting before synthesis
- Better readability for long texts

**Note:** TTS synthesizes the raw text, not the rendered HTML.

### Synthesis

**Generate Audio:**
1. Enter or upload text
2. Select voice and adjust rate
3. Click "Synthesize" (or press Ctrl+Enter)
4. Wait for processing (status shows "Synthesizing...")
5. Audio player appears when complete

**Audio Playback:**
- Standard HTML5 audio controls (play/pause/seek)
- Media session support for lock screen controls
- Auto-play on synthesis completion

**Download Audio:**
- Click "Download" button to save as `.wav` file
- Filename includes voice name and timestamp

### Read-Along Mode

Read-Along mode highlights text as it's spoken, useful for following along with longer content.

**How to Use:**
1. Synthesize your text
2. Click "Play with Read-Along"
3. A dedicated panel opens showing the text
4. Paragraphs highlight as they play

**Read-Along Controls:**
- **Pause** - Pause playback (resume with Play)
- **Stop** - Stop and close read-along
- **✕ Close** - Close panel (playback continues)

**Text Chunking:**
- Long text is split into chunks for sequential synthesis
- Default: paragraph-based chunking
- Each paragraph synthesized separately for smooth highlighting

## Export Tab

See the detailed [Export Guide](EXPORT.md) for complete export configuration and usage.

**Quick Overview:**
- Export transcripts to GitLab, GitHub, or SFTP
- Create and save export targets for quick access
- Generic webhooks for n8n, Zapier, etc.
- Preview payload before sending

## Data Tab

See the [Data & Metrics Guide](DATA.md) for complete metrics documentation.

**Quick Overview:**
- View usage statistics (minutes recorded/transcribed/generated)
- Browse event history with timestamps and details
- Export history as JSON
- Clear history when needed
- Local-only, no external telemetry

## Settings

Access Settings by clicking the ⚙️ button in the top navigation.

### Mobile & Tablet Settings

**Enable Mobile Toolbar:**
- Shows sticky toolbar with one-tap actions
- Appears automatically on narrow viewports (< 768px)
- Can be manually enabled/disabled

**Export Options:**
- Confirm before export
- One-tap export (uses last target)

### Data & Metrics

**Metrics Status:**
- View-only indicator showing if metrics are enabled
- Click for configuration instructions
- Controlled by server environment variables

### Behavior Settings

**Auto-Transcribe:**
- Automatically transcribe when recording stops
- Saves manual clicks for continuous recording

**Auto-Copy:**
- Automatically copy transcript after transcription
- Works with auto-transcribe

**Confirmations:**
- Confirm before clearing all clips
- Confirm before deleting individual clips
- Shift+Click always bypasses confirmation

### Formatting Settings

See [Transcript Formatting](#transcript-formatting) above for details on:
- Clip separators
- Whitespace cleanup
- Line break modes
- Between clips formatting

## Keyboard Shortcuts

Global shortcuts (work from any tab):

| Shortcut | Action |
|----------|--------|
| **D** | Switch to Data tab |
| **S** | Open Settings |

ASR Tab shortcuts:

| Shortcut | Action |
|----------|--------|
| **Space** | Start/Stop recording |
| **Ctrl+Enter** | Transcribe all clips |
| **Ctrl+Shift+C** | Copy transcript |

TTS Tab shortcuts:

| Shortcut | Action |
|----------|--------|
| **Ctrl+Enter** | Synthesize text |

**Note:** Shortcuts are disabled when typing in input fields or text areas.

## Tips & Best Practices

### For Best Recording Quality

1. Use a good quality microphone
2. Record in a quiet environment
3. Speak clearly and at a steady pace
4. Keep clips under 5 minutes for faster processing

### For Best Transcription Results

1. Use the appropriate Whisper model size:
   - `tiny.en` - Fast, lower accuracy
   - `base`, `small` - Good balance
   - `medium`, `large` - High accuracy, slower
2. Minimize background noise
3. Transcribe in batches rather than individually

### For Best TTS Quality

1. Use high-quality voice models when available
2. Keep paragraphs under 200 words for read-along mode
3. Use markdown for structured documents
4. Adjust speaking rate for personal preference

### Workflow Optimization

**Quick Transcription Workflow:**
1. Enable auto-transcribe + auto-copy
2. Record your audio (Space to start/stop)
3. Transcript automatically copied when done
4. Paste wherever needed

**Long Document TTS:**
1. Upload your `.md` file
2. Toggle to Markdown view to verify formatting
3. Select voice and adjust rate
4. Use Read-Along mode for best experience

## Troubleshooting

### Microphone Not Working
- Check browser permissions (usually top-left of address bar)
- Ensure HTTPS or localhost (required for `getUserMedia`)
- Verify correct microphone selected in system settings

### Transcription Fails
- Check that ASR backend is running
- Verify network connectivity
- Check browser console for errors
- Try smaller clip or different audio format

### TTS No Sound
- Verify TTS backend is running
- Check voice models are installed (see main README)
- Ensure browser allows audio playback
- Check system volume settings

### Export Not Working
- Verify exporter service is running
- Check credentials in exporter `.env` file
- Test API tokens have correct permissions
- See [Export Guide](EXPORT.md) for detailed troubleshooting

## Next Steps

- **Export Setup**: Configure export targets in the [Export Guide](EXPORT.md)
- **Metrics**: Learn about usage tracking in the [Data Guide](DATA.md)
- **Mobile Use**: Check the [Mobile & Tablet Guide](MOBILE.md)
- **Deployment**: See the main [README](../README.md) for installation and configuration
