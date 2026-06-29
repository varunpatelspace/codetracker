# Deployment Guide: Vercel + MongoDB Atlas

## Prerequisites
- Node.js 16+ installed
- npm or yarn
- GitHub account (already linked to your repo)
- Vercel account (free at vercel.com)
- MongoDB Atlas account (free at mongodb.com/cloud/atlas)

## Step 1: Set up MongoDB Atlas

1. Go to **mongodb.com/cloud/atlas**
2. Create a free account
3. Create a new cluster:
   - Choose free tier
   - Select region closest to you
   - Cluster name: `codetracker`
4. Create a database user:
   - Username: `codetracker`
   - Password: (generate secure password)
5. Allow network access: Add `0.0.0.0/0` (or your IP only)
6. Get connection string:
   - Click "Connect" → "Drivers" → "Node.js"
   - Copy the connection string
   - Replace `<password>` with your actual password
   - Replace `myFirstDatabase` with `codetracker`

Example:
```
mongodb+srv://codetracker:PASSWORD@cluster.mongodb.net/codetracker?retryWrites=true&w=majority
```

## Step 2: Install Vercel CLI

```bash
npm install -g vercel
```

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Easiest)

1. Go to **vercel.com**
2. Sign in with GitHub
3. Click "New Project"
4. Select your `codetracker` repository
5. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave blank)
   - **Output Directory**: (leave blank)
6. Add Environment Variables:
   - Click "Add" for each:
     - `MONGODB_URI`: Your MongoDB connection string
     - `JWT_SECRET`: A random secure string (e.g., `openssl rand -base64 32`)
     - `GITHUB_TOKEN`: Your GitHub personal access token (optional)
     - `GITHUB_OWNER`: Your GitHub username
     - `GITHUB_REPO`: `codetracker`
     - `NODE_ENV`: `production`
7. Click "Deploy"
8. Wait for deployment to complete (~2-3 minutes)

### Option B: Deploy via CLI (Advanced)

```bash
cd c:\Users\varun\Downloads\CodeTracker\CodeTracker

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts:
# - Link to existing project? (if first time, answer "no")
# - Set project name: codetracker
# - Confirm directory structure
# - Add environment variables when prompted
```

## Step 4: Add Environment Variables on Vercel

After deployment starts:

1. Go to **vercel.com** → Your Project → **Settings** → **Environment Variables**
2. Add these variables:
   ```
   MONGODB_URI=mongodb+srv://codetracker:PASSWORD@cluster.mongodb.net/codetracker
   JWT_SECRET=<generate-random-string>
   GITHUB_TOKEN=<your-github-token>
   GITHUB_OWNER=varunpatelspace
   GITHUB_REPO=codetracker
   NODE_ENV=production
   ```
3. Click "Save"
4. Go to **Deployments** → Click the latest → Click "Redeploy"

## Step 5: Test Deployment

Once deployment is complete:

1. Your frontend will be at: `https://codetracker-<username>.vercel.app`
2. Test the API:
   - Health: `https://codetracker-<username>.vercel.app/health`
   - Should return: `{"status":"ok"}`
3. Test authentication:
   ```bash
   curl -X POST https://codetracker-<username>.vercel.app/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@example.com","password":"password123"}'
   ```

## Step 6: Update Frontend API Base

The frontend in `client/index.html` needs to point to your deployed backend:

Replace:
```javascript
const API_BASE = "http://localhost:5000";
```

With:
```javascript
const API_BASE = "https://codetracker-<username>.vercel.app";
```

Then commit and push:
```bash
git add client/index.html
git commit -m "Update API_BASE for production"
git push
```

Vercel will automatically redeploy.

## Step 7: Enable Automation (Optional)

The automation scheduler runs every 5 minutes to collect solved problems.

Currently it uses mock data. To enable real collection:

1. Add your platform usernames to the `.env` or environment variables:
   ```
   CODEFORCES_USERNAME=your_handle
   LEETCODE_USERNAME=your_username
   CODECHEF_USERNAME=your_username
   ```

2. Update `server/services/collectorService.js` to use real APIs instead of mock data

## Troubleshooting

### 502 Bad Gateway
- Check MongoDB URI is correct
- Verify environment variables are set
- Check function logs in Vercel dashboard

### MongoDB Connection Timeout
- Ensure your IP is in MongoDB Atlas network access list
- Add `0.0.0.0/0` if testing from different locations

### Frontend not loading
- Ensure `client/index.html` is in the correct folder
- Check `vercel.json` routes are configured correctly

## Project Structure After Deployment

```
client/           → Frontend (HTML/CSS/JS)
server/
  ├── api.js      → Vercel serverless handler
  ├── app.js      → Express app
  ├── index.js    → Local dev server
  └── ...         → Routes, models, services
vercel.json       → Deployment config
```

## Local Development vs Production

### Local (localhost:5000)
```bash
npm run dev
```

### Production (Vercel)
- Serverless functions (no persistent connections)
- Automatic scaling
- No local file system persistence
- Environment variables from Vercel dashboard

## Next Steps

1. Set up MongoDB Atlas
2. Deploy via Vercel Dashboard or CLI
3. Add environment variables
4. Test the API endpoints
5. Update frontend API_BASE if needed
6. Enable notifications and GitHub sync (in progress)
