#!/usr/bin/env python3
"""
Update Python scripts to use environment variables for credentials.
This ensures security in GitHub Actions.
"""

import os
import re

def update_credentials_in_file(filename):
    """Update hardcoded credentials to use environment variables"""
    
    if not os.path.exists(filename):
        print(f"⚠️  File not found: {filename}")
        return False
    
    with open(filename, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Add import os if not present
    if 'import os' not in content:
        # Find the first import statement and add import os after it
        import_match = re.search(r'^(import .+)$', content, re.MULTILINE)
        if import_match:
            content = content.replace(
                import_match.group(0), 
                import_match.group(0) + '\nimport os'
            )
        else:
            content = 'import os\n' + content
    
    # Replace SurveyCTO credentials
    content = re.sub(
        r'SURVEYCTO_USERNAME\s*=\s*["\'].*?["\']',
        'SURVEYCTO_USERNAME = os.environ.get("SURVEYCTO_USERNAME")',
        content
    )
    content = re.sub(
        r'SURVEYCTO_PASSWORD\s*=\s*["\'].*?["\']',
        'SURVEYCTO_PASSWORD = os.environ.get("SURVEYCTO_PASSWORD")',
        content
    )
    
    # Handle variations in variable names
    content = re.sub(
        r'username\s*=\s*["\'].*?@.*?["\']',  # Email pattern
        'username = os.environ.get("SURVEYCTO_USERNAME")',
        content
    )
    content = re.sub(
        r'password\s*=\s*["\']HELENKELLER\d{4}!?["\']',  # HK password pattern
        'password = os.environ.get("SURVEYCTO_PASSWORD")',
        content
    )
    
    # Replace SharePoint credentials
    content = re.sub(
        r'SHAREPOINT_USERNAME\s*=\s*["\'].*?["\']',
        'SHAREPOINT_USERNAME = os.environ.get("SHAREPOINT_USERNAME")',
        content
    )
    content = re.sub(
        r'SHAREPOINT_PASSWORD\s*=\s*["\'].*?["\']',
        'SHAREPOINT_PASSWORD = os.environ.get("SHAREPOINT_PASSWORD")',
        content
    )
    
    # Handle variations
    content = re.sub(
        r'sharepoint_username\s*=\s*["\'].*?["\']',
        'sharepoint_username = os.environ.get("SHAREPOINT_USERNAME")',
        content
    )
    content = re.sub(
        r'sharepoint_password\s*=\s*["\'].*?["\']',
        'sharepoint_password = os.environ.get("SHAREPOINT_PASSWORD")',
        content
    )
    
    # Replace SharePoint site URL
    content = re.sub(
        r'SHAREPOINT_SITE_URL\s*=\s*["\']https://.*?sharepoint\.com.*?["\']',
        'SHAREPOINT_SITE_URL = os.environ.get("SHAREPOINT_SITE_URL", "https://hkw.sharepoint.com/teams/PBI_MER_Data")',
        content
    )
    content = re.sub(
        r'sharepoint_site_url\s*=\s*["\']https://.*?sharepoint\.com.*?["\']',
        'sharepoint_site_url = os.environ.get("SHAREPOINT_SITE_URL", "https://hkw.sharepoint.com/teams/PBI_MER_Data")',
        content
    )
    
    # Add validation for credentials
    validation_code = '''
# Validate credentials are loaded
if not all([SURVEYCTO_USERNAME, SURVEYCTO_PASSWORD, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD]):
    print("❌ Error: Missing required environment variables")
    print("Please set: SURVEYCTO_USERNAME, SURVEYCTO_PASSWORD, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD")
    import sys
    sys.exit(1)
'''
    
    # Find a good place to insert validation (after credential definitions)
    if 'os.environ.get("SURVEYCTO_PASSWORD")' in content and validation_code not in content:
        # Find the last credential definition
        last_cred_pos = max(
            content.rfind('os.environ.get("SURVEYCTO_PASSWORD")'),
            content.rfind('os.environ.get("SHAREPOINT_PASSWORD")')
        )
        # Find the end of that line
        newline_pos = content.find('\n', last_cred_pos)
        if newline_pos != -1:
            content = content[:newline_pos+1] + validation_code + content[newline_pos+1:]
    
    if content != original_content:
        # Create backup
        backup_name = f"{filename}.backup"
        with open(backup_name, 'w') as f:
            f.write(original_content)
        print(f"✅ Created backup: {backup_name}")
        
        # Write updated content
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {filename}")
        print("   - Replaced hardcoded credentials with environment variables")
        return True
    else:
        print(f"ℹ️  No changes needed for: {filename}")
        return False

def main():
    """Update all Python harmonization scripts"""
    print("🔐 Updating scripts to use environment variables for credentials\n")
    
    scripts = [
        "IM_Data_Harmonization.py",
        "IM_Supervision_Harmonization.py"
    ]
    
    updated_count = 0
    for script in scripts:
        if update_credentials_in_file(script):
            updated_count += 1
    
    print(f"\n✅ Updated {updated_count} file(s)")
    
    if updated_count > 0:
        print("\n📝 Next steps:")
        print("1. Review the updated files")
        print("2. Test locally with environment variables:")
        print("   export SURVEYCTO_USERNAME='your_email@example.com'")
        print("   export SURVEYCTO_PASSWORD='your_password'")
        print("   export SHAREPOINT_USERNAME='your_sharepoint_email'")
        print("   export SHAREPOINT_PASSWORD='your_sharepoint_password'")
        print("   export SHAREPOINT_SITE_URL='https://hkw.sharepoint.com/teams/PBI_MER_Data'")
        print("3. Commit the updated files to Git")
        print("4. Configure GitHub Secrets in your repository settings")

if __name__ == "__main__":
    main()
