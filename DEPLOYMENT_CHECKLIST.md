# Deployment Configuration Checklist

## Issue: NetworkError when attempting to fetch resource

This error occurs when the frontend can't reach the backend API, usually due to incorrect environment variable configuration in production.

## Steps to Fix

### 1. Find Your Deployed URLs

- **Render Backend URL**: Check your Render dashboard (e.g., `https://paco-api-xxxx.onrender.com`)
- **Vercel Frontend URL**: Check your Vercel dashboard (e.g., `https://your-app.vercel.app`)

### 2. Configure Vercel Environment Variables

Go to: Vercel Dashboard → Your Project → Settings → Environment Variables

Add the following:

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://your-render-url.onrender.com/api/v1` | Production |
| `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` | (your agent ID) | Production |
| `NEXT_PUBLIC_ELEVENLABS_API_KEY` | (your API key) | Production |

**Important**: After adding these, redeploy your Vercel app.

### 3. Configure Render Environment Variables

Go to: Render Dashboard → Your Service → Environment → Add Environment Variable

Add or update:

| Variable Name | Value |
|--------------|-------|
| `CORS_ORIGINS` | `https://your-vercel-url.vercel.app` |
| `SECRET_KEY` | (your secret key) |
| `DATABASE_URL` | (should be auto-configured) |
| `GROQ_API_KEY` | (your Groq API key) |
| `ELEVENLABS_API_KEY` | (your ElevenLabs API key) |

**Important**: After updating CORS_ORIGINS, redeploy your Render service.

### 4. Verify Configuration

#### Test Backend API
```bash
# Check if backend is running
curl https://your-render-url.onrender.com/health

# Check API docs
curl https://your-render-url.onrender.com/docs
```

#### Test Frontend Connection
1. Open browser DevTools (F12)
2. Go to Console tab
3. Visit your Vercel URL
4. Try to login with an RID
5. Check for any CORS or network errors

### 5. Common Issues

#### CORS Error
**Symptom**: "Access-Control-Allow-Origin" error in browser console
**Fix**: Make sure `CORS_ORIGINS` in Render includes your Vercel URL

#### Wrong API URL
**Symptom**: "NetworkError" or "Failed to fetch"
**Fix**: Verify `NEXT_PUBLIC_API_URL` in Vercel matches your Render URL

#### 404 Not Found
**Symptom**: API returns 404
**Fix**: Check that the API endpoint path includes `/api/v1` prefix

## Quick Debug Commands

### Check what URL your frontend is using:
Open browser console on your deployed Vercel app and run:
```javascript
console.log(process.env.NEXT_PUBLIC_API_URL)
```

### Test backend CORS:
```bash
curl -X OPTIONS https://your-render-url.onrender.com/api/v1/auth/validate-research-id \
  -H "Origin: https://your-vercel-url.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

## Notes

- Environment variables starting with `NEXT_PUBLIC_` are exposed to the browser
- You must redeploy after changing environment variables
- CORS must allow your exact frontend domain (including https://)
- Render free tier may have cold starts (first request takes ~30 seconds)
