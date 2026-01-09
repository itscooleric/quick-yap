// Yap ASR Configuration
// Copy this file to config.js and adjust the values as needed.
// This file is loaded by index.html to configure cross-linking and add-on settings.

window.__YAP_CONFIG = {
  // Cross-linking URLs (leave empty or use relative paths for same-domain)
  asrUrl: '',           // e.g., 'https://asr.yourdomain.com' or '' for current page
  ttsUrl: '/tts/',      // e.g., 'https://tts.yourdomain.com' or relative path

  // Ollama add-on configuration
  ollamaUrl: 'http://localhost:11434',
  ollamaModel: 'llama3'
};
