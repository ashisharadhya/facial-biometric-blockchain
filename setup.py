"""
Setup Script for Facial Biometric Key Generation System
Installs dependencies and initializes the production environment
"""

import os
import subprocess
import sys
import json
from pathlib import Path


def install_requirements():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "production_requirements.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False


def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = [
        "user_templates",
        "secure_keys",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   Created: {directory}")
    
    print("✅ Directories created successfully")


def create_gitignore():
    """Create .gitignore file to protect sensitive data"""
    gitignore_content = """# Sensitive data - DO NOT COMMIT
user_templates/
secure_keys/
logs/
backups/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore file created")


def test_system():
    """Test if the system components work correctly"""
    print("🧪 Testing system components...")
    
    try:
        # Test imports
        from facial_keygen_system import ProductionKeygenSystem
        
        # Initialize system
        system = ProductionKeygenSystem()
        
        print("✅ System initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False


def display_usage_info():
    """Display usage information"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📖 Usage Options:")
    print("\n1. 🖥️  Desktop Application:")
    print("   python facial_keygen_system.py")
    
    print("\n2. 🌐 API Server (requires Flask):")
    print("   pip install flask")
    print("   python api_server.py")
    
    print("\n📊 System Features:")
    print("   • Single-shot face recognition")
    print("   • Automatic user identification")
    print("   • Dynamic LFSR key generation")
    print("   • Secure key storage")
    print("   • Production-ready architecture")
    
    print("\n🔒 Security Notes:")
    print("   • User templates stored in: user_templates/")
    print("   • Cryptographic keys stored in: secure_keys/")
    print("   • Never commit these directories to version control")
    
    print("\n🎯 Next Steps:")
    print("   1. Run the desktop application to test")
    print("   2. Register a few users to verify recognition")
    print("   3. Check generated keys in secure_keys/")
    print("\n" + "="*60)


def main():
    """Main setup function"""
    print("🚀 Facial Biometric Key Generation System Setup")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists('facial_keygen_system.py'):
        print("❌ Error: facial_keygen_system.py not found!")
        print("   Please run this script from the project directory")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Create .gitignore
    create_gitignore()
    
    # Test system
    if not test_system():
        print("❌ Setup completed but system test failed")
        print("   You may need to install additional dependencies")
    
    # Display usage information
    display_usage_info()


if __name__ == "__main__":
    main()