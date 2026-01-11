# YAP Export Feature

This document describes how to use the Export feature in YAP to send transcripts to external services.

## Overview

YAP supports exporting transcripts via:
1. **Generic Webhooks** - Send to any HTTP endpoint
2. **GitLab Commit via Webhook** - Commit to GitLab through a proxy (recommended)
3. **GitLab Commit Direct** - Commit directly to GitLab API (may be CORS blocked)
4. **Exporter Service** - Use the YAP exporter service for GitHub, GitLab, or SFTP

## Access the Export Panel

1. Click the **Export** button in the ASR transcript panel
2. The Export panel opens showing your configured export targets

## Export Target Types

### Generic Webhook

Send transcripts to any HTTP endpoint (n8n, Zapier, custom servers, etc.).

**Configuration:**
- **Name**: Display name for the target
- **Webhook URL**: The endpoint URL to send to
- **Method**: HTTP method (POST or PUT)
- **Headers**: JSON object for custom headers (e.g., `{"Authorization": "Bearer xyz"}`)
- **Payload Format**: 
  - `transcript_only`: Minimal payload with just the transcript
  - `full_session`: Full payload including clips metadata

**Example webhook payload (transcript_only):**
```json
{
  "source": "yap",
  "created_at": "2024-01-15T10:30:00.000Z",
  "transcript": "Your transcribed text..."
}
```

**Example webhook payload (full_session):**
```json
{
  "source": "yap",
  "created_at": "2024-01-15T10:30:00.000Z",
  "transcript": "Your transcribed text...",
  "clips": [
    {
      "id": "abc123",
      "created_at": "2024-01-15T10:28:00.000Z",
      "duration_ms": 45000,
      "text": "Individual clip text..."
    }
  ],
  "meta": {
    "app_version": "1.0.0"
  }
}
```

### GitLab Commit via Webhook (Recommended)

Commit transcripts to GitLab through a proxy webhook. This approach:
- Avoids CORS issues (browser can't call GitLab API directly)
- Keeps tokens secure on the server side
- Works with n8n, custom servers, or any webhook handler

**Configuration:**
- **Webhook/Proxy URL**: Your proxy endpoint (e.g., `http://localhost:5678/webhook/gitlab-commit`)
- **Headers**: Optional auth headers for the proxy
- **Project ID or Path**: GitLab project (e.g., `username/repo` or project ID)
- **Branch**: Target branch (default: `main`)
- **File Path**: Where to save the file (supports variables)
- **File Format**: JSON or Markdown

**File path variables:**
- `{year}` - Current year (e.g., 2024)
- `{month}` - Current month (e.g., 01)
- `{day}` - Current day (e.g., 15)
- `{timestamp}` - Full timestamp (e.g., 20240115-1030)
- `{date}` - Date string (e.g., 2024-01-15)

**Example file path:** `inbox/yap/{year}/{month}/{timestamp}.json`

**Webhook payload sent to proxy:**
```json
{
  "intent": "gitlab_commit",
  "project_id": "username/repo",
  "branch": "main",
  "commit_message": "yap export 2024-01-15 10:30",
  "file_path": "inbox/yap/2024/01/20240115-1030.json",
  "file_format": "json",
  "payload": {
    "source": "yap",
    "created_at": "2024-01-15T10:30:00.000Z",
    "transcript": "..."
  }
}
```

### GitLab Commit Direct

Commit directly to GitLab's API. 

⚠️ **Limitations:**
- May be blocked by CORS depending on your GitLab instance
- Token is stored in browser localStorage (not recommended for shared computers)

**Configuration:**
- **GitLab URL**: Your GitLab instance (default: `https://gitlab.com`)
- **Project ID or Path**: Project to commit to
- **Private Token**: GitLab personal access token with `api` scope
- **Branch**: Target branch
- **File Path**: Where to save the file
- **File Format**: JSON or Markdown
- **Commit Message**: Custom commit message

**If you encounter CORS errors:**
The browser will show an error like "Request failed - likely CORS blocked". Switch to the webhook/proxy mode instead.

### Exporter Service (Legacy)

If you have the YAP exporter service running, you can use it for GitHub, GitLab, or SFTP exports. Configure the exporter URL in the Export settings.

## Setting Up n8n as a GitLab Commit Proxy

Here's how to set up n8n to handle GitLab commits:

1. Create a new workflow in n8n
2. Add a **Webhook** trigger node:
   - HTTP Method: POST
   - Path: `/gitlab-commit`
3. Add an **HTTP Request** node to call GitLab API:
   - Method: POST
   - URL: `https://gitlab.com/api/v4/projects/{{ $json.project_id }}/repository/commits`
   - Authentication: Add GitLab token via header
   - Body: Map the incoming payload to GitLab's commit format
4. Connect the nodes and activate the workflow

## Security Notes

### Token Storage

- **Webhook/Proxy mode**: Tokens stay on your server (recommended)
- **Direct mode**: Token stored in browser localStorage
  - Not encrypted
  - Accessible to JavaScript
  - Not suitable for shared computers
  - Clear localStorage to remove tokens

### CORS Considerations

GitLab's API typically doesn't allow cross-origin requests from browsers. Use webhook/proxy mode for reliable operation.

### HTTPS

For production use, ensure your webhook endpoints use HTTPS to protect data in transit.

## Troubleshooting

### "CORS blocked" error
Switch from Direct mode to Webhook mode. The GitLab API doesn't support browser-based requests.

### "Request failed" with no details
- Check the webhook URL is correct
- Verify the proxy is running
- Check network connectivity

### Export succeeds but no file appears
- Verify the project ID/path is correct
- Check the branch exists
- Ensure the token has write permissions

### Authentication errors
- Verify the token is correct
- Check token has required scopes (`api` for GitLab)
- Ensure token hasn't expired
