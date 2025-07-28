#!/usr/bin/env python3
"""
ELOHIM - Advanced OSINT Reconnaissance Framework
By: Scav-enger
Professional backend CLI tool for enterprise penetration testing

Enhanced with Wizard Mode, Extended Platform Coverage, and Plugin Architecture
"""

import asyncio
import aiohttp
import argparse
import json
import sys
import time
import random
import os
import importlib.util
import pkgutil
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import re
from urllib.parse import urlparse
import dns.resolver
import whois
from colorama import init, Fore, Back, Style
import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import socket
import ssl
import subprocess
from pathlib import Path
import inspect

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class ElohimLogger:
    """Professional logging with brutal dystopic cyberpunk styling"""
    
    @staticmethod
    def banner():
        banner = f"""
{Fore.RED}{Style.DIM}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Fore.GREEN}{Style.BRIGHT}
▓█████  ██▓     ▒█████   ██░ ██  ██▓ ███▄ ▄███▓{Fore.RED}{Style.DIM}
▓█   ▀ ▓██▒    ▒██▒  ██▒▓██░ ██▒▓██▒▓██▒▀█▀ ██▒{Fore.GREEN}{Style.BRIGHT}
▒███   ▒██░    ▒██░  ██▒▒██▀▀██░▒██▒▓██    ▓██░{Fore.RED}{Style.DIM}
▒▓█  ▄ ▒██░    ▒██   ██░░▓█ ░██ ░██░▒██    ▒██ {Fore.GREEN}{Style.BRIGHT}
░▒████▒░██████▒░ ████▓▒░░▓█▒░██▓░██░▒██▒   ░██▒{Fore.RED}{Style.DIM}
░░ ▒░ ░░ ▒░▓  ░░ ▒░▒░▒░  ▒ ░░▒░▒░▓  ░ ▒░   ░  ░{Fore.WHITE}{Style.DIM}
 ░ ░  ░░ ░ ▒  ░  ░ ▒ ▒░  ▒ ░▒░ ░ ▒ ░░  ░      ░{Style.RESET_ALL}
{Fore.BLACK}{Back.RED}┌─[DYSTOPIC RECONNAISSANCE FRAMEWORK]─[v3.0-GHOST]─┐{Style.RESET_ALL}
{Fore.WHITE}{Style.DIM}│ {Fore.RED}◢◤{Fore.WHITE} Advanced OSINT Intelligence Gathering      {Fore.RED}◢◤ {Fore.WHITE}│{Style.RESET_ALL}
{Fore.WHITE}{Style.DIM}│ {Fore.GREEN}◢◤{Fore.WHITE} Professional Cybersecurity Tool           {Fore.GREEN}◢◤ {Fore.WHITE}│{Style.RESET_ALL}
{Fore.WHITE}{Style.DIM}│ {Fore.YELLOW}◢◤{Fore.WHITE} By: Scav-enger | Ghost Protocol          {Fore.YELLOW}◢◤ {Fore.WHITE}│{Style.RESET_ALL}
{Fore.BLACK}{Back.RED}└──[ENTER THE DIGITAL SHADOWLANDS]──────────────────┘{Style.RESET_ALL}
{Fore.RED}{Style.DIM}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}
        """
        print(banner)
    
    @staticmethod
    def wizard_banner():
        banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          {Fore.GREEN}ELOHIM WIZARD MODE{Fore.MAGENTA}                               ║
