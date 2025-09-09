# Cloudflare Setup for voicemode.sh

This guide explains how to deploy the voicemode.sh domain to serve the installer script.

## Prerequisites

1. Cloudflare account with voicemode.sh domain
2. Cloudflare API token with Workers permissions
3. Node.js installed locally (for wrangler CLI)

## Setup Steps

### 1. Install Wrangler CLI

```bash
npm install -g wrangler
```

### 2. Login to Cloudflare

```bash
wrangler login
```

### 3. Update Configuration

Edit `wrangler.toml`:
- Replace `your-account-id` with your Cloudflare account ID
- Get this from: https://dash.cloudflare.com/ → Right sidebar

### 4. Deploy the Worker

```bash
# Deploy to production
wrangler deploy

# Or test locally first
wrangler dev
```

### 5. Configure Domain

In Cloudflare Dashboard:
1. Go to Workers & Pages
2. Select your worker
3. Go to Settings → Triggers
4. Add custom domain: voicemode.sh
5. Add custom domain: www.voicemode.sh

### 6. Set Up GitHub Actions (Optional)

Add these secrets to your GitHub repository:
- `CLOUDFLARE_API_TOKEN` - Create at https://dash.cloudflare.com/profile/api-tokens
- `CLOUDFLARE_ACCOUNT_ID` - From dashboard
- `CLOUDFLARE_ZONE_ID` - From domain overview page (optional, for cache purging)

## How It Works

The Cloudflare Worker:
1. Detects if the request is from a CLI tool (curl, wget) or browser
2. Serves the install script to CLI tools
3. Serves a nice landing page to browsers
4. Fetches the install script from GitHub (with caching)
5. Falls back to embedded script if GitHub is unavailable

## Testing

### Test CLI Install
```bash
# Should download install script
curl -sSf https://voicemode.sh

# Should also work
wget -qO- https://voicemode.sh
```

### Test Browser
Open https://voicemode.sh in a browser - should see the landing page.

### Test Direct Script Access
```bash
curl https://voicemode.sh/install.sh
```

## Monitoring

View metrics in Cloudflare Dashboard:
- Workers & Pages → Analytics
- See requests, errors, and performance

## Updating

### Update Install Script
1. Edit `docs/web/install.sh`
2. Commit and push
3. Worker will fetch new version (5-minute cache)

### Update Worker or Landing Page
1. Edit `cloudflare-worker.js`
2. Deploy: `wrangler deploy`
3. Or push to GitHub (if Actions configured)

## Troubleshooting

### Worker Not Responding
- Check worker status in dashboard
- View logs: `wrangler tail`

### Install Script Not Updating
- Cache TTL is 5 minutes
- Force refresh: Purge cache in Cloudflare dashboard
- Or wait for cache to expire

### Domain Not Working
- Ensure DNS is configured correctly
- Check Workers → Settings → Triggers
- Verify custom domain is active

## Security Notes

- Install script is fetched from public GitHub repo
- No sensitive data in worker
- HTTPS enforced by Cloudflare
- User-agent detection is for convenience only

## Analytics (Optional)

The worker includes basic analytics:
- Track installs by country
- See user agents
- Access at: https://voicemode.sh/analytics

To enable, create a Workers KV namespace:
```bash
wrangler kv:namespace create "CACHE"
```

Then update the IDs in `wrangler.toml`.