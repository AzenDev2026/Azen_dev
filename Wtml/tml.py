#!/usr/bin/env python3
"""
Custom Terminal Tool with Colored ASCII Logo and Customizable Prompt
"""

import os
import sys
import platform
import subprocess
import readline
import psutil
import socket
from datetime import datetime
from pathlib import Path
import distro
import getpass

# ANSI Color Codes
class Colors:
    # Regular Colors
    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    LIGHT_WHITE = '\033[1;37m'
    
    # Bold Colors
    BOLD_BLACK = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_PURPLE = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    
    # Background Colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_PURPLE = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'
    
    # Special
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Custom Colors for Logo - ONLY these three
    LOGO_TOP = '\033[94m'      # Light Blue
    LOGO_MID = '\033[34m'      # Blue
    LOGO_BOTTOM = '\033[36m'   # Dark Blue (using cyan for dark blue effect)

class CustomTerminal:
    def __init__(self):
        self.aliases = {
            'exit': 'quit',
            'clear': 'cls'
        }
        self.history_file = Path.home() / '.custom_terminal_history'
        self.setup_readline()
        self.system_info = self.get_system_info()
        
        # Prompt color settings (default: light white)
        self.prompt_color = Colors.LIGHT_WHITE
        self.prompt_color_name = 'light_white'
        self.prompt_text = '➜ '  # Default prompt symbol
        
        # Available colors for users
        self.available_colors = {
            'black': Colors.BLACK,
            'red': Colors.RED,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'blue': Colors.BLUE,
            'purple': Colors.PURPLE,
            'cyan': Colors.CYAN,
            'white': Colors.WHITE,
            'light_white': Colors.LIGHT_WHITE,
            'bold_black': Colors.BOLD_BLACK,
            'bold_red': Colors.BOLD_RED,
            'bold_green': Colors.BOLD_GREEN,
            'bold_yellow': Colors.BOLD_YELLOW,
            'bold_blue': Colors.BOLD_BLUE,
            'bold_purple': Colors.BOLD_PURPLE,
            'bold_cyan': Colors.BOLD_CYAN
        }
        
    def setup_readline(self):
        """Setup command history"""
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass
        readline.set_history_length(1000)
        
    def save_history(self):
        """Save command history"""
        try:
            readline.write_history_file(self.history_file)
        except Exception:
            pass

    def get_ascii_logo_colored(self):
        """Return the custom ASCII logo with ONLY light blue, blue, and dark blue"""
        logo_lines = [
            "               ##              ",
            "            ########           ",
            "         ##############        ",
            "      ####################     ",
            "   ##########################  ",
            "    :######################    ",
            "  %    *################+    # ",
            "  %%%%    ############    %%%# ",
            "  +%%%%%+    ######    *%%%%%  ",
            "     %%%%%%          %%%%%*    ",
            "  %%    %%%%%%    %%%%%%    %% ",
            "  %%%%%    %%%%%%%%%%    %%%%% ",
            "    %%%%%     %%%%     %%%%%   ",
            "      #%%%%%        %%%%%*     ",
            "         %%%%%%  %%%%%%        ",
            "            %%%%%%%%           ",
            "               %%              "
        ]
        
        # Define exact color zones for the logo
        # Top part: Light Blue (lines 0-5)
        # Middle part: Blue (lines 6-11)
        # Bottom part: Dark Blue (lines 12-16)
        
        colored_logo = []
        for i, line in enumerate(logo_lines):
            if i <= 5:  # Top section
                color = Colors.LOGO_TOP  # Light Blue
            elif i <= 11:  # Middle section
                color = Colors.LOGO_MID  # Blue
            else:  # Bottom section (lines 12-16)
                color = Colors.LOGO_BOTTOM  # Dark Blue
            
            colored_logo.append(f"{color}{line}{Colors.RESET}")
        
        return '\n'.join(colored_logo)

    def get_color_test_grid(self):
        """Generate a 16-color test grid"""
        colors = [
            ('Black', Colors.BG_BLACK, Colors.WHITE),
            ('Red', Colors.BG_RED, Colors.WHITE),
            ('Green', Colors.BG_GREEN, Colors.BLACK),
            ('Yellow', Colors.BG_YELLOW, Colors.BLACK),
            ('Blue', Colors.BG_BLUE, Colors.WHITE),
            ('Purple', Colors.BG_PURPLE, Colors.WHITE),
            ('Cyan', Colors.BG_CYAN, Colors.BLACK),
            ('White', Colors.BG_WHITE, Colors.BLACK),
            ('Bright Black', Colors.BG_BRIGHT_BLACK, Colors.WHITE),
            ('Bright Red', Colors.BG_BRIGHT_RED, Colors.WHITE),
            ('Bright Green', Colors.BG_BRIGHT_GREEN, Colors.BLACK),
            ('Bright Yellow', Colors.BG_BRIGHT_YELLOW, Colors.BLACK),
            ('Bright Blue', Colors.BG_BRIGHT_BLUE, Colors.WHITE),
            ('Bright Purple', Colors.BG_BRIGHT_PURPLE, Colors.WHITE),
            ('Bright Cyan', Colors.BG_BRIGHT_CYAN, Colors.BLACK),
            ('Bright White', Colors.BG_BRIGHT_WHITE, Colors.BLACK)
        ]
        
        # Create two rows of 8 colors each
        grid = []
        # Row 1: Colors 0-7
        row1 = []
        for i in range(8):
            bg, fg = colors[i][1], colors[i][2]
            row1.append(f"{bg}{fg}████████{Colors.RESET}")
        grid.append('  ' + '  '.join(row1))
        
        # Row 2: Colors 8-15
        row2 = []
        for i in range(8, 16):
            bg, fg = colors[i][1], colors[i][2]
            row2.append(f"{bg}{fg}████████{Colors.RESET}")
        grid.append('  ' + '  '.join(row2))
        
        # Add color names as a legend
        legend = []
        for i, (name, _, _) in enumerate(colors):
            if i < 8:
                legend.append(f"{Colors.BOLD}{name}{Colors.RESET}")
            else:
                legend.append(f"{Colors.BOLD}{name}{Colors.RESET}")
        
        # Show first row names
        legend_row1 = '  '.join([f"{Colors.DIM}{name[:8]:<8}{Colors.RESET}" for name in legend[:8]])
        legend_row2 = '  '.join([f"{Colors.DIM}{name[:8]:<8}{Colors.RESET}" for name in legend[8:]])
        
        return '\n'.join([
            f"  {legend_row1}",
            grid[0],
            f"  {legend_row2}",
            grid[1]
        ])

    def get_cpu_info(self):
        """Get detailed CPU information"""
        cpu_info = {}
        
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('model name'):
                        cpu_info['model'] = line.split(':')[1].strip()
                        break
        except:
            cpu_info['model'] = platform.processor() or 'Unknown'
        
        cpu_info['cores'] = os.cpu_count() or 0
        cpu_info['physical_cores'] = 0
        
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpu_info['physical_cores'] = len([line for line in f if line.startswith('physical id')])
                if cpu_info['physical_cores'] == 0:
                    cpu_info['physical_cores'] = cpu_info['cores']
        except:
            cpu_info['physical_cores'] = cpu_info['cores']
        
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('cpu MHz'):
                        cpu_info['frequency'] = f"{float(line.split(':')[1].strip()):.2f} MHz"
                        break
        except:
            cpu_info['frequency'] = 'Unknown'
        
        cpu_info['usage_percent'] = psutil.cpu_percent(interval=0.5)
        cpu_info['usage_per_core'] = psutil.cpu_percent(interval=0.5, percpu=True)
        
        return cpu_info

    def get_memory_info(self):
        """Get detailed memory information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': self.bytes_to_human(mem.total),
            'available': self.bytes_to_human(mem.available),
            'used': self.bytes_to_human(mem.used),
            'percent': mem.percent,
            'swap_total': self.bytes_to_human(swap.total) if swap.total > 0 else 'N/A',
            'swap_used': self.bytes_to_human(swap.used) if swap.total > 0 else 'N/A',
            'swap_percent': swap.percent if swap.total > 0 else 0
        }

    def get_disk_info(self):
        """Get disk information"""
        disk_info = []
        try:
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'device': partition.device,
                        'mount': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': self.bytes_to_human(usage.total),
                        'used': self.bytes_to_human(usage.used),
                        'free': self.bytes_to_human(usage.free),
                        'percent': usage.percent
                    })
                except:
                    pass
        except:
            pass
        return disk_info

    def get_network_info(self):
        """Get network information"""
        network_info = {}
        
        try:
            hostname = socket.gethostname()
            network_info['hostname'] = hostname
            
            ips = []
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ips.append(s.getsockname()[0])
                s.close()
            except:
                pass
            
            try:
                import netifaces
                for interface in netifaces.interfaces():
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        for addr in addrs[netifaces.AF_INET]:
                            if addr['addr'] != '127.0.0.1':
                                ips.append(addr['addr'])
            except:
                try:
                    ips.append(socket.gethostbyname(hostname))
                except:
                    pass
            
            network_info['ips'] = list(set(ips)) if ips else ['Unknown']
            
            macs = []
            try:
                import netifaces
                for interface in netifaces.interfaces():
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_LINK in addrs:
                        for addr in addrs[netifaces.AF_LINK]:
                            if addr['addr'] != '00:00:00:00:00:00':
                                macs.append(f"{interface}: {addr['addr']}")
            except:
                try:
                    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                    for line in result.stdout.split('\n'):
                        if 'ether' in line:
                            parts = line.strip().split()
                            idx = parts.index('ether')
                            if idx + 1 < len(parts):
                                macs.append(parts[idx + 1])
                        elif 'HWaddr' in line:
                            parts = line.strip().split()
                            idx = parts.index('HWaddr')
                            if idx + 1 < len(parts):
                                macs.append(parts[idx + 1])
                except:
                    pass
            
            network_info['macs'] = list(set(macs)) if macs else ['Unknown']
            
        except Exception as e:
            network_info = {'hostname': 'Unknown', 'ips': ['Unknown'], 'macs': ['Unknown']}
        
        return network_info

    def get_user_info(self):
        """Get detailed user information"""
        user_info = {}
        
        try:
            user_info['username'] = getpass.getuser()
            user_info['uid'] = os.getuid()
            user_info['gid'] = os.getgid()
            
            try:
                import pwd
                pw = pwd.getpwnam(user_info['username'])
                user_info['home'] = pw.pw_dir
                user_info['shell'] = pw.pw_shell
                user_info['gecos'] = pw.pw_gecos
            except:
                user_info['home'] = os.path.expanduser('~')
                user_info['shell'] = os.environ.get('SHELL', 'Unknown')
                user_info['gecos'] = 'Unknown'
            
            try:
                import grp
                groups = []
                for group in grp.getgrall():
                    if user_info['username'] in group.gr_mem:
                        groups.append(group.gr_name)
                user_info['groups'] = groups
            except:
                user_info['groups'] = ['Unknown']
            
        except Exception as e:
            user_info = {
                'username': 'Unknown',
                'uid': 0,
                'gid': 0,
                'home': 'Unknown',
                'shell': 'Unknown',
                'gecos': 'Unknown',
                'groups': ['Unknown']
            }
        
        return user_info

    def get_system_info(self):
        """Get ALL system information"""
        info = {}
        
        # OS Information
        info['os'] = {}
        try:
            info['os']['name'] = distro.name(pretty=True)
            info['os']['version'] = distro.version()
            info['os']['id'] = distro.id()
            info['os']['codename'] = distro.codename()
        except:
            info['os']['name'] = platform.system()
            info['os']['version'] = platform.release()
            info['os']['id'] = platform.system().lower()
            info['os']['codename'] = 'Unknown'
        
        info['os']['kernel'] = platform.release()
        info['os']['architecture'] = platform.machine()
        
        # System uptime
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                hours, remainder = divmod(uptime_seconds, 3600)
                days, hours = divmod(hours, 24)
                info['os']['uptime'] = f"{int(days)} days, {int(hours)} hours, {int(remainder // 60)} minutes"
        except:
            info['os']['uptime'] = 'Unknown'
        
        # CPU Info
        info['cpu'] = self.get_cpu_info()
        
        # Memory Info
        info['memory'] = self.get_memory_info()
        
        # Disk Info
        info['disk'] = self.get_disk_info()
        
        # Network Info
        info['network'] = self.get_network_info()
        
        # User Info
        info['user'] = self.get_user_info()
        
        # Time Info
        info['time'] = {
            'current': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timezone': datetime.now().astimezone().tzinfo,
            'timestamp': datetime.now().timestamp()
        }
        
        # Current Directory
        info['cwd'] = os.getcwd()
        
        # Environment Info
        info['env'] = {
            'shell': os.environ.get('SHELL', 'Unknown'),
            'term': os.environ.get('TERM', 'Unknown'),
            'lang': os.environ.get('LANG', 'Unknown'),
            'display': os.environ.get('DISPLAY', 'None')
        }
        
        return info

    def bytes_to_human(self, bytes_value):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def display_header(self):
        """Display the logo and system info"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Get logo lines
        logo_lines = self.get_ascii_logo_colored().split('\n')
        info = self.system_info
        
        # Prepare system and user info lines (to be displayed beside the logo)
        sys_info_lines = [
            f"{Colors.BOLD_CYAN}=== SYSTEM INFO ==={Colors.RESET}",
            f"  OS:      {info['os']['name']}",
            f"  Kernel:  {info['os']['kernel']}",
            f"  Arch:    {info['os']['architecture']}",
            f"  Uptime:  {info['os']['uptime']}",
            "",
            f"{Colors.BOLD_CYAN}=== USER INFO ==={Colors.RESET}",
            f"  User:    {info['user']['username']}",
            f"  Shell:   {info['user']['shell']}",
            f"  Home:    {info['user']['home']}",
            "",
            f"{Colors.BOLD_YELLOW}=== COLOR TEST ==={Colors.RESET}",
            self.get_color_test_grid()
        ]
        
        # Print logo with system info beside it
        max_logo_height = len(logo_lines)
        max_info_height = len(sys_info_lines)
        max_height = max(max_logo_height, max_info_height)
        
        # Pad both to same height
        logo_lines_padded = logo_lines + [''] * (max_height - max_logo_height)
        sys_info_lines_padded = sys_info_lines + [''] * (max_height - max_info_height)
        
        # Print side by side
        for i in range(max_height):
            logo_part = logo_lines_padded[i] if i < max_logo_height else ''
            info_part = sys_info_lines_padded[i] if i < max_info_height else ''
            # Add spacing between logo and info
            print(f"{logo_part:<50}  {info_part}")
        
        print("=" * 80)
        
        # Hardware Information (below the logo and system info)
        print(f"{Colors.BOLD_CYAN}=== HARDWARE INFORMATION ==={Colors.RESET}")
        print(f"  CPU:           {info['cpu']['model']}")
        print(f"  CPU Cores:     {info['cpu']['physical_cores']} physical, {info['cpu']['cores']} logical")
        print(f"  CPU Usage:     {info['cpu']['usage_percent']}%")
        if info['cpu']['frequency'] != 'Unknown':
            print(f"  CPU Freq:      {info['cpu']['frequency']}")
        print(f"  Memory:        {info['memory']['total']} total")
        print(f"  Memory Usage:  {info['memory']['percent']}% (used: {info['memory']['used']})")
        if info['memory']['swap_total'] != 'N/A':
            print(f"  Swap:          {info['memory']['swap_total']} total, {info['memory']['swap_percent']}% used")
        
        # Show first disk
        if info['disk']:
            disk = info['disk'][0]
            print(f"\n{Colors.BOLD_CYAN}=== DISK INFORMATION ==={Colors.RESET}")
            print(f"  Root Disk:     {disk['device']} ({disk['fstype']})")
            print(f"  Size:          {disk['total']} total, {disk['used']} used")
            print(f"  Usage:         {disk['percent']}%")
        
        # Network Information
        print(f"\n{Colors.BOLD_CYAN}=== NETWORK INFORMATION ==={Colors.RESET}")
        print(f"  Hostname:      {info['network']['hostname']}")
        print(f"  IP Addresses:  {', '.join(info['network']['ips'][:3])}")
        if info['network']['macs'] and info['network']['macs'][0] != 'Unknown':
            print(f"  MAC Addresses: {', '.join(info['network']['macs'][:2])}")
        
        # Current Environment
        print(f"\n{Colors.BOLD_CYAN}=== CURRENT ENVIRONMENT ==={Colors.RESET}")
        print(f"  Time:          {info['time']['current']} ({info['time']['timezone']})")
        print(f"  Directory:     {info['cwd']}")
        print(f"  Shell:         {info['env']['shell']}")
        print(f"  Terminal:      {info['env']['term']}")
        print("=" * 80)
        print(f"  {Colors.BOLD_GREEN}Type 'help' for available commands{Colors.RESET}")
        print(f"  {Colors.BOLD_YELLOW}Type 'pcc [color]' to change prompt color{Colors.RESET}")
        print("=" * 80)
        print()

    def change_prompt_color(self, color_name):
        """Change the prompt color"""
        color_name = color_name.lower()
        if color_name in self.available_colors:
            self.prompt_color = self.available_colors[color_name]
            self.prompt_color_name = color_name
            print(f"{Colors.GREEN}✓ Prompt color changed to '{color_name}'{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}✗ Invalid color: '{color_name}'{Colors.RESET}")
            print(f"{Colors.YELLOW}Available colors: {', '.join(self.available_colors.keys())}{Colors.RESET}")
            return False

    def show_available_colors(self):
        """Display available colors with preview"""
        print(f"\n{Colors.BOLD_CYAN}Available Prompt Colors:{Colors.RESET}")
        for name, code in self.available_colors.items():
            preview = f"{code}■{Colors.RESET}"
            current = " ★" if name == self.prompt_color_name else ""
            print(f"  {name:15} {preview} {current}")
        print()

    def execute_command(self, cmd):
        """Execute the command"""
        if not cmd.strip():
            return True
            
        # Handle built-in commands
        if cmd.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            self.save_history()
            return False
            
        if cmd.lower() == 'cls' or cmd.lower() == 'clear':
            self.system_info = self.get_system_info()
            self.display_header()
            return True
            
        if cmd.lower() == 'help':
            self.show_help()
            return True
            
        if cmd.lower() == 'logo':
            print(self.get_ascii_logo_colored())
            return True
            
        if cmd.lower() == 'sysinfo':
            self.system_info = self.get_system_info()
            self.display_header()
            return True
            
        if cmd.lower() == 'aliases':
            self.show_aliases()
            return True
            
        if cmd.lower() == 'refresh':
            self.system_info = self.get_system_info()
            print(f"{Colors.GREEN}✓ System information refreshed!{Colors.RESET}")
            return True
            
        if cmd.lower() == 'colors':
            self.show_available_colors()
            return True
            
        # Handle prompt color change command
        if cmd.lower().startswith('pcc '):
            color_name = cmd[4:].strip()
            self.change_prompt_color(color_name)
            return True

        # Handle shell commands
        try:
            # Handle cd command with directory display
            if cmd.strip().startswith('cd '):
                new_dir = cmd.strip()[3:].strip()
                try:
                    os.chdir(os.path.expanduser(new_dir))
                    # Update the directory in system info
                    self.system_info['cwd'] = os.getcwd()
                    # Display the new directory in the requested format
                    current_path = os.getcwd()
                    # Show full path or just the directory name
                    print(f"[{current_path}] ->")
                except Exception as e:
                    print(f"Error: {e}")
                return True
                
            # Execute the command in shell
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                executable='/bin/bash' if os.name == 'posix' else None
            )
            
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='', file=sys.stderr)
                
            return True
            
        except KeyboardInterrupt:
            print("\nCommand interrupted")
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return True

    def get_prompt_with_directory(self):
        """Get the prompt with current directory"""
        current_dir = os.getcwd()
        
        # Get the directory name or full path
        # If in home directory, show ~
        home = os.path.expanduser('~')
        if current_dir.startswith(home):
            display_dir = '~' + current_dir[len(home):]
        else:
            display_dir = current_dir
            
        # Return the prompt with directory in brackets
        return f"{self.prompt_color}[{display_dir}] {self.prompt_text}{Colors.RESET} "

    def show_help(self):
        """Display help information"""
        help_text = f"""
{Colors.BOLD_YELLOW}Available Commands:{Colors.RESET}
  {Colors.GREEN}help{Colors.RESET}               - Show this help message
  {Colors.GREEN}exit, quit, q{Colors.RESET}      - Exit the terminal
  {Colors.GREEN}clear, cls{Colors.RESET}         - Clear screen and show header
  {Colors.GREEN}logo{Colors.RESET}               - Display the ASCII logo
  {Colors.GREEN}sysinfo{Colors.RESET}            - Display system information (logo + info)
  {Colors.GREEN}aliases{Colors.RESET}            - Show available aliases
  {Colors.GREEN}refresh{Colors.RESET}            - Refresh system information
  {Colors.GREEN}colors{Colors.RESET}             - Show available prompt colors
  {Colors.GREEN}pcc [color]{Colors.RESET}        - Change prompt color (e.g., pcc blue)
  
  {Colors.GREEN}cd <directory>{Colors.RESET}     - Change current directory (shows path in prompt)
  Any other command  - Executed in the system shell

{Colors.BOLD_YELLOW}Available Colors for Prompt:{Colors.RESET}
  {Colors.YELLOW}black, red, green, yellow, blue, purple, cyan, white,{Colors.RESET}
  {Colors.YELLOW}light_white, bold_black, bold_red, bold_green, bold_yellow,{Colors.RESET}
  {Colors.YELLOW}bold_blue, bold_purple, bold_cyan{Colors.RESET}

{Colors.BOLD_YELLOW}Aliases:{Colors.RESET}
  exit, quit, q      -> exit the terminal
  clear, cls         -> clear the screen

{Colors.BOLD_YELLOW}Special Features:{Colors.RESET}
  - Command history (use up/down arrows)
  - REAL system information detection
  - Colored ASCII logo (Light Blue top, Blue middle, Dark Blue bottom)
  - System/User info displayed beside the logo
  - 16-color test grid displayed under system info
  - Customizable prompt colors
  - Directory shown in prompt: [path] ➜
  - Shows CPU, memory, disk usage
  - Network information
  - User and group information
  - System uptime
"""
        print(help_text)

    def show_aliases(self):
        """Display aliases"""
        print(f"\n{Colors.BOLD_YELLOW}Available Aliases:{Colors.RESET}")
        for alias, command in self.aliases.items():
            print(f"  {alias:10} -> {command}")
        print()

    def run(self):
        """Main loop"""
        self.display_header()
        
        while True:
            try:
                # Get command with directory in prompt
                prompt = self.get_prompt_with_directory()
                cmd = input(prompt).strip()
                
                # Handle empty command
                if not cmd:
                    continue
                    
                # Process aliases
                if cmd.split()[0] in self.aliases:
                    parts = cmd.split()
                    parts[0] = self.aliases[parts[0]]
                    cmd = ' '.join(parts)
                
                # Execute the command
                if not self.execute_command(cmd):
                    break
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")

def install_dependencies():
    """Install required dependencies"""
    dependencies = ['psutil', 'distro', 'netifaces']
    
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            print(f"Installing required package '{dep}'...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True)
                print(f"✓ {dep} installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {dep}: {e}")
                return False
    return True

def main():
    """Main entry point"""
    # Check if running on Linux
    if not os.name == 'posix':
        print("Warning: This tool is designed for Linux/Unix systems")
        print("Some features may not work properly on other systems")
    
    # Install dependencies
    if not install_dependencies():
        print("\nFailed to install all dependencies. Some features may not work.")
        print("You can manually install: pip install psutil distro netifaces")
        input("Press Enter to continue...")
    
    # Run the terminal
    terminal = CustomTerminal()
    try:
        terminal.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()