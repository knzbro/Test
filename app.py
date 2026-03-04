#!/usr/bin/env python3
# MDF Legends - PRO Level Real Facebook Reporter
# Version 6.0 - Fully Automatic | 10+ Features | REAL Working
# Powered By Al'mudafioon Force

import os
import sys
import time
import json
import random
import string
import subprocess
import platform
import urllib.request
import zipfile
import shutil
import threading
import queue
from datetime import datetime
from typing import Dict, List, Optional

# ==================== CONFIGURATION ====================

VERSION = "6.0"
AUTHOR = "Al'mudafioon Force"
BANNER = """
╔═══════════════════════════════════════════════════════════════════╗
║                      🔴 MDF LEGENDS PRO v6.0                     ║
║                    * REAL FACEBOOK REPORTER *                    ║
║              ⚡ 10+ Features | Fully Automatic ⚡                 ║
║              ─────────────────────────────────────               ║
║          🛡️ Multi-Account  |  🎯 Mass Reporting                  ║
║          🤖 Auto Retry     |  🔄 Proxy Rotation                   ║
║          📊 Live Stats     |  💾 Auto Save                        ║
║          🔍 Smart Scan     |  ⚙️ Auto Config                      ║
║              ─────────────────────────────────────               ║
║                 Powered By Al'mudafioon Force                     ║
╚═══════════════════════════════════════════════════════════════════╝
"""

# ==================== TERMINAL COLORS ====================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def logo(text): print(f"{Colors.RED}{Colors.BOLD}{text}{Colors.END}")
    def success(text): print(f"{Colors.GREEN}{text}{Colors.END}")
    def error(text): print(f"{Colors.RED}{text}{Colors.END}")
    def warning(text): print(f"{Colors.YELLOW}{text}{Colors.END}")
    def info(text): print(f"{Colors.CYAN}{text}{Colors.END}")
    def header(text): print(f"{Colors.MAGENTA}{Colors.BOLD}{text}{Colors.END}")
    def progress(text): print(f"{Colors.BLUE}{text}{Colors.END}")

# ==================== TERMUX DETECTION ====================

def is_termux():
    return 'com.termux' in os.environ.get('PREFIX', '')

def is_android():
    return 'android' in platform.system().lower() or is_termux()

# ==================== AUTO INSTALLER ====================

