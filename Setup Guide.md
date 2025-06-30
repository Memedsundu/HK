# GitHub Automation Setup Guide for PECS Data Harmonization

## Table of Contents
1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Prepare Your Notebook](#3-step-1-prepare-your-notebook)
4. [Step 2: Create GitHub Repository](#4-step-2-create-github-repository)
5. [Step 3: Upload Your Files](#5-step-3-upload-your-files)
6. [Step 4: Set Up GitHub Secrets](#6-step-4-set-up-github-secrets)
7. [Step 5: Create GitHub Actions Workflow](#7-step-5-create-github-actions-workflow)
8. [Step 6: Test Your Automation](#8-step-6-test-your-automation)
9. [Step 7: Schedule Automatic Runs](#9-step-7-schedule-automatic-runs)
10. [Monitoring and Troubleshooting](#10-monitoring-and-troubleshooting)

---

## 1. Overview

This guide will help you set up automatic daily execution of your PECS Data Harmonization notebook using GitHub Actions. Once configured, your notebook will:
- Run automatically at scheduled times
- Save outputs to GitHub
- Send notifications if errors occur
- Keep a history of all runs

---

## 2. Prerequisites

Before starting, ensure you have:
- [ ] A GitHub account (free at github.com)
- [ ] Your `PECS_Data_Harmonization.ipynb` notebook
- [ ] SurveyCTO username and password
- [ ] Basic familiarity with GitHub's web interface

---

## 3. Step 1: Prepare Your Notebook

### 3.1 Create a Python Script Version

First, we need to convert your notebook to a Python script that can run automatically.

1. **Open your Jupyter notebook**
2. **Click File → Download as → Python (.py)**
3. **Save as `run_harmonization.py`**

### 3.2 Modify the Script for Automation

Open `run_harmonization.py` in a text editor and make these changes:

**At the top of the file, add:**
```python
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Get credentials from environment variables
SURVEYCTO_USERNAME = os.environ.get('SURVEYCTO_USERNAME')
SURVEYCTO_PASSWORD = os.environ.get('SURVEYCTO_PASSWORD')

if not SURVEYCTO_USERNAME or not SURVEYCTO_PASSWORD:
    print("Error: Missing credentials")
    sys.exit(1)

print("Starting PECS Data Harmonization...")
```

**Replace any hardcoded credentials in your script:**

Find:
```python
SURVEYCTO_USERNAME = "your_email@example.com"
SURVEYCTO_PASSWORD = "your_password"
```

Replace with:
```python
# Already defined at the top of the file
```

### 3.3 Add CSV Export Functionality

After each table is created, add code to save it as CSV:

```python
# Example for Census Main table
if census_main_combined is not None:
    output_filename = f"output/01_census_main_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
    census_main_combined.to_csv(output_filename, index=False)
    print(f"Saved: {output_filename}")
```

---

## 4. Step 2: Create GitHub Repository

### 4.1 Create New Repository

1. **Go to GitHub.com and sign in**
2. **Click the green "New" button** (or go to https://github.com/new)
3. **Fill in the repository details:**
   - Repository name: `pecs-data-harmonization`
   - Description: "Automated PECS data harmonization system"
   - Set to **Private** (important for data security)
   - Don't initialize with README (we'll add files manually)
4. **Click "Create repository"**

### 4.2 Note Your Repository URL

After creation, you'll see a URL like:
```
https://github.com/YOUR_USERNAME/pecs-data-harmonization
```
Keep this URL handy.

---

## 5. Step 3: Upload Your Files

### 5.1 Create Required Folders

In your repository, create the following folder structure:

1. **Click "creating a new file"**
2. **Type:** `output/.gitkeep` (this creates an output folder)
3. **Click "Commit new file"**

### 5.2 Upload Your Python Script

1. **Click "Add file" → "Upload files"**
2. **Drag and drop `run_harmonization.py`**
3. **Click "Commit changes"**

### 5.3 Create Requirements File

1. **Click "Add file" → "Create new file"**
2. **Name it:** `requirements.txt`
3. **Add these contents:**
```
pandas==1.5.3
requests==2.28.2
numpy==1.24.3
openpyxl==3.1.2
```
4. **Click "Commit new file"**

---

## 6. Step 4: Set Up GitHub Secrets

### 6.1 Navigate to Settings

1. **In your repository, click "Settings"** (top menu)
2. **In left sidebar, click "Secrets and variables"**
3. **Click "Actions"**

### 6.2 Add SurveyCTO Username

1. **Click "New repository secret"**
2. **Name:** `SURVEYCTO_USERNAME`
3. **Value:** Your SurveyCTO email (e.g., `camille@reliefapplications.org`)
4. **Click "Add secret"**

### 6.3 Add SurveyCTO Password

1. **Click "New repository secret"**
2. **Name:** `SURVEYCTO_PASSWORD`
3. **Value:** Your SurveyCTO password
4. **Click "Add secret"**

**Important:** These secrets are encrypted and cannot be viewed once saved.

---

## 7. Step 5: Create GitHub Actions Workflow

### 7.1 Create Workflow File

1. **Click "Actions"** in top menu
2. **Click "set up a workflow yourself"**
3. **Replace all content with the following:**

```yaml
name: PECS Data Harmonization

# Manual trigger for testing
on:
  workflow_dispatch:
  
# Scheduled runs (we'll add this later)
# schedule:
#   - cron: '0 6 * * *'  # Daily at 6 AM UTC

jobs:
  harmonize-data:
    runs-on: ubuntu-latest
    
    steps:
    # Step 1: Check out repository
    - name: Checkout repository
      uses: actions/checkout@v3
    
    # Step 2: Set up Python
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    # Step 3: Install dependencies
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    # Step 4: Run harmonization
    - name: Run data harmonization
      env:
        SURVEYCTO_USERNAME: ${{ secrets.SURVEYCTO_USERNAME }}
        SURVEYCTO_PASSWORD: ${{ secrets.SURVEYCTO_PASSWORD }}
      run: |
        python run_harmonization.py
    
    # Step 5: Upload outputs as artifacts
    - name: Upload harmonized data
      uses: actions/upload-artifact@v3
      with:
        name: harmonized-data-${{ github.run_number }}
        path: output/*.csv
        retention-days: 30
    
    # Step 6: Commit outputs back to repository
    - name: Commit outputs
      run: |
        git config --local user.email "actions@github.com"
        git config --local user.name "GitHub Actions"
        git add output/*.csv
        git diff --staged --quiet || git commit -m "Update harmonized data - $(date +'%Y-%m-%d')"
        git push
```

4. **Name the file:** `.github/workflows/harmonization.yml`
5. **Click "Commit changes"**

---

## 8. Step 6: Test Your Automation

### 8.1 Run Manual Test

1. **Go to "Actions" tab**
2. **Click "PECS Data Harmonization"** (your workflow name)
3. **Click "Run workflow" button**
4. **Click green "Run workflow" button**

### 8.2 Monitor the Run

1. **You'll see a yellow dot** (running)
2. **Click on the run to see details**
3. **Watch each step execute**
4. **Green checkmark = success, Red X = failure**

### 8.3 Check Results

If successful:
1. **Click on "harmonized-data-XXX"** in the run summary
2. **Download the zip file with your CSVs**
3. **Check that all 15 tables are present**

---

## 9. Step 7: Schedule Automatic Runs

### 9.1 Edit Workflow for Daily Runs

1. **Navigate to:** `.github/workflows/harmonization.yml`
2. **Click the pencil icon to edit**
3. **Uncomment the schedule section:**

Change from:
```yaml
# schedule:
#   - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

To:
```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

4. **Commit the change**

### 9.2 Understanding Cron Schedule

The cron expression `'0 6 * * *'` means:
- `0` - 0 minutes
- `6` - 6 hours (6 AM)
- `* * *` - Every day, every month, every day of week

**Common schedules:**
- `'0 6 * * *'` - Daily at 6 AM UTC
- `'0 6 * * 1-5'` - Weekdays only at 6 AM UTC
- `'0 6,18 * * *'` - Twice daily at 6 AM and 6 PM UTC

**Note:** GitHub Actions uses UTC time. Adjust based on your timezone.

---

## 10. Monitoring and Troubleshooting

### 10.1 Email Notifications

GitHub automatically sends email notifications for:
- Failed workflow runs
- First successful run after a failure

### 10.2 Viewing Run History

1. **Go to "Actions" tab**
2. **See list of all runs with status**
3. **Click any run to see details**

### 10.3 Common Issues and Solutions

#### Authentication Failed
**Problem:** 401 Unauthorized error  
**Solution:** 
1. Check secrets are correctly named
2. Verify credentials are still valid
3. Re-add secrets if needed

#### Module Not Found
**Problem:** ImportError for pandas or other libraries  
**Solution:** 
1. Check `requirements.txt` includes all needed libraries
2. Add missing libraries to the file

#### Timeout Errors
**Problem:** Connection timeout to SurveyCTO  
**Solution:** 
Add retry logic to your Python script:
```python
import time
from requests.exceptions import Timeout

def fetch_with_retry(url, auth, max_retries=3):
    for i in range(max_retries):
        try:
            response = requests.get(url, auth=auth, timeout=60)
            return response
        except Timeout:
            if i < max_retries - 1:
                time.sleep(30)  # Wait 30 seconds before retry
                continue
            raise
```

### 10.4 Downloading Results

**Option 1: From Actions**
1. Go to specific workflow run
2. Download artifacts (expires after 30 days)

**Option 2: From Repository**
1. Navigate to `output` folder
2. Click on any CSV file
3. Click "Download" button

### 10.5 Cost Considerations

- GitHub Actions provides 2,000 free minutes per month for private repositories
- Your daily run should take 5-10 minutes
- Monthly usage: ~300 minutes (well within free tier)

---

## Advanced Options

### Adding SharePoint Upload

To automatically upload to SharePoint, add this step to your workflow:

```yaml
- name: Upload to SharePoint
  run: |
    # Install SharePoint library
    pip install Office365-REST-Python-Client
    
    # Create upload script
    python upload_to_sharepoint.py
```

(Requires additional setup and SharePoint credentials)

### Adding Email Reports

To send email summaries after each run:

```yaml
- name: Send email report
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: PECS Harmonization Complete
    body: The daily harmonization has completed successfully.
    to: your-email@example.com
```

---

## Quick Checklist

### Initial Setup
- [ ] Convert notebook to Python script
- [ ] Create GitHub repository
- [ ] Upload script and requirements.txt
- [ ] Add secrets (username/password)
- [ ] Create workflow file
- [ ] Test manual run
- [ ] Enable scheduled runs

### Daily Monitoring
- [ ] Check email for failure notifications
- [ ] Weekly: Review Actions tab for any issues
- [ ] Monthly: Clean up old artifacts if needed

---

## Support Contacts

**GitHub Actions Documentation:**
- https://docs.github.com/actions

**GitHub Support:**
- https://support.github.com

**Internal Support:**
- Technical Lead: _____________
- Data Manager: ______________

---

**Remember:** Never commit credentials directly to the repository. Always use GitHub Secrets for sensitive information.
