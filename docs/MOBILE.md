# YAP Mobile & Tablet Guide

Guide to using YAP on tablets, mobile devices, and narrow viewports.

## Overview

YAP includes a responsive mobile toolbar designed for efficient one-handed operation on tablets and small screens. This guide covers the mobile-optimized interface and best practices for touch-screen devices.

## Mobile Toolbar

### Automatic Display

The mobile toolbar automatically appears when:
- Viewport width is less than 768px (typical tablet portrait mode)
- Mobile toolbar is manually enabled in Settings

**Manual Control:**
1. Open Settings (⚙️ button)
2. Toggle "Enable Mobile Toolbar"
3. Toolbar visibility persists across sessions

### Toolbar Layout

The mobile toolbar is a sticky panel at the top of the ASR tab, providing quick access to common actions:

```
┌──────────────────────────────────────────────┐
│ [⏺ Record] [📝 Transcribe] [📋 Copy] [📤 Export] │
│ [📊 Data] [⚙️ Settings] [⋯ More]              │
│ ● Status: Idle                               │
└──────────────────────────────────────────────┘
```

### Toolbar Buttons

**Primary Actions:**
- **⏺ Record** - Start/stop recording (toggles to ⏹ Stop when active)
- **📝 Transcribe** - Transcribe all untranscribed clips
- **📋 Copy** - Copy transcript to clipboard
- **📤 Export** - Open export panel or quick export to last target

**Navigation:**
- **📊 Data** - Switch to Data tab for metrics
- **⚙️ Settings** - Open settings panel
- **⋯ More** - Additional options menu

**Status Indicator:**
- Shows current state (Idle, Recording, Processing, Done, Error)
- Color-coded dot for quick visual feedback

### Button States

Buttons enable/disable automatically based on context:

| Button | Enabled When |
|--------|--------------|
| Record | Always available |
| Transcribe | At least one untranscribed clip exists |
| Copy | Transcript is available |
| Export | Transcript is available |
| Data | Always available |
| Settings | Always available |

## Touch-Optimized Features

### Large Touch Targets

All toolbar buttons are sized for easy touch interaction:
- Minimum 44×44px touch target
- Adequate spacing between buttons
- Clear visual feedback on tap

### Visual Feedback

Buttons provide clear feedback:
- **Active state** - Recording button shows red/recording state
- **Disabled state** - Grayed out when unavailable
- **Pressed state** - Visual depression on tap

### Gestures

**Supported:**
- Tap - All standard interactions
- Long-press - Clip actions (play/delete)
- Swipe - Scroll through clips and transcript
- Pinch-zoom - Not blocked (browser default)

**Not Implemented:**
- Swipe to delete clips
- Pull to refresh
- Custom gesture shortcuts

## Tablet Workflow

### Portrait Mode (Recommended)

In portrait orientation, the mobile toolbar provides optimal efficiency:

**Recording Workflow:**
1. Tap "⏺ Record" to start
2. Speak naturally
3. Tap "⏹ Stop" when done
4. Tap "📝 Transcribe" to process
5. Tap "📋 Copy" to use text

**One-Tap Workflow:**
Enable these settings for streamlined use:
- Auto-transcribe
- Auto-copy
- One-tap export (with saved target)

Then simply:
1. Tap Record → Stop
2. Wait for auto-transcribe + copy
3. Paste wherever needed

### Landscape Mode

Landscape orientation shows the standard desktop interface with:
- Full navigation bar at top
- Waveform visualization
- Clips list
- Transcript panel

Mobile toolbar can still be enabled if preferred.

## Mobile Settings

Access mobile-specific settings via Settings (⚙️):

### Mobile Toolbar Settings

**Enable Mobile Toolbar:**
- Toggle: ON/OFF
- Default: Auto (shows on narrow viewports)
- When disabled: Shows only on very narrow screens (<480px)

**Confirm Before Export:**
- Toggle: ON/OFF
- Default: ON
- Shows confirmation before export action

**One-Tap Export:**
- Toggle: ON/OFF
- Default: OFF
- When enabled: Export button sends to last used target
- Requires: At least one successful export first

### Requirements

Mobile toolbar only shows in **ASR tab**. TTS and Data tabs use the standard interface on all screen sizes.

## Keyboard Shortcuts (On-Screen Keyboard)

Even with touch input, keyboard shortcuts work if a physical keyboard is attached:

| Shortcut | Action |
|----------|--------|
| Space | Start/Stop recording |
| Ctrl+Enter | Transcribe all |
| Ctrl+Shift+C | Copy transcript |
| D | Switch to Data tab |
| S | Open Settings |

**Note:** Shortcuts don't work when typing in text fields.

## Tips for Tablet Use

### Recording

**Best Practices:**
- Hold tablet steady or use a stand
- Position microphone toward you
- Use external microphone for best quality
- Test microphone access before first use

**Microphone Selection:**
If you have multiple audio inputs:
1. Browser may prompt for permission on first use
2. Select built-in microphone or external USB mic
3. Permission persists across sessions

### Network Considerations

**Local Network:**
- Best: Tablet and YAP server on same LAN
- Fast transcription and synthesis
- Minimal latency