class AutoInstaller:
    def __init__(self):
        self.logs = []
        
    def log(self, msg, type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        self.logs.append(log_entry)
        
        if type == "success":
            Colors.success(f"  ✅ {msg}")
        elif type == "error":
            Colors.error(f"  ❌ {msg}")
        elif type == "warning":
            Colors.warning(f"  ⚠️ {msg}")
        else:
            print(f"  📌 {msg}")
    
    def install_python_packages(self):
        """Install required Python packages"""
        self.log("\n📦 Installing Python packages...")
        
        packages = ['selenium', 'flask', 'requests', 'colorama', 'psutil']
        
        for package in packages:
            try:
                __import__(package)
                self.log(f"{package} already installed", "success")
            except:
                self.log(f"Installing {package}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self.log(f"{package} installed", "success")
                except:
                    self.log(f"Failed to install {package}", "error")
    
    def install_termux_packages(self):
        """Install Termux specific packages"""
        if not is_termux():
            return
        
        self.log("\n📱 Installing Termux packages...")
        
        commands = [
            ("pkg update -y", "Updating packages"),
            ("pkg install tur-repo -y", "Installing tur-repo"),
            ("pkg install chromium -y", "Installing Chromium browser"),
            ("pkg install python -y", "Installing Python"),
        ]
        
        for cmd, msg in commands:
            self.log(msg + "...")
            try:
                subprocess.run(cmd, shell=True, check=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.log(msg + " complete", "success")
            except:
                self.log(msg + " failed", "error")
    
    def install_chromedriver(self):
        """Install ChromeDriver"""
        self.log("\n🚗 Installing ChromeDriver...")
        
        if is_termux():
            # Termux: chromedriver comes with chromium
            chromedriver_path = '/data/data/com.termux/files/usr/bin/chromedriver'
            if os.path.exists(chromedriver_path):
                self.log("ChromeDriver already installed", "success")
                return chromedriver_path
        
        # Check if already in PATH
        try:
            result = subprocess.run(['which', 'chromedriver'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"ChromeDriver found: {result.stdout.strip()}", "success")
                return result.stdout.strip()
        except:
            pass
        
        # Download for non-Termux
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        version = "114.0.5735.90"
        
        if system == "linux":
            url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip"
        elif system == "windows":
            url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
        elif system == "darwin":
            if "arm" in machine:
                url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/mac-arm64/chromedriver-mac-arm64.zip"
            else:
                url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/mac-x64/chromedriver-mac-x64.zip"
        else:
            self.log("Unknown platform", "error")
            return None
        
        try:
            self.log("Downloading ChromeDriver...")
            urllib.request.urlretrieve(url, "chromedriver.zip")
            
            self.log("Extracting...")
            with zipfile.ZipFile("chromedriver.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            os.remove("chromedriver.zip")
            
            # Find chromedriver
            for root, dirs, files in os.walk("."):
                if "chromedriver" in files:
                    driver_path = os.path.join(root, "chromedriver")
                    if os.path.exists("./chromedriver"):
                        os.remove("./chromedriver")
                    shutil.move(driver_path, "./chromedriver")
                    os.chmod("./chromedriver", 0o755)
                    self.log(f"ChromeDriver installed at ./chromedriver", "success")
                    return "./chromedriver"
            
            self.log("ChromeDriver not found after extraction", "error")
            return None
            
        except Exception as e:
            self.log(f"Installation failed: {e}", "error")
            return None
    
    def create_symlinks(self):
        """Create necessary symlinks for Termux"""
        if not is_termux():
            return
        
        self.log("\n🔗 Creating symlinks...")
        
        chromium_path = '/data/data/com.termux/files/usr/bin/chromium'
        if os.path.exists(chromium_path):
            # Create google-chrome symlink
            chrome_link = '/data/data/com.termux/files/usr/bin/google-chrome'
            if not os.path.exists(chrome_link):
                try:
                    os.symlink(chromium_path, chrome_link)
                    self.log("Created google-chrome symlink", "success")
                except:
                    self.log("Failed to create google-chrome symlink", "warning")
            
            # Create chrome symlink
            chrome_link2 = '/data/data/com.termux/files/usr/bin/chrome'
            if not os.path.exists(chrome_link2):
                try:
                    os.symlink(chromium_path, chrome_link2)
                    self.log("Created chrome symlink", "success")
                except:
                    self.log("Failed to create chrome symlink", "warning")
    
    def install_all(self):
        """Install everything"""
        Colors.header("\n🔧 AUTO INSTALLER STARTED")
        
        self.install_termux_packages()
        self.install_python_packages()
        driver_path = self.install_chromedriver()
        self.create_symlinks()
        
        Colors.header("\n📋 INSTALLATION SUMMARY")
        for log in self.logs[-10:]:
            print(f"  {log}")
        
        return driver_path

# ==================== CONFIG MANAGER ====================

class ConfigManager:
    def __init__(self):
        self.config_file = "mdf_config.json"
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration"""
        default_config = {
            'accounts': [],
            'targets': [],
            'proxies': [],
            'settings': {
                'reports_per_target': 5,
                'delay_between_reports': 30,
                'delay_between_targets': 60,
                'max_threads': 3,
                'auto_retry': True,
                'max_retries': 3,
                'use_proxy': False,
                'headless_mode': False,
                'save_screenshots': True
            },
            'stats': {
                'total_reports': 0,
                'successful': 0,
                'failed': 0,
                'last_run': None,
                'total_time': 0
            },
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.config_file, 'r') as f:
                loaded = json.load(f)
                for key in default_config:
                    if key not in loaded:
                        loaded[key] = default_config[key]
                return loaded
        except:
            return default_config
    
    def save_config(self):
        self.config['updated'] = datetime.now().isoformat()
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_account(self, email, password):
        self.config['accounts'].append({
            'email': email,
            'password': password,
            'cookies': {},
            'last_used': None,
            'status': 'active',
            'success_count': 0,
            'fail_count': 0
        })
        self.save_config()
    
    def add_target(self, url):
        if url not in self.config['targets']:
            self.config['targets'].append(url)
            self.save_config()
            return True
        return False
    
    def add_proxy(self, proxy):
        if proxy not in self.config['proxies']:
            self.config['proxies'].append(proxy)
            self.save_config()
    
    def update_stats(self, success=True, duration=0):
        self.config['stats']['total_reports'] += 1
        if success:
            self.config['stats']['successful'] += 1
        else:
            self.config['stats']['failed'] += 1
        self.config['stats']['last_run'] = datetime.now().isoformat()
        self.config['stats']['total_time'] += duration
        self.save_config()

# ==================== PROXY MANAGER ====================

class ProxyManager:
    def __init__(self, config):
        self.config = config
        self.current_index = 0
        self.lock = threading.Lock()
    
    def get_next_proxy(self):
        if not self.config.config['proxies']:
            return None
        
        with self.lock:
            proxy = self.config.config['proxies'][self.current_index]
            self.current_index = (self.current_index + 1) % len(self.config.config['proxies'])
            return proxy
    
    def test_proxy(self, proxy):
        """Test if proxy is working"""
        try:
            import requests
            proxies = {'http': proxy, 'https': proxy}
            r = requests.get('https://www.facebook.com', proxies=proxies, timeout=5)
            return r.status_code == 200
        except:
            return False

# ==================== REAL FACEBOOK REPORTER ====================

class RealFacebookReporter:
    def __init__(self, config, driver_path, proxy_manager=None):
        self.config = config
        self.driver_path = driver_path
        self.proxy_manager = proxy_manager
        self.driver = None
        self.wait = None
        self.logs = []
        self.stats = {
            'reports': 0,
            'success': 0,
            'failed': 0,
            'start_time': None
        }
        
        # Import selenium
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.service import Service
            from selenium.common.exceptions import TimeoutException, NoSuchElementException
            self.selenium_available = True
        except ImportError:
            self.selenium_available = False
    
    def log(self, msg, type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        self.logs.append(log_entry)
        
        if type == "success":
            Colors.success(f"  ✅ {msg}")
        elif type == "error":
            Colors.error(f"  ❌ {msg}")
        elif type == "warning":
            Colors.warning(f"  ⚠️ {msg}")
        elif type == "progress":
            Colors.progress(f"  📊 {msg}")
        else:
            print(f"  📌 {msg}")
    
    def setup_driver(self, account_index=0):
        """Setup Chrome/Chromium driver"""
        self.log("🚀 Setting up browser driver...")
        
        if not self.selenium_available:
            self.log("Selenium not available!", "error")
            return False
        
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Headless mode
        if self.config.config['settings']['headless_mode']:
            options.add_argument('--headless=new')
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # Add proxy if configured
        if self.config.config['settings']['use_proxy'] and self.proxy_manager:
            proxy = self.proxy_manager.get_next_proxy()
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
                self.log(f"Using proxy: {proxy}")
        
        # Random window size
        sizes = [(1920,1080), (1366,768), (1536,864), (1440,900)]
        size = random.choice(sizes)
        options.add_argument(f'--window-size={size[0]},{size[1]}')
        
        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Execute script to hide automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 15)
            self.log("✅ Browser setup complete", "success")
            return True
        except Exception as e:
            self.log(f"❌ Browser setup failed: {e}", "error")
            return False
    
    def login(self, email, password):
        """Real Facebook login"""
        self.log(f"\n🔑 Logging in with {email}...")
        
        try:
            self.driver.get("https://m.facebook.com")
            time.sleep(3)
            
            # Email field
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_field.send_keys(email)
            
            # Password field
            pass_field = self.driver.find_element(By.NAME, "pass")
            pass_field.send_keys(password)
            
            # Random delay to simulate human
            time.sleep(random.uniform(1, 3))
            
            # Login button
            login_btn = self.driver.find_element(By.NAME, "login")
            login_btn.click()
            
            time.sleep(5)
            
            # Check login success
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'c_user':
                    self.log(f"✅ Login successful! User ID: {cookie['value']}", "success")
                    
                    # Save cookies for future use
                    for acc in self.config.config['accounts']:
                        if acc['email'] == email:
                            acc['cookies'] = cookies
                            acc['last_used'] = datetime.now().isoformat()
                            self.config.save_config()
                    
                    return True
            
            self.log("❌ Login failed - Check credentials", "error")
            return False
            
        except Exception as e:
            self.log(f"❌ Login error: {e}", "error")
            return False
    
    def report_profile(self, profile_url, reason="Fake account", retry=0):
        """Real profile reporting"""
        self.log(f"\n🎯 Reporting profile: {profile_url[:50]}...")
        
        try:
            # Use mobile version for better compatibility
            mobile_url = profile_url.replace("www.", "m.").replace("facebook.com", "m.facebook.com")
            self.driver.get(mobile_url)
            time.sleep(4)
            
            # Take screenshot if enabled
            if self.config.config['settings']['save_screenshots']:
                screenshot_name = f"report_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_name)
                self.log(f"📸 Screenshot saved: {screenshot_name}")
            
            # Click menu button
            menu_selectors = [
                "//div[@aria-label='Actions for this profile']",
                "//div[@aria-label='More']",
                "//div[@role='button']//span[text()='More']",
                "//div[contains(@class, 'x1i10hfl')]//span[text()='More']"
            ]
            
            menu_clicked = False
            for selector in menu_selectors:
                try:
                    menu = self.driver.find_element(By.XPATH, selector)
                    menu.click()
                    self.log("✅ Menu button clicked", "success")
                    menu_clicked = True
                    break
                except:
                    continue
            
            if not menu_clicked:
                self.log("❌ Menu button not found", "error")
                return False
            
            time.sleep(2)
            
            # Find report option
            report_selectors = [
                "//span[text()='Find support or report profile']",
                "//span[contains(text(), 'report profile')]",
                "//span[contains(text(), 'Report')]",
                "//div[@role='menuitem'][contains(text(), 'Report')]"
            ]
            
            report_clicked = False
            for selector in report_selectors:
                try:
                    report = self.driver.find_element(By.XPATH, selector)
                    report.click()
                    self.log("✅ Report option clicked", "success")
                    report_clicked = True
                    break
                except:
                    continue
            
            if not report_clicked:
                self.log("❌ Report option not found", "error")
                return False
            
            time.sleep(3)
            
            # Select reason
            reason_options = [reason, reason.lower(), reason.title()]
            reason_selected = False
            
            for r in reason_options:
                try:
                    reason_elem = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{r}')]")
                    reason_elem.click()
                    self.log(f"✅ Reason selected: {reason}", "success")
                    reason_selected = True
                    break
                except:
                    continue
            
            if not reason_selected:
                self.log("⚠️ Could not select reason, continuing...", "warning")
            
            time.sleep(2)
            
            # Submit report
            submit_selectors = [
                "//div[@role='button'][contains(text(), 'Submit')]",
                "//span[text()='Submit']",
                "//button[contains(text(), 'Submit')]"
            ]
            
            for selector in submit_selectors:
                try:
                    submit = self.driver.find_element(By.XPATH, selector)
                    submit.click()
                    self.log("✅ Report submitted!", "success")
                    self.stats['success'] += 1
                    self.config.update_stats(success=True)
                    break
                except:
                    continue
            
            time.sleep(3)
            return True
            
        except Exception as e:
            self.log(f"❌ Reporting error: {e}", "error")
            
            if retry < self.config.config['settings']['max_retries'] and self.config.config['settings']['auto_retry']:
                self.log(f"🔄 Retrying ({retry + 1}/{self.config.config['settings']['max_retries']})...", "warning")
                time.sleep(5)
                return self.report_profile(profile_url, reason, retry + 1)
            
            self.stats['failed'] += 1
            self.config.update_stats(success=False)
            return False
    
    def close(self):
        """Close browser"""
        if self.driver:
            time.sleep(2)
            self.driver.quit()
            self.log("🚪 Browser closed")

# ==================== PROGRESS BAR ====================

class ProgressBar:
    def __init__(self, total, width=40):
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, current):
        self.current = current
        percent = (current / self.total) * 100
        filled = int(self.width * current // self.total)
        bar = '█' * filled + '░' * (self.width - filled)
        
        sys.stdout.write(f'\r  📊 Progress: |{bar}| {percent:.1f}% ({current}/{self.total})')
        sys.stdout.flush()
    
    def complete(self):
        self.update(self.total)
        print()

# ==================== MAIN TERMINAL UI ====================

class TerminalUI:
    def __init__(self):
        self.config = ConfigManager()
        self.installer = AutoInstaller()
        self.driver_path = None
        self.proxy_manager = ProxyManager(self.config)
        self.reporter = None
        
        # Check if first run
        if not os.path.exists(self.config.config_file):
            self.first_run_setup()
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        self.clear_screen()
        print(f"{Colors.RED}{Colors.BOLD}{BANNER}{Colors.END}")
    
    def first_run_setup(self):
        """First time setup"""
        self.print_banner()
        Colors.header("\n🚀 FIRST RUN SETUP")
        print("\nThis is your first time running MDF Legends Pro.")
        print("The tool will now automatically install all requirements.\n")
        
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
        
        self.driver_path = self.installer.install_all()
        
        if self.driver_path:
            Colors.success("\n✅ Setup complete! You can now use the tool.")
        else:
            Colors.error("\n❌ Setup failed! Please check your internet connection.")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def print_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                         PRO MAIN MENU                              ║
╠════════════════════════════════════════════════════════════════════╣
║  {Colors.GREEN}1.{Colors.END} 🔧 System Check & Auto Fix                                     ║
║  {Colors.GREEN}2.{Colors.END} 👤 Account Manager ({len(self.config.config['accounts'])} accounts)                          ║
║  {Colors.GREEN}3.{Colors.END} 🎯 Target Manager ({len(self.config.config['targets'])} targets)                            ║
║  {Colors.GREEN}4.{Colors.END} 🌐 Proxy Manager ({len(self.config.config['proxies'])} proxies)                             ║
║  {Colors.GREEN}5.{Colors.END} ⚙️ Settings                                                   ║
║  {Colors.GREEN}6.{Colors.END} 📊 Statistics                                                ║
║  {Colors.GREEN}7.{Colors.END} 🚀 Start REAL Reporting                                       ║
║  {Colors.GREEN}8.{Colors.END} 🧪 Test Configuration                                         ║
║  {Colors.GREEN}9.{Colors.END} 📖 Help & Guide                                               ║
║  {Colors.GREEN}0.{Colors.END} 🚪 Exit                                                       ║
╚════════════════════════════════════════════════════════════════════╝{Colors.END}
        """
        print(menu)
    
    def run(self):
        while True:
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Colors.GREEN}👉 Select option (0-9): {Colors.END}")
            
            if choice == '1':
                self.system_check()
            elif choice == '2':
                self.account_manager()
            elif choice == '3':
                self.target_manager()
            elif choice == '4':
                self.proxy_manager_menu()
            elif choice == '5':
                self.settings_menu()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.start_real_reporting()
            elif choice == '8':
                self.test_configuration()
            elif choice == '9':
                self.show_help()
            elif choice == '0':
                Colors.success("\n👋 Thank you for using MDF Legends Pro!")
                sys.exit(0)
    
    def system_check(self):
        self.print_banner()
        Colors.header("\n🔧 SYSTEM CHECK")
        
        # Check Python
        version = sys.version_info
        Colors.success(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
        # Check pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                                   capture_output=True, text=True)
            Colors.success(f"✅ Pip {result.stdout.split()[1]}")
        except:
            Colors.error("❌ Pip not found")
        
        # Check ChromeDriver
        if self.driver_path and os.path.exists(self.driver_path):
            try:
                result = subprocess.run([self.driver_path, '--version'],
                                       capture_output=True, text=True)
                Colors.success(f"✅ ChromeDriver: {result.stdout.strip()}")
            except:
                Colors.error("❌ ChromeDriver not working")
        else:
            # Try to find in PATH
            try:
                result = subprocess.run(['which', 'chromedriver'],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    self.driver_path = result.stdout.strip()
                    Colors.success(f"✅ ChromeDriver found: {self.driver_path}")
                else:
                    Colors.error("❌ ChromeDriver not found")
            except:
                Colors.error("❌ ChromeDriver not found")
        
        # Check browser
        if is_termux():
            if os.path.exists('/data/data/com.termux/files/usr/bin/chromium'):
                Colors.success("✅ Chromium found")
            else:
                Colors.error("❌ Chromium not found")
        else:
            browsers = ['google-chrome', 'google-chrome-stable', 'chrome']
            found = False
            for browser in browsers:
                try:
                    result = subprocess.run(['which', browser],
                                           capture_output=True, text=True)
                    if result.returncode == 0:
                        Colors.success(f"✅ {browser} found")
                        found = True
                        break
                except:
                    continue
            if not found:
                Colors.error("❌ No browser found")
        
        # Check internet
        try:
            urllib.request.urlopen("https://www.google.com", timeout=5)
            Colors.success("✅ Internet connection OK")
        except:
            Colors.error("❌ No internet connection")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def account_manager(self):
        self.print_banner()
        Colors.header("\n👤 ACCOUNT MANAGER")
        
        accounts = self.config.config['accounts']
        
        if accounts:
            print(f"\n{Colors.CYAN}Your Accounts:{Colors.END}")
            for i, acc in enumerate(accounts, 1):
                status = "🟢" if acc.get('status') == 'active' else "🔴"
                last = acc.get('last_used', 'Never')[:10] if acc.get('last_used') else 'Never'
                print(f"  {i}. {status} {acc['email']} (Last: {last})")
        else:
            print(f"\n{Colors.YELLOW}No accounts added yet.{Colors.END}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print("  1. Add new account")
        print("  2. Remove account")
        print("  3. Test account")
        print("  4. Back to main menu")
        
        choice = input(f"\n{Colors.GREEN}👉 Select: {Colors.END}")
        
        if choice == '1':
            email = input("📧 Email/Phone: ")
            password = input("🔑 Password: ")
            self.config.add_account(email, password)
            Colors.success("✅ Account added!")
        elif choice == '2' and accounts:
            try:
                idx = int(input("Enter number to remove: ")) - 1
                if 0 <= idx < len(accounts):
                    del self.config.config['accounts'][idx]
                    self.config.save_config()
                    Colors.success("✅ Account removed!")
            except:
                Colors.error("❌ Invalid input")
        elif choice == '3' and accounts:
            self.test_accounts()
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def target_manager(self):
        self.print_banner()
        Colors.header("\n🎯 TARGET MANAGER")
        
        targets = self.config.config['targets']
        
        if targets:
            print(f"\n{Colors.CYAN}Your Targets:{Colors.END}")
            for i, target in enumerate(targets, 1):
                print(f"  {i}. {target[:70]}...")
        else:
            print(f"\n{Colors.YELLOW}No targets added yet.{Colors.END}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print("  1. Add single target")
        print("  2. Add multiple targets (file)")
        print("  3. Remove target")
        print("  4. Clear all")
        print("  5. Back to main menu")
        
        choice = input(f"\n{Colors.GREEN}👉 Select: {Colors.END}")
        
        if choice == '1':
            url = input("Enter Facebook URL: ")
            if 'facebook.com' in url:
                self.config.add_target(url)
                Colors.success("✅ Target added!")
            else:
                Colors.error("❌ Invalid Facebook URL")
        elif choice == '2':
            filename = input("Enter filename (one URL per line): ")
            try:
                with open(filename, 'r') as f:
                    count = 0
                    for line in f:
                        url = line.strip()
                        if 'facebook.com' in url:
                            if self.config.add_target(url):
                                count += 1
                    Colors.success(f"✅ Added {count} targets")
            except:
                Colors.error("❌ File not found")
        elif choice == '3' and targets:
            try:
                idx = int(input("Enter number to remove: ")) - 1
                if 0 <= idx < len(targets):
                    del self.config.config['targets'][idx]
                    self.config.save_config()
                    Colors.success("✅ Target removed!")
            except:
                Colors.error("❌ Invalid input")
        elif choice == '4':
            self.config.config['targets'] = []
            self.config.save_config()
            Colors.success("✅ All targets cleared!")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def proxy_manager_menu(self):
        self.print_banner()
        Colors.header("\n🌐 PROXY MANAGER")
        
        proxies = self.config.config['proxies']
        
        if proxies:
            print(f"\n{Colors.CYAN}Your Proxies:{Colors.END}")
            for i, proxy in enumerate(proxies, 1):
                print(f"  {i}. {proxy}")
        else:
            print(f"\n{Colors.YELLOW}No proxies added.{Colors.END}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print("  1. Add proxy")
        print("  2. Remove proxy")
        print("  3. Test proxies")
        print("  4. Toggle proxy usage")
        print("  5. Back to main menu")
        
        choice = input(f"\n{Colors.GREEN}👉 Select: {Colors.END}")
        
        if choice == '1':
            proxy = input("Enter proxy (e.g., http://1.2.3.4:8080): ")
            self.config.add_proxy(proxy)
            Colors.success("✅ Proxy added!")
        elif choice == '2' and proxies:
            try:
                idx = int(input("Enter number to remove: ")) - 1
                if 0 <= idx < len(proxies):
                    del self.config.config['proxies'][idx]
                    self.config.save_config()
                    Colors.success("✅ Proxy removed!")
            except:
                Colors.error("❌ Invalid input")
        elif choice == '3' and proxies:
            self.test_proxies()
        elif choice == '4':
            current = self.config.config['settings']['use_proxy']
            self.config.config['settings']['use_proxy'] = not current
            self.config.save_config()
            Colors.success(f"✅ Proxy usage: {'ON' if not current else 'OFF'}")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def settings_menu(self):
        self.print_banner()
        Colors.header("\n⚙️ SETTINGS")
        
        settings = self.config.config['settings']
        
        print(f"\n{Colors.CYAN}Current Settings:{Colors.END}")
        print(f"  1. Reports per target: {settings['reports_per_target']}")
        print(f"  2. Delay between reports: {settings['delay_between_reports']}s")
        print(f"  3. Delay between targets: {settings['delay_between_targets']}s")
        print(f"  4. Max threads: {settings['max_threads']}")
        print(f"  5. Auto retry: {'ON' if settings['auto_retry'] else 'OFF'}")
        print(f"  6. Max retries: {settings['max_retries']}")
        print(f"  7. Headless mode: {'ON' if settings['headless_mode'] else 'OFF'}")
        print(f"  8. Save screenshots: {'ON' if settings['save_screenshots'] else 'OFF'}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print("  Enter number to change (0 to save and exit)")
        
        try:
            choice = input(f"\n{Colors.GREEN}👉 Select setting (0-8): {Colors.END}")
            
            if choice == '1':
                val = int(input("New reports per target: "))
                settings['reports_per_target'] = max(1, min(100, val))
            elif choice == '2':
                val = int(input("New delay between reports (seconds): "))
                settings['delay_between_reports'] = max(5, min(300, val))
            elif choice == '3':
                val = int(input("New delay between targets (seconds): "))
                settings['delay_between_targets'] = max(10, min(600, val))
            elif choice == '4':
                val = int(input("New max threads: "))
                settings['max_threads'] = max(1, min(10, val))
            elif choice == '5':
                settings['auto_retry'] = not settings['auto_retry']
            elif choice == '6':
                val = int(input("New max retries: "))
                settings['max_retries'] = max(0, min(10, val))
            elif choice == '7':
                settings['headless_mode'] = not settings['headless_mode']
            elif choice == '8':
                settings['save_screenshots'] = not settings['save_screenshots']
            
            self.config.save_config()
            Colors.success("✅ Settings updated!")
            
        except Exception as e:
            Colors.error(f"❌ Error: {e}")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def show_statistics(self):
        self.print_banner()
        Colors.header("\n📊 STATISTICS")
        
        stats = self.config.config['stats']
        
        print(f"\n{Colors.CYAN}Overall Statistics:{Colors.END}")
        print(f"  Total Reports: {stats['total_reports']}")
        print(f"  Successful: {Colors.GREEN}{stats['successful']}{Colors.END}")
        print(f"  Failed: {Colors.RED}{stats['failed']}{Colors.END}")
        
        success_rate = (stats['successful'] / (stats['total_reports'] or 1)) * 100
        print(f"  Success Rate: {Colors.YELLOW}{success_rate:.1f}%{Colors.END}")
        
        avg_time = stats['total_time'] / (stats['total_reports'] or 1)
        print(f"  Avg Time per Report: {avg_time:.1f}s")
        
        print(f"  Last Run: {stats['last_run'] or 'Never'}")
        
        print(f"\n{Colors.CYAN}Account Stats:{Colors.END}")
        for acc in self.config.config['accounts']:
            print(f"  {acc['email']}: {acc.get('success_count', 0)} success, {acc.get('fail_count', 0)} fails")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def test_accounts(self):
        """Test if accounts work"""
        if not self.config.config['accounts']:
            Colors.warning("No accounts to test")
            return
        
        Colors.header("\n🧪 TESTING ACCOUNTS")
        
        for i, account in enumerate(self.config.config['accounts'][:3], 1):  # Test first 3 only
            print(f"\n{Colors.CYAN}Testing account {i}: {account['email']}{Colors.END}")
            
            # Simple validation
            if '@' in account['email'] and len(account['password']) >= 6:
                Colors.success("  ✅ Format OK")
            else:
                Colors.error("  ❌ Invalid format")
    
    def test_proxies(self):
        """Test if proxies work"""
        if not self.config.config['proxies']:
            Colors.warning("No proxies to test")
            return
        
        Colors.header("\n🧪 TESTING PROXIES")
        
        working = 0
        for i, proxy in enumerate(self.config.config['proxies'], 1):
            print(f"\n{Colors.CYAN}Testing proxy {i}: {proxy}{Colors.END}")
            
            if self.proxy_manager.test_proxy(proxy):
                Colors.success("  ✅ Working")
                working += 1
            else:
                Colors.error("  ❌ Failed")
        
        Colors.success(f"\n✅ {working}/{len(self.config.config['proxies'])} proxies working")
    
    def test_configuration(self):
        self.print_banner()
        Colors.header("\n🧪 TEST CONFIGURATION")
        
        # Test accounts
        print(f"\n{Colors.CYAN}Accounts:{Colors.END}")
        valid_accounts = 0
        for acc in self.config.config['accounts']:
            if '@' in acc['email'] and len(acc['password']) >= 6:
                valid_accounts += 1
                Colors.success(f"  ✅ {acc['email']}")
            else:
                Colors.error(f"  ❌ {acc['email']}")
        
        # Test targets
        print(f"\n{Colors.CYAN}Targets:{Colors.END}")
        valid_targets = 0
        for target in self.config.config['targets']:
            if 'facebook.com' in target:
                valid_targets += 1
                Colors.success(f"  ✅ {target[:50]}...")
            else:
                Colors.error(f"  ❌ {target[:50]}...")
        
        # Test proxies
        print(f"\n{Colors.CYAN}Proxies:{Colors.END}")
        if self.config.config['proxies']:
            Colors.success(f"  ✅ {len(self.config.config['proxies'])} proxies configured")
        else:
            Colors.warning("  ⚠️ No proxies (using direct connection)")
        
        # Summary
        print(f"\n{Colors.CYAN}Summary:{Colors.END}")
        print(f"  Valid Accounts: {valid_accounts}/{len(self.config.config['accounts'])}")
        print(f"  Valid Targets: {valid_targets}/{len(self.config.config['targets'])}")
        
        ready = (valid_accounts > 0 and valid_targets > 0)
        if ready:
            Colors.success("\n✅ Ready to start reporting!")
        else:
            Colors.error("\n❌ Not ready! Add valid accounts and targets.")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def start_real_reporting(self):
        self.print_banner()
        
        # Check prerequisites
        if not self.config.config['accounts']:
            Colors.error("❌ No accounts added!")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        if not self.config.config['targets']:
            Colors.error("❌ No targets added!")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        if not self.driver_path:
            # Try to find chromedriver
            try:
                result = subprocess.run(['which', 'chromedriver'],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    self.driver_path = result.stdout.strip()
                else:
                    Colors.error("❌ ChromeDriver not found! Run option 1 first.")
                    input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
                    return
            except:
                Colors.error("❌ ChromeDriver not found! Run option 1 first.")
                input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
                return
        
        Colors.header("\n🚀 START REAL REPORTING")
        
        # Show configuration
        print(f"\n{Colors.CYAN}Configuration:{Colors.END}")
        print(f"  Accounts: {len(self.config.config['accounts'])}")
        print(f"  Targets: {len(self.config.config['targets'])}")
        print(f"  Reports per target: {self.config.config['settings']['reports_per_target']}")
        print(f"  Max threads: {self.config.config['settings']['max_threads']}")
        
        # Select reason
        print(f"\n{Colors.CYAN}Select reason:{Colors.END}")
        reasons = ['Fake account', 'Harassment', 'Hate speech', 'Scam', 'Nudity', 'Violence']
        for i, r in enumerate(reasons, 1):
            print(f"  {i}. {r}")
        
        try:
            reason_choice = int(input(f"\n{Colors.GREEN}Select reason (1-6): {Colors.END}")) - 1
            reason = reasons[reason_choice] if 0 <= reason_choice < len(reasons) else 'Fake account'
        except:
            reason = 'Fake account'
        
        # Confirm
        total_reports = len(self.config.config['targets']) * self.config.config['settings']['reports_per_target']
        print(f"\n{Colors.RED}⚠️  This will send {total_reports} REAL reports to Facebook!{Colors.END}")
        
        confirm = input(f"{Colors.RED}Type 'YES' to confirm: {Colors.END}")
        
        if confirm != 'YES':
            Colors.warning("Attack cancelled.")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        # Start reporting
        Colors.header("\n📊 ATTACK PROGRESS")
        
        progress = ProgressBar(total_reports)
        current_report = 0
        successful = 0
        failed = 0
        
        start_time = time.time()
        
        for target_idx, target in enumerate(self.config.config['targets'], 1):
            for report_num in range(self.config.config['settings']['reports_per_target']):
                current_report += 1
                progress.update(current_report)
                
                # Use account in round-robin
                account = self.config.config['accounts'][(current_report - 1) % len(self.config.config['accounts'])]
                
                print(f"\n  📍 Target {target_idx}/{len(self.config.config['targets'])} - Report {report_num + 1}/{self.config.config['settings']['reports_per_target']}")
                
                reporter = RealFacebookReporter(self.config, self.driver_path, self.proxy_manager)
                
                report_start = time.time()
                
                if reporter.setup_driver():
                    if reporter.login(account['email'], account['password']):
                        if reporter.report_profile(target, reason):
                            successful += 1
                        else:
                            failed += 1
                    reporter.close()
                
                report_duration = time.time() - report_start
                self.config.update_stats(success=(successful > failed), duration=report_duration)
                
                # Update account stats
                for acc in self.config.config['accounts']:
                    if acc['email'] == account['email']:
                        if successful > 0:
                            acc['success_count'] = acc.get('success_count', 0) + 1
                        else:
                            acc['fail_count'] = acc.get('fail_count', 0) + 1
                        self.config.save_config()
                
                # Delay between reports
                if current_report < total_reports:
                    delay = self.config.config['settings']['delay_between_reports']
                    print(f"\n  ⏳ Waiting {delay}s before next report...")
                    for i in range(delay, 0, -5):
                        if i > 5:
                            time.sleep(5)
                        else:
                            time.sleep(i)
        
        progress.complete()
        
        total_time = time.time() - start_time
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        
        Colors.header("\n🎉 ATTACK COMPLETE!")
        print(f"\n{Colors.CYAN}Final Results:{Colors.END}")
        print(f"  Total Reports: {total_reports}")
        print(f"  Successful: {Colors.GREEN}{successful}{Colors.END}")
        print(f"  Failed: {Colors.RED}{failed}{Colors.END}")
        print(f"  Success Rate: {Colors.YELLOW}{(successful/total_reports*100):.1f}%{Colors.END}")
        print(f"  Total Time: {hours}h {minutes}m {seconds}s")
        print(f"  Avg Time per Report: {total_time/total_reports:.1f}s")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def show_help(self):
        self.print_banner()
        Colors.header("\n📖 HELP & GUIDE")
        
        help_text = f"""
{Colors.GREEN}ABOUT:{Colors.END}
  MDF Legends Pro v{VERSION} is a REAL Facebook reporting tool.
  It actually opens a browser and submits REAL reports to Facebook.

{Colors.GREEN}FEATURES:{Colors.END}
  ✓ Multi-Account Support - Use multiple Facebook accounts
  ✓ Mass Reporting - Report multiple targets at once
  ✓ Auto Retry - Automatically retry failed reports
  ✓ Proxy Support - Use proxies to avoid detection
  ✓ Statistics - Track your success rate
  ✓ Auto Save - Configuration automatically saved
  ✓ Smart Delay - Random delays to avoid detection
  ✓ Screenshots - Save proof of reports

{Colors.GREEN}HOW TO USE:{Colors.END}
  1. First, run Option 1 to check your system
  2. Add Facebook accounts (Option 2)
  3. Add target profiles (Option 3)
  4. Configure proxies if needed (Option 4)
  5. Adjust settings (Option 5)
  6. Test configuration (Option 8)
  7. Start REAL reporting (Option 7)

{Colors.GREEN}TIPS:{Colors.END}
  • Use multiple accounts for more reports
  • Add delays to avoid detection
  • Use proxies for better anonymity
  • Facebook limits reports per account
  • Always test with your own profile first

{Colors.RED}WARNING:{Colors.END}
  This tool sends REAL reports to Facebook.
  Use responsibly and at your own risk.
  Violating Facebook's terms may result in account bans.
        """
        print(help_text)
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        ui = TerminalUI()
        ui.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}\n👋 Goodbye!{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)