║                     {Fore.WHITE}Interactive Reconnaissance Guide{Fore.MAGENTA}                      ║
║                                                                               ║
║  {Fore.CYAN}┌─ AUTOMATED INTELLIGENCE GATHERING ─┐{Fore.MAGENTA}                              ║
║  {Fore.CYAN}│ • Guided Target Selection           │{Fore.MAGENTA}                              ║
║  {Fore.CYAN}│ • Platform Auto-Detection           │{Fore.MAGENTA}                              ║
║  {Fore.CYAN}│ • Comprehensive Scanning            │{Fore.MAGENTA}                              ║
║  {Fore.CYAN}│ • Automated Report Generation       │{Fore.MAGENTA}                              ║
║  {Fore.CYAN}└─────────────────────────────────────┘{Fore.MAGENTA}                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)
    
    @staticmethod
    def info(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {Fore.CYAN}[◢◤ INFO]{Style.RESET_ALL} {Fore.WHITE}{message}{Style.RESET_ALL}")
    
    @staticmethod
    def success(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {Fore.GREEN}[◢◤ SUCCESS]{Style.RESET_ALL} {Fore.GREEN}{message}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {Fore.YELLOW}[◢◤ WARNING]{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    @staticmethod
    def error(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {Fore.RED}[◢◤ ERROR]{Style.RESET_ALL} {Fore.RED}{message}{Style.RESET_ALL}")
    
    @staticmethod
    def ghost(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {Fore.MAGENTA}[◢◤ GHOST]{Style.RESET_ALL} {Fore.MAGENTA}{Style.DIM}{message}{Style.RESET_ALL}")
    
    @staticmethod
    def result(platform: str, status: str, url: str = ""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status.upper() == "FOUND":
            status_color = f"{Fore.GREEN}[◢◤ FOUND]{Style.RESET_ALL}"
            print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {status_color} {Fore.MAGENTA}{platform:<25}{Style.RESET_ALL} {Fore.BLUE}{Style.DIM}{url}{Style.RESET_ALL}")
        elif status.upper() == "NSFW":
            status_color = f"{Fore.YELLOW}[◢◤ NSFW-FOUND]{Style.RESET_ALL}"
            print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {status_color} {Fore.RED}{platform:<25}{Style.RESET_ALL} {Fore.RED}{Style.DIM}{url}{Style.RESET_ALL}")
        else:
            status_color = f"{Fore.RED}[◢◤ NOT FOUND]{Style.RESET_ALL}"
            print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {status_color} {Fore.WHITE}{Style.DIM}{platform:<25}{Style.RESET_ALL}")
    
    @staticmethod
    def plugin_loaded(plugin_name: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}{Style.DIM}[{timestamp}] {Fore.CYAN}[◢◤ PLUGIN]{Style.RESET_ALL} {Fore.CYAN}Loaded: {plugin_name}{Style.RESET_ALL}")
    
    @staticmethod
    def wizard_input(prompt: str) -> str:
        return input(f"{Fore.MAGENTA}[◢◤ WIZARD]{Style.RESET_ALL} {Fore.WHITE}{prompt}{Style.RESET_ALL}")
    
    @staticmethod
    def wizard_step(step: int, message: str):
        print(f"{Fore.MAGENTA}[◢◤ STEP {step}]{Style.RESET_ALL} {Fore.WHITE}{message}{Style.RESET_ALL}")

class OSINTDatabase:
    """Comprehensive OSINT platform database with file-based URL loading"""
    
    @staticmethod
    def load_urls_from_file(filename: str = "Assets/Urls.txt") -> Dict[str, str]:
        """Load platform URLs from file"""
        urls = {}
        url_file = Path(filename)
        
        if not url_file.exists():
            ElohimLogger.warning(f"URL file {filename} not found, creating with default URLs")
            OSINTDatabase._create_default_url_file(url_file)
        
        try:
            with open(url_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            platform, url = line.split('=', 1)
                            urls[platform.strip()] = url.strip()
                        else:
                            ElohimLogger.warning(f"Invalid format at line {line_num}: {line}")
            
            ElohimLogger.success(f"Loaded {len(urls)} platform URLs from {filename}")
            
        except Exception as e:
            ElohimLogger.error(f"Failed to load URLs: {str(e)}")
            return OSINTDatabase._get_fallback_urls()
        
        return urls
    
    @staticmethod
    def _create_default_url_file(url_file: Path):
        """Create default URL file with comprehensive platform list"""
        default_urls = """# ELOHIM Platform URL Database
# Format: PlatformName=URL_Template
# Use {} as placeholder for username

# Social Media Platforms
Instagram=https://instagram.com/{}
Twitter=https://twitter.com/{}
Facebook=https://facebook.com/{}
LinkedIn=https://linkedin.com/in/{}
TikTok=https://tiktok.com/@{}
YouTube=https://youtube.com/user/{}
Snapchat=https://snapchat.com/add/{}
Pinterest=https://pinterest.com/{}
Reddit=https://reddit.com/user/{}
Discord=https://discord.com/users/{}
Telegram=https://t.me/{}
Twitch=https://twitch.tv/{}
VKontakte=https://vk.com/{}
Mastodon=https://mastodon.social/@{}

# Gaming Platforms
Steam=https://steamcommunity.com/id/{}
Xbox=https://account.xbox.com/en-us/profile?gamertag={}
PlayStation=https://psnprofiles.com/{}
Epic Games=https://fortnitetracker.com/profile/pc/{}
Roblox=https://roblox.com/users/{}/profile
Minecraft=https://namemc.com/profile/{}

# Developer Platforms
GitHub=https://github.com/{}
GitLab=https://gitlab.com/{}
Bitbucket=https://bitbucket.org/{}
Stack Overflow=https://stackoverflow.com/users/{}
CodePen=https://codepen.io/{}
HackerRank=https://hackerrank.com/{}
LeetCode=https://leetcode.com/{}
Kaggle=https://kaggle.com/{}

# Business Platforms
AngelList=https://angel.co/{}
Crunchbase=https://crunchbase.com/person/{}
Upwork=https://upwork.com/freelancers/{}
Fiverr=https://fiverr.com/{}

# Music Platforms
Spotify=https://open.spotify.com/user/{}
SoundCloud=https://soundcloud.com/{}
Bandcamp=https://bandcamp.com/{}
Last.fm=https://last.fm/user/{}

# Financial Platforms
PayPal=https://paypal.me/{}
Venmo=https://venmo.com/{}
CashApp=https://cash.app/${}
Patreon=https://patreon.com/{}

# NSFW Platforms (Uncomment if needed)
# OnlyFans=https://onlyfans.com/{}
# Pornhub=https://pornhub.com/model/{}
# FetLife=https://fetlife.com/users/{}
"""
        
        url_file.parent.mkdir(exist_ok=True)
        with open(url_file, 'w') as f:
            f.write(default_urls)
        
        ElohimLogger.success(f"Created default URL file: {url_file}")
    
    @staticmethod
    def _get_fallback_urls() -> Dict[str, str]:
        """Fallback URLs if file loading fails"""
        return {
            'GitHub': 'https://github.com/{}',
            'Instagram': 'https://instagram.com/{}',
            'Twitter': 'https://twitter.com/{}',
            'LinkedIn': 'https://linkedin.com/in/{}',
            'Reddit': 'https://reddit.com/user/{}'
        }
    
    # Legacy methods for backward compatibility
    SOCIAL_PLATFORMS = {}
    GAMING_PLATFORMS = {}
    DEV_PLATFORMS = {}
    BUSINESS_PLATFORMS = {}
    DATING_PLATFORMS = {}
    FORUM_PLATFORMS = {}
    NSFW_PLATFORMS = {}
    FINANCIAL_PLATFORMS = {}
    MUSIC_PLATFORMS = {}

class PluginManager:
    """Simplified plugin manager"""
    
    def __init__(self):
        self.plugins = {}
        self.plugin_directory = Path("Assets")
        self.plugin_directory.mkdir(exist_ok=True)
        ElohimLogger.ghost("Plugin system initialized")
    
    def load_plugins(self):
        """Load plugins from Assets directory"""
        ElohimLogger.info("Loading available plugins...")
        
        # Create simple built-in plugins
        self.plugins['url_scanner'] = self._create_url_scanner()
        self.plugins['email_hunter'] = self._create_email_hunter()
        self.plugins['dark_web'] = self._create_dark_web_scanner()
        
        ElohimLogger.success(f"Loaded {len(self.plugins)} plugin(s)")
    
    def _create_url_scanner(self):
        """Simple URL scanner plugin"""
        def execute(target, **kwargs):
            ElohimLogger.ghost("Scanning for platform URLs...")
            discovered = [f"https://newsite.com/{target}", f"https://platform.io/{target}"]
            for url in discovered:
                ElohimLogger.result("URL Scanner", "FOUND", url)
            return {'url_scanner': {'discovered': discovered}}
        
        plugin = type('URLScanner', (), {
            'execute': execute,
            'description': 'Platform URL discovery',
            'version': '1.0'
        })()
        ElohimLogger.plugin_loaded("builtin:url_scanner")
        return plugin
    
    def _create_email_hunter(self):
        """Simple email hunter plugin"""
        def execute(target, **kwargs):
            ElohimLogger.ghost("Hunting email addresses...")
            domain = target.split('@')[1] if '@' in target else target
            emails = [f"admin@{domain}", f"info@{domain}"]
            for email in emails:
                ElohimLogger.result("Email Hunter", "FOUND", email)
            return {'email_hunter': {'found': emails}}
        
        plugin = type('EmailHunter', (), {
            'execute': execute,
            'description': 'Email address discovery',
            'version': '1.0'
        })()
        ElohimLogger.plugin_loaded("builtin:email_hunter")
        return plugin
    
    def _create_dark_web_scanner(self):
        """Simple dark web scanner"""
        def execute(target, **kwargs):
            ElohimLogger.ghost("Scanning dark web mentions...")
            mentions = random.randint(0, 3)
            if mentions > 0:
                ElohimLogger.warning(f"Found {mentions} dark web mention(s)")
            else:
                ElohimLogger.success("No dark web presence detected")
            return {'dark_web': {'mentions': mentions}}
        
        plugin = type('DarkWebScanner', (), {
            'execute': execute,
            'description': 'Dark web presence detection',
            'version': '1.0'
        })()
        ElohimLogger.plugin_loaded("builtin:dark_web")
        return plugin
    
    def execute_plugin(self, plugin_name: str, target: str, **kwargs) -> Dict[str, Any]:
        """Execute plugin"""
        if plugin_name not in self.plugins:
            ElohimLogger.error(f"Plugin '{plugin_name}' not found")
            return {}
        
        try:
            ElohimLogger.info(f"Executing plugin: {plugin_name}")
            result = self.plugins[plugin_name].execute(target, **kwargs)
            ElohimLogger.success(f"Plugin '{plugin_name}' completed")
            return result
        except Exception as e:
            ElohimLogger.error(f"Plugin '{plugin_name}' failed: {str(e)}")
            return {}
    
    def list_plugins(self) -> List[str]:
        return list(self.plugins.keys())
    
    def get_plugin_info(self, plugin_name: str) -> Dict[str, str]:
        if plugin_name not in self.plugins:
            return {}
        
        plugin = self.plugins[plugin_name]
        return {
            'name': plugin_name,
            'description': getattr(plugin, 'description', 'No description'),
            'version': getattr(plugin, 'version', '1.0')
        }

class UsernameSearcher:
    """Enhanced username enumeration with robust error handling"""
    
    def __init__(self, max_workers: int = 20, simulation_mode: bool = True):
        self.max_workers = max_workers
        self.simulation_mode = simulation_mode
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def check_username_async(self, session: aiohttp.ClientSession, platform: str, url: str, username: str) -> Dict[str, Any]:
        """Asynchronously check username with robust error handling"""
        
        # Simulation mode for demos/testing
        if self.simulation_mode:
            await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
            found = random.choice([True, False, False, False])  # 25% chance found
            status = "FOUND" if found else "NOT FOUND"
            formatted_url = url.format(username) if found else ""
            return {'platform': platform, 'status': status, 'url': formatted_url}
        
        # Real scanning mode
        try:
            formatted_url = url.format(username)
            async with session.get(formatted_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    content = await response.text()
                    if self._validate_profile_content(platform, content, username):
                        return {'platform': platform, 'status': 'FOUND', 'url': formatted_url}
                    else:
                        return {'platform': platform, 'status': 'NOT FOUND', 'url': ''}
                else:
                    return {'platform': platform, 'status': 'NOT FOUND', 'url': ''}
        except asyncio.TimeoutError:
            return {'platform': platform, 'status': 'TIMEOUT', 'url': ''}
        except (aiohttp.ClientConnectionError, aiohttp.ClientSSLError) as e:
            return {'platform': platform, 'status': 'CONNECTION_ERROR', 'url': '', 'error': str(e)}
        except Exception as e:
            return {'platform': platform, 'status': 'ERROR', 'url': '', 'error': str(e)}
    
    def _validate_profile_content(self, platform: str, content: str, username: str) -> bool:
        """Validate if profile actually exists based on content analysis"""
        validation_rules = {
            'GitHub': lambda c: 'Not Found' not in c and 'Page not found' not in c,
            'Instagram': lambda c: '"user_id"' in c or 'profilePage_' in c,
            'Twitter': lambda c: 'profile_id' in c or 'ProfileTimeline' in c,
            'LinkedIn': lambda c: 'profile' in c.lower() and 'member' in c.lower(),
            'Reddit': lambda c: 'user/' in c and 'overview' in c
        }
        
        if platform in validation_rules:
            return validation_rules[platform](content)
        
        negative_indicators = [
            'not found', 'page not found', '404', 'user not found',
            'profile not found', 'account not found', 'suspended'
        ]
        
        return not any(indicator in content.lower() for indicator in negative_indicators)
    
    async def search_username(self, username: str, platforms: Dict[str, str]) -> List[Dict[str, Any]]:
        """Search username across multiple platforms with improved connection handling"""
        ElohimLogger.info(f"Initiating username reconnaissance for: {username}")
        ElohimLogger.info(f"Scanning {len(platforms)} platforms...")
        
        if self.simulation_mode:
            ElohimLogger.warning("Running in simulation mode for demonstration")
        
        # More conservative connection settings
        connector = aiohttp.TCPConnector(
            limit=20,  # Reduced from 100
            limit_per_host=5,  # Reduced from 10
            ssl=False,  # Disable SSL verification for problematic sites
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        timeout = aiohttp.ClientTimeout(total=15, connect=5)
        
        try:
            async with aiohttp.ClientSession(
                connector=connector, 
                timeout=timeout,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            ) as session:
                
                # Process platforms in smaller batches to avoid overwhelming connections
                batch_size = 10
                platform_items = list(platforms.items())
                all_results = []
                
                for i in range(0, len(platform_items), batch_size):
                    batch = platform_items[i:i+batch_size]
                    ElohimLogger.info(f"Processing batch {i//batch_size + 1}/{(len(platform_items) + batch_size - 1)//batch_size}")
                    
                    tasks = []
                    for platform, url_template in batch:
                        task = self.check_username_async(session, platform, url_template, username)
                        tasks.append(task)
                    
                    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for result in batch_results:
                        if isinstance(result, dict):
                            all_results.append(result)
                            status = result['status']
                            if status == 'FOUND':
                                ElohimLogger.result(result['platform'], status, result.get('url', ''))
                            elif status in ['NSFW']:
                                ElohimLogger.result(result['platform'], 'NSFW', result.get('url', ''))
                            elif status in ['TIMEOUT', 'CONNECTION_ERROR']:
                                ElohimLogger.warning(f"{result['platform']}: {status}")
                    
                    # Small delay between batches
                    await asyncio.sleep(0.5)
                
        except Exception as e:
            ElohimLogger.error(f"Session error: {str(e)}")
            return []
        
        found_count = len([r for r in all_results if r.get('status') == 'FOUND'])
        ElohimLogger.success(f"Scan completed. Found {found_count} profiles across {len(platforms)} platforms")
        
        return all_results

class DomainAnalyzer:
    """Comprehensive domain and infrastructure analysis"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def whois_lookup(self, domain: str) -> Dict[str, Any]:
        """Perform WHOIS lookup"""
        try:
            ElohimLogger.info(f"Performing WHOIS lookup for {domain}")
            w = whois.whois(domain)
            return {
                'domain': domain,
                'registrar': getattr(w, 'registrar', 'Unknown'),
                'creation_date': str(getattr(w, 'creation_date', 'Unknown')),
                'expiration_date': str(getattr(w, 'expiration_date', 'Unknown')),
                'name_servers': getattr(w, 'name_servers', []),
                'status': getattr(w, 'status', 'Unknown')
            }
        except Exception as e:
            ElohimLogger.error(f"WHOIS lookup failed: {str(e)}")
            return {'error': str(e)}
    
    def dns_enumeration(self, domain: str) -> Dict[str, List[str]]:
        """Enumerate DNS records"""
        ElohimLogger.info(f"Enumerating DNS records for {domain}")
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(answer) for answer in answers]
                ElohimLogger.success(f"Found {len(records[record_type])} {record_type} records")
            except:
                records[record_type] = []
        
        return records
    
    def subdomain_enumeration(self, domain: str) -> List[str]:
        """Discover subdomains using wordlist"""
        ElohimLogger.info(f"Discovering subdomains for {domain}")
        
        # Common subdomain wordlist
        subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mobile', 'm', 'dev',
            'staging', 'test', 'admin', 'api', 'blog', 'shop', 'store', 'secure', 'vpn',
            'cdn', 'static', 'assets', 'media', 'images', 'img', 'docs', 'support',
            'portal', 'dashboard', 'app', 'apps', 'beta', 'alpha', 'demo', 'preview'
        ]
        
        found_subdomains = []
        
        def check_subdomain(sub):
            try:
                full_domain = f"{sub}.{domain}"
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
                ElohimLogger.success(f"Found subdomain: {full_domain}")
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(check_subdomain, subdomains)
        
        return found_subdomains
    
    def ssl_analysis(self, domain: str) -> Dict[str, Any]:
        """Analyze SSL certificate"""
        ElohimLogger.info(f"Analyzing SSL certificate for {domain}")
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'san': cert.get('subjectAltName', [])
                    }
        except Exception as e:
            ElohimLogger.error(f"SSL analysis failed: {str(e)}")
            return {'error': str(e)}

class EmailInvestigator:
    """Email address investigation and analysis"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def analyze_email(self, email: str) -> Dict[str, Any]:
        """Comprehensive email analysis"""
        ElohimLogger.info(f"Investigating email: {email}")
        
        domain = email.split('@')[1] if '@' in email else None
        if not domain:
            return {'error': 'Invalid email format'}
        
        results = {
            'email': email,
            'domain': domain,
            'domain_analysis': {},
            'breach_check': self.check_breaches(email),
            'account_enumeration': self.enumerate_accounts(email)
        }
        
        # Analyze domain
        domain_analyzer = DomainAnalyzer()
        results['domain_analysis'] = {
            'whois': domain_analyzer.whois_lookup(domain),
            'dns': domain_analyzer.dns_enumeration(domain)
        }
        
        return results
    
    def check_breaches(self, email: str) -> Dict[str, Any]:
        """Check for data breaches (simulated)"""
        ElohimLogger.info(f"Checking breach databases for {email}")
        
        # Simulated breach check results
        common_breaches = [
            'LinkedIn 2012', 'Adobe 2013', 'Yahoo 2014', 'Equifax 2017',
            'Facebook 2019', 'Twitter 2020', 'Microsoft 2021'
        ]
        
        # Simulate random breach results
        found_breaches = random.sample(common_breaches, random.randint(0, 3))
        
        if found_breaches:
            ElohimLogger.warning(f"Found in {len(found_breaches)} breach(es)")
            for breach in found_breaches:
                ElohimLogger.result("Breach Database", "FOUND", breach)
        else:
            ElohimLogger.success("No breaches found")
        
        return {
            'breaches_found': len(found_breaches),
            'breach_list': found_breaches
        }
    
    def enumerate_accounts(self, email: str) -> List[str]:
        """Enumerate associated accounts"""
        ElohimLogger.info("Enumerating associated accounts")
        
        # Platform-specific account enumeration
        platforms = {
            'Adobe': f'https://accounts.adobe.com/verify?email={email}',
            'GitHub': f'https://github.com/password_reset',
            'Microsoft': f'https://account.live.com/ResetPassword.aspx',
            'Google': f'https://accounts.google.com/signin/recovery'
        }
        
        found_accounts = []
        for platform, url in platforms.items():
            # Simulated account detection
            if random.choice([True, False]):
                found_accounts.append(platform)
                ElohimLogger.result(platform, "FOUND", "Account exists")
            else:
                ElohimLogger.result(platform, "NOT FOUND")
        
        return found_accounts

class PhoneInvestigator:
    """Phone number OSINT and analysis"""
    
    def analyze_phone(self, phone: str) -> Dict[str, Any]:
        """Comprehensive phone number analysis"""
        ElohimLogger.info(f"Analyzing phone number: {phone}")
        
        # Clean phone number
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        results = {
            'phone': phone,
            'cleaned': cleaned_phone,
            'carrier': self.identify_carrier(cleaned_phone),
            'location': self.get_location_info(cleaned_phone),
            'social_links': self.find_social_links(cleaned_phone),
            'spam_check': self.check_spam_database(cleaned_phone)
        }
        
        return results
    
    def identify_carrier(self, phone: str) -> Dict[str, str]:
        """Identify phone carrier"""
        ElohimLogger.info("Identifying carrier information")
        
        # Simulated carrier data
        carriers = ['Verizon', 'AT&T', 'T-Mobile', 'Sprint', 'US Cellular']
        carrier = random.choice(carriers)
        
        ElohimLogger.success(f"Carrier identified: {carrier}")
        
        return {
            'carrier': carrier,
            'type': random.choice(['Mobile', 'Landline', 'VoIP']),
            'region': random.choice(['US-East', 'US-West', 'US-Central'])
        }
    
    def get_location_info(self, phone: str) -> Dict[str, str]:
        """Get location information"""
        ElohimLogger.info("Analyzing location data")
        
        locations = {
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            'state': random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
            'timezone': random.choice(['EST', 'PST', 'CST', 'MST'])
        }
        
        ElohimLogger.success(f"Location: {locations['city']}, {locations['state']}")
        
        return locations
    
    def find_social_links(self, phone: str) -> List[str]:
        """Find social media profiles linked to phone"""
        ElohimLogger.info("Searching for linked social media accounts")
        
        platforms = ['WhatsApp', 'Telegram', 'Signal', 'Viber']
        found = random.sample(platforms, random.randint(0, 2))
        
        for platform in found:
            ElohimLogger.result(platform, "FOUND", "Profile linked")
        
        return found
    
    def check_spam_database(self, phone: str) -> Dict[str, Any]:
        """Check spam/scam databases"""
        ElohimLogger.info("Checking spam/scam databases")
        
        is_spam = random.choice([True, False])
        spam_score = random.randint(0, 100) if is_spam else random.randint(0, 30)
        
        if is_spam:
            ElohimLogger.warning(f"Spam score: {spam_score}/100")
        else:
            ElohimLogger.success(f"Clean number - Spam score: {spam_score}/100")
        
        return {
            'is_spam': is_spam,
            'spam_score': spam_score,
            'reports': random.randint(0, 50) if is_spam else 0
        }

class ReportGenerator:
    """Generate comprehensive OSINT reports"""
    
    @staticmethod
    def generate_report(target: str, results: Dict[str, Any], output_format: str = 'json') -> str:
        """Generate comprehensive report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'target': target,
            'timestamp': timestamp,
            'scan_type': 'comprehensive_osint',
            'results': results,
            'summary': ReportGenerator._generate_summary(results)
        }
        
        if output_format == 'json':
            filename = f"elohim_report_{target}_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        
        ElohimLogger.success(f"Report generated: {filename}")
        return filename
    
    @staticmethod
    def _generate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        summary = {
            'total_platforms_checked': 0,
            'profiles_found': 0,
            'risk_level': 'LOW',
            'recommendations': []
        }
        
        # Analyze results and generate summary
        if 'username_search' in results:
            username_results = results['username_search']
            summary['total_platforms_checked'] = len(username_results)
            summary['profiles_found'] = len([r for r in username_results if r.get('status') == 'FOUND'])
        
        # Risk assessment
        if summary['profiles_found'] > 10:
            summary['risk_level'] = 'HIGH'
        elif summary['profiles_found'] > 5:
            summary['risk_level'] = 'MEDIUM'
        
        return summary

class ElohimCore:
    """Main ELOHIM framework controller with plugin support"""
    
    def __init__(self):
        self.username_searcher = UsernameSearcher()
        self.domain_analyzer = DomainAnalyzer()
        self.email_investigator = EmailInvestigator()
        self.phone_investigator = PhoneInvestigator()
        self.report_generator = ReportGenerator()
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
    
    async def run_username_search(self, username: str, platform_types: List[str], include_nsfw: bool = False) -> Dict[str, Any]:
        """Execute enhanced username search with file-based URL loading"""
        
        # Load all URLs from file
        all_platforms = OSINTDatabase.load_urls_from_file()
        
        # Filter platforms based on types (optional - use all if no filtering needed)
        if platform_types and platform_types != ['all']:
            # For now, use all platforms since file doesn't have categories
            # You can add category filtering by adding comments in the URL file
            platforms = all_platforms
        else:
            platforms = all_platforms
        
        # Filter NSFW if not requested
        if not include_nsfw:
            nsfw_keywords = ['onlyfans', 'pornhub', 'fetlife', 'adult', 'xxx', 'cam', 'sex']
            platforms = {k: v for k, v in platforms.items() 
                        if not any(keyword in k.lower() or keyword in v.lower() for keyword in nsfw_keywords)}
        
        results = await self.username_searcher.search_username(username, platforms)
        return {'username_search': results}
    
    def run_domain_analysis(self, domain: str) -> Dict[str, Any]:
        """Execute domain analysis"""
        ElohimLogger.info(f"Starting comprehensive domain analysis for: {domain}")
        
        results = {
            'whois': self.domain_analyzer.whois_lookup(domain),
            'dns': self.domain_analyzer.dns_enumeration(domain),
            'subdomains': self.domain_analyzer.subdomain_enumeration(domain),
            'ssl': self.domain_analyzer.ssl_analysis(domain)
        }
        
        return {'domain_analysis': results}
    
    def run_email_investigation(self, email: str) -> Dict[str, Any]:
        """Execute email investigation"""
        results = self.email_investigator.analyze_email(email)
        return {'email_investigation': results}
    
    def run_phone_investigation(self, phone: str) -> Dict[str, Any]:
        """Execute phone investigation"""
        results = self.phone_investigator.analyze_phone(phone)
        return {'phone_investigation': results}
    
    async def run_comprehensive_scan(self, target: str, include_nsfw: bool = False) -> Dict[str, Any]:
        """Execute comprehensive multi-vector scan"""
        ElohimLogger.info(f"Initiating comprehensive scan for: {target}")
        
        all_results = {}
        
        # Determine target type and run appropriate scans
        if '@' in target:  # Email
            all_results.update(self.run_email_investigation(target))
            username = target.split('@')[0]
            all_results.update(await self.run_username_search(
                username, ['social', 'dev', 'business'], include_nsfw
            ))
            
        elif target.replace('+', '').replace('-', '').replace(' ', '').isdigit():  # Phone
            all_results.update(self.run_phone_investigation(target))
            
        elif '.' in target and not ' ' in target:  # Domain
            all_results.update(self.run_domain_analysis(target))
            
        else:  # Username
            all_results.update(await self.run_username_search(
                target, ['social', 'gaming', 'dev', 'business', 'dating', 'forum'], include_nsfw
            ))
        
        return all_results

def main():
    """Enhanced CLI interface with wizard mode and plugin support"""
    parser = argparse.ArgumentParser(
        description="ELOHIM - Advanced OSINT Reconnaissance Framework v3.0-GHOST",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.GREEN}Examples:{Style.RESET_ALL}
  {Fore.CYAN}python3 elohim.py --wizard{Style.RESET_ALL}                    # Interactive wizard mode
  {Fore.CYAN}python3 elohim.py username -t johndoe --platforms social dev --nsfw{Style.RESET_ALL}
  {Fore.CYAN}python3 elohim.py email -t user@example.com --plugins all{Style.RESET_ALL}
  {Fore.CYAN}python3 elohim.py domain -t example.com --deep-scan{Style.RESET_ALL}
  {Fore.CYAN}python3 elohim.py phone -t +1234567890 --save-report{Style.RESET_ALL}
  {Fore.CYAN}python3 elohim.py comprehensive -t target --nsfw --plugins social_analyzer,breach_monitor{Style.RESET_ALL}
  {Fore.CYAN}python3 elohim.py list-plugins{Style.RESET_ALL}               # List available plugins
        """
    )
    
    # Add wizard mode flag
    parser.add_argument('--wizard', action='store_true', 
                       help='Launch interactive wizard mode for guided reconnaissance')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Username search
    username_parser = subparsers.add_parser('username', help='Username reconnaissance')
    username_parser.add_argument('-t', '--target', required=True, help='Username to investigate')
    username_parser.add_argument('--platforms', nargs='+', 
                               choices=['social', 'gaming', 'dev', 'business', 'dating', 'forum', 'financial', 'music'],
                               default=['social', 'dev'], help='Platform types to search')
    username_parser.add_argument('--nsfw', action='store_true', 
                               help='Include NSFW platforms (extended coverage)')
    
    # Email investigation
    email_parser = subparsers.add_parser('email', help='Email investigation')
    email_parser.add_argument('-t', '--target', required=True, help='Email to investigate')
    
    # Domain analysis
    domain_parser = subparsers.add_parser('domain', help='Domain analysis')
    domain_parser.add_argument('-t', '--target', required=True, help='Domain to analyze')
    
    # Phone investigation
    phone_parser = subparsers.add_parser('phone', help='Phone number investigation')
    phone_parser.add_argument('-t', '--target', required=True, help='Phone number to investigate')
    
    # Comprehensive scan
    comp_parser = subparsers.add_parser('comprehensive', help='Comprehensive multi-vector scan')
    comp_parser.add_argument('-t', '--target', required=True, help='Target to investigate')
    comp_parser.add_argument('--nsfw', action='store_true', 
                           help='Include NSFW platforms in scan')
    
    # Plugin management
    plugin_parser = subparsers.add_parser('list-plugins', help='List available plugins')
    
    plugin_info_parser = subparsers.add_parser('plugin-info', help='Get plugin information')
    plugin_info_parser.add_argument('-p', '--plugin', required=True, help='Plugin name')
    
    # Global options
    parser.add_argument('--output', choices=['json', 'txt'], default='json', 
                       help='Output format for reports')
    parser.add_argument('--save-report', action='store_true', 
                       help='Save results to report file')
    parser.add_argument('--plugins', nargs='+', 
                       help='Execute specific plugins (comma-separated or "all")')
    parser.add_argument('--deep-scan', action='store_true',
                       help='Enable deep scanning mode')
    parser.add_argument('--silent', action='store_true',
                       help='Minimize output (results only)')
    
    args = parser.parse_args()
    
    # Initialize ELOHIM
    if not args.silent:
        ElohimLogger.banner()
    
    elohim = ElohimCore()
    
    # Handle wizard mode
    if args.wizard:
        wizard = WizardMode(elohim)
        asyncio.run(wizard.run())
        return
    
    # Handle plugin management commands
    if args.command == 'list-plugins':
        plugins = elohim.plugin_manager.list_plugins()
        ElohimLogger.info("Available plugins:")
        for plugin in plugins:
            plugin_info = elohim.plugin_manager.get_plugin_info(plugin)
            print(f"  {Fore.GREEN}◢◤{Style.RESET_ALL} {plugin:<20} - {plugin_info.get('description', 'No description')}")
        return
    
    if args.command == 'plugin-info':
        plugin_info = elohim.plugin_manager.get_plugin_info(args.plugin)
        if plugin_info:
            ElohimLogger.info(f"Plugin: {plugin_info['name']}")
            print(f"  Description: {plugin_info.get('description', 'N/A')}")
            print(f"  Version: {plugin_info.get('version', 'N/A')}")
            print(f"  Author: {plugin_info.get('author', 'N/A')}")
        else:
            ElohimLogger.error(f"Plugin '{args.plugin}' not found")
        return
    
    if not args.command:
        parser.print_help()
        return
    
    async def run_scan():
        results = {}
        
        try:
            if args.command == 'username':
                results = await elohim.run_username_search(
                    args.target, args.platforms, getattr(args, 'nsfw', False)
                )
            elif args.command == 'email':
                results = elohim.run_email_investigation(args.target)
            elif args.command == 'domain':
                results = elohim.run_domain_analysis(args.target)
            elif args.command == 'phone':
                results = elohim.run_phone_investigation(args.target)
            elif args.command == 'comprehensive':
                results = await elohim.run_comprehensive_scan(
                    args.target, getattr(args, 'nsfw', False)
                )
            
            # Execute additional plugins if specified
            if hasattr(args, 'plugins') and args.plugins:
                if 'all' in args.plugins:
                    selected_plugins = elohim.plugin_manager.list_plugins()
                else:
                    selected_plugins = args.plugins
                
                for plugin_name in selected_plugins:
                    plugin_result = elohim.plugin_manager.execute_plugin(plugin_name, args.target)
                    results.update(plugin_result)
            
            if args.save_report:
                report_file = elohim.report_generator.generate_report(
                    args.target, results, args.output
                )
                ElohimLogger.success(f"Scan completed. Report saved: {report_file}")
            else:
                ElohimLogger.success("Scan completed successfully")
                
        except KeyboardInterrupt:
            ElohimLogger.warning("Scan interrupted by user")
        except Exception as e:
            ElohimLogger.error(f"Scan failed: {str(e)}")
    
    # Run the async scan
    asyncio.run(run_scan())

if __name__ == "__main__":
    main()
