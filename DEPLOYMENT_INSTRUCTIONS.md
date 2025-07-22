# GitHub and Streamlit Deployment Instructions

## Quick Deploy to Streamlit Cloud

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in to your account
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository: `trading-webhook-proxy`
5. Make it **Public** (required for free Streamlit deployment)
6. Do NOT initialize with README (we already have files)
7. Click "Create repository"

### Step 2: Push Code to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your local terminal:

```bash
# Navigate to your project directory
cd /path/to/webhook-proxy

# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/trading-webhook-proxy.git

# Push the code to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/trading-webhook-proxy`
5. Set the main file path: `streamlit_app.py`
6. Click "Deploy!"

Your app will be live at: `https://YOUR_USERNAME-trading-webhook-proxy-streamlit-app-main.streamlit.app`

## Alternative: Manual Upload Method

If you prefer not to use Git:

1. Download the complete ZIP file provided
2. Extract all files
3. Create a new GitHub repository (as above)
4. Use GitHub's web interface to upload files:
   - Click "uploading an existing file"
   - Drag and drop all files from the extracted folder
   - Commit the files
5. Follow Step 3 above for Streamlit deployment

## Files Included for Streamlit Deployment

- `streamlit_app.py` - Main Streamlit application
- `requirements_streamlit.txt` - Streamlit-specific dependencies
- All Flask files (for comparison and alternative deployment)
- Complete documentation in README.md

## Streamlit App Features

✅ **Complete Trading Functionality**
- BUY, SELL, EXIT buttons
- All Webhooks support
- Real-time status feedback
- Corrected JSON payload format

✅ **Professional UI**
- Responsive design
- Modern styling
- Interactive forms
- Status indicators

✅ **Database Management**
- Add/delete webhooks
- Persistent storage
- Real-time updates

✅ **Corrected JSON Format**
```json
{
  "headers": {...},
  "params": {},
  "query": {},
  "body": "description: JMA US500 v3...",
  "webhookUrl": "https://your-webhook-url.com",
  "executionMode": "production"
}
```

## Troubleshooting

### Issue: "Module not found"
**Solution**: Ensure `requirements_streamlit.txt` is in the root directory

### Issue: "Database error"
**Solution**: Streamlit will automatically create the SQLite database

### Issue: "App won't start"
**Solution**: Check that `streamlit_app.py` is in the root directory

### Issue: "Repository not found"
**Solution**: Ensure repository is public for free Streamlit deployment

## Support

If you encounter any issues:
1. Check the Streamlit logs in the deployment dashboard
2. Ensure all files are properly uploaded to GitHub
3. Verify the repository is public
4. Check that `streamlit_app.py` is in the root directory

Your Streamlit app will be ready in 2-3 minutes after deployment!