**Remote Access:**
- Works over internet via VPN or port forwarding
- Slower transcription due to network latency
- Consider using smaller Whisper models for speed

### Screen Rotation Lock

For consistent interface, enable screen rotation lock:
- Prevents layout shifts during use
- Choose portrait for mobile toolbar
- Choose landscape for full desktop interface

## Touch Screen UI Tips

### Clips List

**Scrolling:**
- Swipe up/down to scroll through clips
- Momentum scrolling supported

**Clip Actions:**
- Tap clip to expand/collapse details
- Tap ▶ to play audio
- Tap 🗑️ to delete clip

**Selection:**
- No multi-select currently supported
- Actions apply to individual clips

### Transcript Panel

**Scrolling:**
- Swipe to scroll long transcripts
- Pinch-zoom to adjust text size (browser default)

**Selection:**
- Long-press to select text
- Use browser copy menu

**Editing:**
- Transcript is read-only
- Copy text and paste into editor if changes needed

## Browser Recommendations

### iOS (iPad/iPhone)

**Recommended:** Safari (best compatibility)

**Also Works:**
- Chrome for iOS
- Firefox for iOS

**Notes:**
- Safari has best MediaRecorder support
- Other browsers use Safari engine on iOS
- Ensure iOS 14+ for full feature support

### Android (Tablets)

**Recommended:** Chrome or Firefox

**Notes:**
- Chrome has excellent MediaRecorder support
- Firefox works well but test microphone first
- Samsung Internet also compatible

### Required Permissions

All browsers require:
- ✅ Microphone access (for recording)
- ✅ HTTPS or localhost (for getUserMedia)

Optional:
- Notifications (not currently used)
- Location (not used)

## Troubleshooting

### Mobile Toolbar Not Showing

**Problem:** Toolbar doesn't appear on tablet.

**Check:**
1. Viewport width < 768px (or manually enabled in Settings)
2. You're in the ASR tab (toolbar ASR-specific)
3. Settings → "Enable Mobile Toolbar" is ON (or auto)
4. Page loaded correctly (try refresh)

### Buttons Not Working

**Problem:** Tapping buttons has no effect.

**Solutions:**
1. Ensure button is enabled (not grayed out)
2. Refresh page if interface frozen
3. Check browser console for errors (if accessible)
4. Try different browser

### Recording Not Starting

**Problem:** Record button tapped but nothing happens.

**Check:**
1. Microphone permissions granted
2. Browser supports getUserMedia (modern browsers only)
3. HTTPS or localhost (required for mic access)
4. No other app using microphone
5. Browser console shows error details

### Layout Issues

**Problem:** Interface looks wrong or cut off.

**Solutions:**
1. Rotate device and rotate back
2. Refresh page
3. Clear browser cache
4. Update browser to latest version
5. Try different browser

### Copy Button Not Working

**Problem:** Copy doesn't put text in clipboard.

**Check:**
1. Browser clipboard permissions
2. Try long-press on transcript → Copy
3. Some browsers require user interaction for clipboard

## Comparison: Mobile vs Desktop

| Feature | Desktop | Mobile Toolbar |
|---------|---------|----------------|
| Record | Button in panel | Toolbar button |
| Transcribe | Button in panel | Toolbar button |
| Copy | Button below transcript | Toolbar button |
| Export | Button below transcript | Toolbar button |
| Status | In panel | Toolbar status bar |
| Waveform | Full visualization | Same |
| Clips List | Full detail | Same |
| Transcript | Full panel | Same |
| Settings | Button in nav | Toolbar button |
| Data | Nav button | Toolbar button |

**Key Difference:** Mobile toolbar consolidates actions into a sticky panel for one-handed access.

## Accessibility

### Touch Targets

- All buttons meet 44×44px minimum size
- Adequate spacing prevents mis-taps
- Clear visual feedback on interaction

### Screen Readers

- Buttons have descriptive labels
- Status updates announced
- Icons have text fallbacks

### Contrast

- High contrast for readability
- Dark theme optimized for low light
- Clear status indicators

### Text Size

- Respects system font size settings
- Transcript uses readable font size
- Pinch-zoom not blocked

## Performance Optimization

### Battery Life

**To Maximize:**
- Stop recording when not needed (recorder holds mic open)
- Close read-along panel when done
- Avoid keeping audio player running

### Data Usage

Over cellular/metered connections:
- Transcription uploads full audio clips
- TTS downloads audio files
- Each operation uses data proportional to audio length
- Consider using on WiFi for heavy usage

### Speed Tips

**Faster Transcription:**
- Use smaller Whisper models (tiny.en, base)
- Record shorter clips
- Ensure good network connection

**Faster TTS:**
- Use medium or low quality voices
- Keep text chunks under 500 chars
- Faster speaking rates process quicker

## Next Steps

- **Try It**: Enable mobile toolbar in Settings and test workflow
- **Customize**: Adjust auto-features for your preferred workflow
- **Export Setup**: Configure export targets for one-tap export
- **User Guide**: See [User Guide](USER_GUIDE.md) for complete feature documentation
