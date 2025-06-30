# HKI Data Harmonization Systems

## Overview

This repository contains three automated data harmonization systems that consolidate and standardize survey data from multiple African countries. These systems run automatically on GitHub Actions to process data from SurveyCTO APIs and upload harmonized datasets to SharePoint.

## 🎯 Systems Included

### 1. PECS Data Harmonization
- **Purpose**: Post-Event Coverage Survey data processing
- **Countries**: 10 (Burkina Faso, Cameroon, Côte d'Ivoire, Guinea, Kenya, Madagascar, Mali, Niger, Nigeria, RDC)
- **Output**: 15 harmonized tables from 6 survey forms
- **Schedule**: Weekly/Monthly (configurable)

### 2. Independent Monitoring (IM) Harmonization
- **Purpose**: Household monitoring data processing
- **Countries**: 8 (Burkina Faso, Cameroun, Côte d'Ivoire, Guinée, Mali, Niger, Nigeria, RDC)
- **Output**: `HKI_SurveyCTO_Data.csv`
- **Schedule**: Weekly/Monthly (configurable)

### 3. IM Supervision Harmonization
- **Purpose**: Supervision monitoring data processing
- **Countries**: 7 (Burkina Faso, Côte d'Ivoire, Guinea, Mali, Niger, RDC, Kenya)
- **Output**: `IM_Supervision_Harmonized.csv`
- **Schedule**: Weekly/Monthly (configurable)

## 🔐 Security Configuration

### GitHub Secrets Setup (REQUIRED)

This system uses GitHub Secrets to securely store credentials. **Never commit credentials to the repository.**

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

| Secret Name | Description |
|------------|-------------|
| `SURVEYCTO_USERNAME` | SurveyCTO account email |
| `SURVEYCTO_PASSWORD` | SurveyCTO account password |
| `SHAREPOINT_USERNAME` | SharePoint account email |
| `SHAREPOINT_PASSWORD` | SharePoint account password |
| `SHAREPOINT_SITE_URL` | SharePoint site URL (e.g., https://hkw.sharepoint.com/teams/PBI_MER_Data) |

### Security Best Practices

- ✅ All credentials stored as encrypted GitHub Secrets
- ✅ No credentials in code or configuration files
- ✅ Private repository recommended
- ✅ Regular password rotation (every 90 days)
- ✅ Audit logs available in GitHub Actions
- ✅ Limited repository access to authorized personnel only

## 🤖 Automated Execution

### GitHub Actions Workflow

The systems run automatically via GitHub Actions on a configured schedule:

```yaml
name: HKI Data Harmonization

on:
  schedule:
    # Weekly: Every Monday at 6 AM UTC
    - cron: '0 6 * * 1'
    
    # Monthly: First day of month at 6 AM UTC
    # - cron: '0 6 1 * *'
  
  # Manual trigger option
  workflow_dispatch:

jobs:
  harmonize-data:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pandas requests numpy office365-REST-Python-Client openpyxl
    
    - name: Run PECS Harmonization
      env:
        SURVEYCTO_USERNAME: ${{ secrets.SURVEYCTO_USERNAME }}
        SURVEYCTO_PASSWORD: ${{ secrets.SURVEYCTO_PASSWORD }}
        SHAREPOINT_USERNAME: ${{ secrets.SHAREPOINT_USERNAME }}
        SHAREPOINT_PASSWORD: ${{ secrets.SHAREPOINT_PASSWORD }}
        SHAREPOINT_SITE_URL: ${{ secrets.SHAREPOINT_SITE_URL }}
      run: |
        python run_pecs_harmonization.py
    
    - name: Run IM Harmonization
      env:
        SURVEYCTO_USERNAME: ${{ secrets.SURVEYCTO_USERNAME }}
        SURVEYCTO_PASSWORD: ${{ secrets.SURVEYCTO_PASSWORD }}
        SHAREPOINT_USERNAME: ${{ secrets.SHAREPOINT_USERNAME }}
        SHAREPOINT_PASSWORD: ${{ secrets.SHAREPOINT_PASSWORD }}
        SHAREPOINT_SITE_URL: ${{ secrets.SHAREPOINT_SITE_URL }}
      run: |
        python IM_Data_Harmonization.py
    
    - name: Run IM Supervision Harmonization
      env:
        SURVEYCTO_USERNAME: ${{ secrets.SURVEYCTO_USERNAME }}
        SURVEYCTO_PASSWORD: ${{ secrets.SURVEYCTO_PASSWORD }}
        SHAREPOINT_USERNAME: ${{ secrets.SHAREPOINT_USERNAME }}
        SHAREPOINT_PASSWORD: ${{ secrets.SHAREPOINT_PASSWORD }}
        SHAREPOINT_SITE_URL: ${{ secrets.SHAREPOINT_SITE_URL }}
      run: |
        python IM_Supervision_Harmonization.py
```

### Schedule Options

Choose your preferred schedule by uncommenting the appropriate line:

- **Weekly** (Every Monday at 6 AM UTC): `'0 6 * * 1'`
- **Bi-weekly** (1st and 15th at 6 AM UTC): `'0 6 1,15 * *'`
- **Monthly** (1st of month at 6 AM UTC): `'0 6 1 * *'`

[UTC Time Converter](https://www.timeanddate.com/worldclock/timezone/utc)

## 📊 Output Files

All harmonized data is automatically uploaded to SharePoint:

| System | Output File | SharePoint Location |
|--------|------------|-------------------|
| PECS | 15 CSV files | `/PECS_Harmonized_Data/` |
| IM | `HKI_SurveyCTO_Data.csv` | `/python output/` |
| IM Supervision | `IM_Supervision_Harmonized.csv` | `/IM_Supervision_Harmonized_Data/` |

## 🔍 Monitoring and Alerts

### Execution Monitoring

1. **View Run History**:
   - Go to repository → **Actions** tab
   - See all past runs with status (✅ success, ❌ failure)

2. **Email Notifications**:
   - GitHub automatically sends emails for:
     - Failed runs
     - First successful run after failure

3. **Manual Trigger**:
   - Go to **Actions** → **HKI Data Harmonization**
   - Click **Run workflow** for immediate execution

### Execution Logs

Each run provides detailed logs:
- Data collection status per country
- Row counts and validation results
- Upload confirmation
- Error messages (if any)

## 🛠️ Maintenance

### System Health Checks

| Check | Frequency | Action |
|-------|-----------|--------|
| Credential validity | Monthly | Test in GitHub Actions |
| Password rotation | Quarterly | Update GitHub Secrets |
| Error review | Weekly | Check Actions tab |
| Data validation | Monthly | Review output files |

### Adding New Countries

1. Update configuration in the Python scripts:
   ```python
   # Add to country_configs dictionary
   "New Country": {
       "form": "form_id",
       "round": "R1",
       "year": 2024
   }
   ```

2. Add column mappings for the new country
3. Test via manual workflow trigger
4. Update documentation

### Troubleshooting

**Common Issues:**

1. **Authentication Failed**
   - Check GitHub Secrets are correctly named
   - Verify credentials haven't expired
   - Ensure no special characters need escaping

2. **SharePoint Upload Failed**
   - Verify SharePoint URL in secrets
   - Check folder permissions
   - Ensure SharePoint account is active

3. **Timeout Errors**
   - May indicate large datasets
   - Consider increasing timeout in scripts
   - Check SurveyCTO service status

## 🔐 Security Compliance

### Access Control
- Repository: Private, limited to authorized personnel
- GitHub Secrets: Accessible only during workflow execution
- SharePoint: Folder-level permissions required

### Audit Trail
- All executions logged in GitHub Actions
- Success/failure notifications via email
- SharePoint maintains file version history

### Data Protection
- Data transmitted over HTTPS
- Credentials never logged or displayed
- Temporary files cleaned up after execution

## 📋 Prerequisites

### Required Permissions

1. **GitHub Repository**
   - Admin access to configure secrets
   - Write access to create workflows

2. **SurveyCTO**
   - API access enabled
   - Read permissions for all forms

3. **SharePoint**
   - Write access to target folders
   - Sufficient storage quota

## 🚨 Important Notes

1. **Never commit credentials** - Use only GitHub Secrets
2. **Keep repository private** - Contains sensitive configuration
3. **Monitor executions** - Check weekly for failures
4. **Update documentation** - Log all system changes

## 📞 Support Contacts

**Technical Issues:**
- Data Team Lead: [Encrypted contact in SharePoint]
- IT Security: [Encrypted contact in SharePoint]

**External Support:**
- SurveyCTO: support@surveycto.com
- GitHub Support: https://support.github.com

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| [Date] | 1.0 | Initial setup | [Name] |

## ⚖️ License

This project is proprietary to Helen Keller International (HKI) and is for internal use only. Unauthorized distribution is prohibited.

---

**Repository Status**: 🔒 Private  
**Last Security Review**: [Date]  
**Next Review Due**: [Date + 90 days]
