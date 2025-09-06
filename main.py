#!/usr/bin/env python3
import curses
import time
from datetime import datetime
import sys
import os
import json
import urllib.request
import urllib.error

# Application version
VERSION = "0.0.1"

# Configuration file path
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

# GitHub repository information
GITHUB_REPO = "NotLoom/That-Clock-Sucks"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def load_config():
    """Load user configuration from file"""
    default_config = {
        "show_seconds": True,
        "show_date": True,
        "date_format": "%m/%d/%Y",
        "show_menu_hint": True,
        "current_font": 0,
        "current_color": 0,
        "time_format_12hour": False,
        "show_ampm": True
    }
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with default config to ensure all keys are present
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            # Create config file with default settings
            save_config(default_config)
            return default_config
    except Exception as e:
        # If there's any error, return default config
        return default_config

def save_config(config):
    """Save user configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        # Silently fail if we can't save config
        pass

def check_for_updates():
    """Check for updates from GitHub"""
    try:
        # Create request with proper headers
        request = urllib.request.Request(
            GITHUB_API_URL,
            headers={'User-Agent': 'That-Clock-Sucks/0.0.1'}
        )
        
        # Make the request
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            
        # Extract version information
        latest_version = data.get('tag_name', 'unknown').lstrip('v')  # Remove 'v' prefix if present
        release_url = data.get('html_url', '')
        
        return {
            'version': latest_version,
            'url': release_url,
            'available': True
        }
    except Exception as e:
        return {
            'version': 'unknown',
            'url': '',
            'available': False,
            'error': str(e)
        }

def auto_update():
    """Automatically download and install the latest version"""
    try:
        # Get the latest release information
        request = urllib.request.Request(
            GITHUB_API_URL,
            headers={'User-Agent': 'That-Clock-Sucks/0.0.1'}
        )
        
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
        
        # Get the download URL for the zipball
        zipball_url = data.get('zipball_url', '')
        release_tag = data.get('tag_name', '').lstrip('v')
        
        if not zipball_url:
            return False, "No download URL found"
        
        # Get the current script path
        current_script = os.path.abspath(__file__)
        
        # Download the zipball to a temporary location
        temp_zip = current_script + '.zip.tmp'
        urllib.request.urlretrieve(zipball_url, temp_zip)
        
        # Extract the zipball to a temporary directory
        import tempfile
        import zipfile
        import shutil
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the extracted directory (it will be the only item)
            extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            
            # Look for main.py in the extracted directory
            new_main_py = os.path.join(extracted_dir, 'main.py')
            
            if not os.path.exists(new_main_py):
                return False, "New main.py not found in update"
            
            # Replace the current main.py with the new one
            shutil.copy2(new_main_py, current_script)
        
        # Clean up temporary files
        os.remove(temp_zip)
        
        return True, f"Updated to version {release_tag}"
        
    except Exception as e:
        return False, f"Update failed: {str(e)}"

# Define multiple font variations for the ASCII clock display
FONTS = [
    # Original Font
    {
        '0': [' ███ ', '█   █', '█   █', '█   █', ' ███ '],
        '1': ['  █  ', ' ██  ', '  █  ', '  █  ', '█████'],
        '2': [' ███ ', '    █', ' ███ ', '█    ', '█████'],
        '3': [' ███ ', '    █', ' ███ ', '    █', ' ███ '],
        '4': ['█   █', '█   █', ' ████', '    █', '    █'],
        '5': ['█████', '█    ', ' ███ ', '    █', ' ███ '],
        '6': [' ███ ', '█    ', '████ ', '█   █', ' ███ '],
        '7': ['█████', '    █', '   █ ', '  █  ', ' █   '],
        '8': [' ███ ', '█   █', ' ███ ', '█   █', ' ███ '],
        '9': [' ███ ', '█   █', ' ████', '    █', ' ███ '],
        ':': ['     ', '  █  ', '     ', '  █  ', '     '],
        'A': [' ███ ', '█   █', '█████', '█   █', '█   █'],
        'M': ['█   █', '██ ██', '█ █ █', '█   █', '█   █'],
        'P': ['████ ', '█   █', '████ ', '█    ', '█    ']
    },
    # Thick Font - Fixed bottom alignment
    {
        '0': ['█████', '█   █', '█   █', '█   █', '█████'],
        '1': ['  ██ ', '  ██ ', '  ██ ', '  ██ ', '  ██ '],
        '2': ['█████', '    █', '█████', '█    ', '█████'],
        '3': ['█████', '    █', '█████', '    █', '█████'],
        '4': ['█   █', '█   █', '█████', '    █', '    █'],
        '5': ['█████', '█    ', '█████', '    █', '█████'],
        '6': ['█████', '█    ', '█████', '█   █', '█████'],
        '7': ['█████', '    █', '   █ ', '  █  ', ' █   '],
        '8': ['█████', '█   █', '█████', '█   █', '█████'],
        '9': ['█████', '█   █', '█████', '    █', '█████'],
        ':': ['     ', '  ██ ', '     ', '  ██ ', '     '],
        'A': [' ███ ', '█   █', '█████', '█   █', '█   █'],
        'M': ['█   █', '██ ██', '█ █ █', '█   █', '█   █'],
        'P': ['████ ', '█   █', '████ ', '█    ', '█    ']
    },
    # Thin Font
    {
        '0': [' ███ ', '█   █', '█   █', '█   █', ' ███ '],
        '1': ['  █  ', '  █  ', '  █  ', '  █  ', '  █  '],
        '2': ['█████', '    █', '█████', '█    ', '█████'],
        '3': ['█████', '    █', '█████', '    █', '█████'],
        '4': ['█   █', '█   █', '█████', '    █', '    █'],
        '5': ['█████', '█    ', '█████', '    █', '█████'],
        '6': [' ███ ', '█    ', '█████', '█   █', ' ███ '],
        '7': ['█████', '    █', '   █ ', '  █  ', ' █   '],
        '8': [' ███ ', '█   █', ' ███ ', '█   █', ' ███ '],
        '9': [' ███ ', '█   █', '█████', '    █', ' ███ '],
        ':': ['  █  ', '  █  ', '     ', '  █  ', '  █  '],
        'A': [' ███ ', '█   █', '█████', '█   █', '█   █'],
        'M': ['█   █', '██ ██', '█ █ █', '█   █', '█   █'],
        'P': ['█████', '█   █', '█████', '█    ', '█    ']
    },
    # Compact Font
    {
        '0': [' ██ ', '█  █', '█  █', '█  █', ' ██ '],
        '1': [' █ ', ' █ ', ' █ ', ' █ ', ' █ '],
        '2': ['███', '  █', '███', '█  ', '███'],
        '3': ['███', '  █', '███', '  █', '███'],
        '4': ['█ █', '█ █', '███', '  █', '  █'],
        '5': ['███', '█  ', '███', '  █', '███'],
        '6': [' ██', '█  ', '███', '█ █', ' ██'],
        '7': ['███', '  █', '  █', '  █', '  █'],
        '8': [' ██', '█ █', ' ██', '█ █', ' ██'],
        '9': [' ██', '█ █', '███', '  █', ' ██'],
        ':': ['   ', ' █ ', '   ', ' █ ', '   '],
        'A': [' ██ ', '█  █', '████', '█  █', '█  █'],
        'M': ['█  █', '██ ██', '█ █ █', '█  █', '█  █'],
        'P': ['███ ', '█  █', '███ ', '█   ', '█   ']
    },
    # Wide Font - Fixed right alignment
    {
        '0': ['  █████  ', ' ██   ██ ', ' ██   ██ ', ' ██   ██ ', '  █████  '],
        '1': ['   ██    ', '   ██    ', '   ██    ', '   ██    ', ' ███████ '],
        '2': [' ██████  ', '     ██  ', ' ██████  ', ' ██      ', ' ███████ '],
        '3': [' ██████  ', '     ██  ', ' ██████  ', '     ██  ', ' ██████  '],
        '4': [' ██   ██ ', ' ██   ██ ', ' ███████ ', '     ██  ', '     ██  '],
        '5': [' ███████ ', ' ██      ', ' ██████  ', '     ██  ', ' ██████  '],
        '6': ['  █████  ', ' ██      ', ' ██████  ', ' ██   ██ ', '  █████  '],
        '7': [' ███████ ', '     ██  ', '    ██   ', '   ██    ', '  ██     '],
        '8': ['  █████  ', ' ██   ██ ', '  █████  ', ' ██   ██ ', '  █████  '],
        '9': ['  █████  ', ' ██   ██ ', '  ██████ ', '     ██  ', '  █████  '],
        ':': ['        ', '   ██   ', '        ', '   ██   ', '        '],
        'A': ['  █████  ', ' ██   ██ ', ' ███████ ', ' ██   ██ ', ' ██   ██ '],
        'M': [' ██   ██ ', ' ███ ███ ', ' ██ █ ██ ', ' ██   ██ ', ' ██   ██ '],
        'P': [' ██████  ', ' ██   ██ ', ' ██████  ', ' ██      ', ' ██      ']
    }
]

class ClockApp:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
        # Load user configuration
        config = load_config()
        self.show_seconds = config["show_seconds"]
        self.show_date = config["show_date"]
        self.date_format = config["date_format"]
        self.show_menu_hint = config["show_menu_hint"]
        self.current_font = config["current_font"]
        self.current_color = config.get("current_color", 0)  # 0 = white, 1-7 = basic colors, 8 = rainbow
        self.time_format_12hour = config.get("time_format_12hour", False)  # False = 24-hour, True = 12-hour
        self.show_ampm = config.get("show_ampm", True)  # Whether to show AM/PM in 12-hour mode
        
        self.menu_open = False
        self.selected_menu_item = 0
        self.font_names = ["Original", "Thick", "Thin", "Compact", "Wide"]
        self.color_names = ["White", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "Rainbow"]
        self.menu_items = [
            "Show seconds",
            "Show date",
            "Date format: DD/MM/YYYY",
            "Date format: MM/DD/YYYY",
            "Date format: YYYY/MM/DD",
            "Font: Original",
            f"Version: {VERSION}",
            "Color: White",
            "Time format: 24-hour",
            "Show AM/PM",
            "Run at startup (Arch Linux)",
            "Check for updates",
            "Exit menu"
        ]
        
        # Initialize curses settings
        try:
            curses.curs_set(0)  # Hide cursor
        except:
            pass  # Some terminals don't support this
            
        # Initialize color support
        if curses.has_colors():
            curses.start_color()
            # Define color pairs
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
            
        self.stdscr.nodelay(True)  # Non-blocking input
        self.stdscr.timeout(200)  # Refresh every 200ms
        
        # Update menu items to reflect loaded configuration
        self.update_menu_items()
    
    def update_menu_items(self):
        """Update menu items to reflect current configuration"""
        # Update date format menu items
        if self.date_format == "%d/%m/%Y":
            self.menu_items[2] = "(●) Date format: DD/MM/YYYY"
            self.menu_items[3] = "( ) Date format: MM/DD/YYYY"
            self.menu_items[4] = "( ) Date format: YYYY/MM/DD"
        elif self.date_format == "%m/%d/%Y":
            self.menu_items[2] = "( ) Date format: DD/MM/YYYY"
            self.menu_items[3] = "(●) Date format: MM/DD/YYYY"
            self.menu_items[4] = "( ) Date format: YYYY/MM/DD"
        elif self.date_format == "%Y/%m/%d":
            self.menu_items[2] = "( ) Date format: DD/MM/YYYY"
            self.menu_items[3] = "( ) Date format: MM/DD/YYYY"
            self.menu_items[4] = "(●) Date format: YYYY/MM/DD"
            
        # Update font menu item
        self.menu_items[5] = f"Font: {self.font_names[self.current_font]}"
        
        # Update color menu item
        self.menu_items[7] = f"Color: {self.color_names[self.current_color]}"
        
        # Update time format menu items
        if self.time_format_12hour:
            self.menu_items[8] = "(●) Time format: 12-hour"
            self.menu_items[9] = "( ) Show AM/PM" if self.show_ampm else "(●) Show AM/PM"
        else:
            self.menu_items[8] = "( ) Time format: 12-hour"
            self.menu_items[9] = "( ) Show AM/PM"  # Disabled in 24-hour mode
        
    def display_clock(self):
        """Display the large ASCII clock"""
        # Format time string based on settings
        if self.time_format_12hour:
            # 12-hour format
            if self.show_seconds:
                time_str = time.strftime('%I:%M:%S')
            else:
                time_str = time.strftime('%I:%M')
                
            # Add AM/PM if enabled
            if self.show_ampm:
                ampm = time.strftime('%p')  # Returns 'AM' or 'PM'
                time_str += f" {ampm}"
        else:
            # 24-hour format
            if self.show_seconds:
                time_str = time.strftime('%H:%M:%S')
            else:
                time_str = time.strftime('%H:%M')
            
        # Use the selected font
        current_font = FONTS[self.current_font]
        rows = [''] * 5
        for char in time_str:
            seg = current_font.get(char, ['     '] * 5)
            for i in range(5):
                rows[i] += seg[i] + '  '
        
        # Display the clock in the center of the screen
        height, width = self.stdscr.getmaxyx()
        clock_width = len(rows[0])
        start_x = max(0, (width - clock_width) // 2)
        start_y = max(0, (height // 2) - 3)
        
        # Clear screen and display clock
        self.stdscr.clear()
        for i, row in enumerate(rows):
            if start_y + i < height:
                try:
                    # Apply color based on selection
                    if self.current_color == 7:  # Rainbow mode
                        # For rainbow, we'll cycle through colors for each row
                        color_pair = (i % 6) + 1  # Use colors 1-6
                        if curses.has_colors():
                            self.stdscr.addstr(start_y + i, start_x, row, curses.color_pair(color_pair))
                        else:
                            self.stdscr.addstr(start_y + i, start_x, row)
                    elif self.current_color > 0 and self.current_color < 7 and curses.has_colors():  # Basic color
                        self.stdscr.addstr(start_y + i, start_x, row, curses.color_pair(self.current_color))
                    else:  # White or no color support
                        self.stdscr.addstr(start_y + i, start_x, row)
                except:
                    pass  # Handle terminal size issues
        
        # Display date if enabled
        if self.show_date and start_y + 6 < height:
            try:
                date_str = datetime.now().strftime(self.date_format)
                date_x = max(0, (width - len(date_str)) // 2)
                # Apply same color to date
                if self.current_color == 7:  # Rainbow mode
                    if curses.has_colors():
                        self.stdscr.addstr(start_y + 6, date_x, date_str, curses.color_pair(1))
                    else:
                        self.stdscr.addstr(start_y + 6, date_x, date_str)
                elif self.current_color > 0 and self.current_color < 7 and curses.has_colors():  # Basic color
                    self.stdscr.addstr(start_y + 6, date_x, date_str, curses.color_pair(self.current_color))
                else:  # White or no color support
                    self.stdscr.addstr(start_y + 6, date_x, date_str)
            except:
                pass  # Handle terminal size issues
        
        # Display menu hint if enabled
        if self.show_menu_hint:
            try:
                hint = "Press F1 for menu"
                hint_x = max(0, width - len(hint) - 2)
                self.stdscr.addstr(1, hint_x, hint)
            except:
                pass  # Handle terminal size issues
        
        # Display menu if open
        if self.menu_open:
            self.display_menu()
            
        self.stdscr.refresh()
    
    def display_menu(self):
        """Display the configuration menu"""
        try:
            height, width = self.stdscr.getmaxyx()
            
            # Menu dimensions
            menu_width = 40
            menu_height = len(self.menu_items) + 4
            start_x = max(0, (width - menu_width) // 2)
            start_y = max(0, (height - menu_height) // 2)
            
            # Draw menu border
            try:
                self.stdscr.addstr(start_y, start_x, "+" + "-" * (menu_width - 2) + "+")
                for i in range(1, menu_height - 1):
                    self.stdscr.addstr(start_y + i, start_x, "|" + " " * (menu_width - 2) + "|")
                self.stdscr.addstr(start_y + menu_height - 1, start_x, "+" + "-" * (menu_width - 2) + "+")
            except:
                return  # Handle terminal size issues
            
            # Draw menu title
            title = "Clock Settings"
            title_x = start_x + (menu_width - len(title)) // 2
            self.stdscr.addstr(start_y + 1, title_x, title)
            
            # Draw menu items
            for i, item in enumerate(self.menu_items):
                item_y = start_y + i + 3
                item_x = start_x + 2
                
                # Update menu items to show current selections
                if i == 0:  # Show seconds
                    marker = "[●]" if self.show_seconds else "[ ]"
                    display_item = f"{marker} {item}"
                elif i == 1:  # Show date
                    marker = "[●]" if self.show_date else "[ ]"
                    display_item = f"{marker} {item}"
                elif i == 2:  # DD/MM/YYYY
                    marker = "(●)" if self.date_format == "%d/%m/%Y" else "( )"
                    display_item = f"{marker} {item.replace('(●) ', '').replace('( ) ', '')}"
                elif i == 3:  # MM/DD/YYYY
                    marker = "(●)" if self.date_format == "%m/%d/%Y" else "( )"
                    display_item = f"{marker} {item.replace('(●) ', '').replace('( ) ', '')}"
                elif i == 4:  # YYYY/MM/DD
                    marker = "(●)" if self.date_format == "%Y/%m/%d" else "( )"
                    display_item = f"{marker} {item.replace('(●) ', '').replace('( ) ', '')}"
                elif i == 5:  # Font
                    display_item = item
                elif i == 6:  # Version (info only)
                    display_item = item
                elif i == 7:  # Color
                    display_item = item
                elif i == 8:  # Time format: 12-hour
                    marker = "(●)" if self.time_format_12hour else "( )"
                    display_item = f"{marker} {item.replace('(●) ', '').replace('( ) ', '')}"
                elif i == 9:  # Show AM/PM
                    # Only show selection marker if 12-hour format is enabled
                    if self.time_format_12hour:
                        marker = "(●)" if self.show_ampm else "( )"
                        display_item = f"{marker} {item.replace('(●) ', '').replace('( ) ', '')}"
                    else:
                        display_item = f"( ) {item} (disabled)"  # Disabled in 24-hour mode
                elif i == 10:  # Run at startup (Arch Linux)
                    # Show whether startup is enabled or not
                    if self.is_enabled_at_startup():
                        display_item = "✓ Run at startup (Arch Linux)"
                    else:
                        display_item = "Run at startup (Arch Linux)"
                else:
                    display_item = item
                    
                # Highlight selected item
                try:
                    if i == self.selected_menu_item:
                        self.stdscr.addstr(item_y, item_x, f"> {display_item}", curses.A_REVERSE)
                    else:
                        self.stdscr.addstr(item_y, item_x, f"  {display_item}")
                except:
                    pass  # Handle terminal size issues
        except:
            pass  # Handle any other terminal issues
    
    def handle_input(self):
        """Handle user input"""
        try:
            key = self.stdscr.getch()
            
            if key == -1:  # No input
                return True
                
            # Handle F1 to toggle menu
            if key == curses.KEY_F1 or key == ord('m'):
                self.menu_open = not self.menu_open
                self.selected_menu_item = 0
                return True
                
            # Handle F2 to toggle menu hint
            if key == curses.KEY_F2:
                self.show_menu_hint = not self.show_menu_hint
                # Save configuration when menu hint visibility changes
                config = {
                    "show_seconds": self.show_seconds,
                    "show_date": self.show_date,
                    "date_format": self.date_format,
                    "show_menu_hint": self.show_menu_hint,
                    "current_font": self.current_font,
                    "current_color": self.current_color,
                    "time_format_12hour": self.time_format_12hour,
                    "show_ampm": self.show_ampm
                }
                save_config(config)
                return True
                
            # Handle ESC to close menu
            if key == 27:  # ESC key
                self.menu_open = False
                return True
                
            # Handle menu navigation
            if self.menu_open:
                if key == curses.KEY_UP:
                    self.selected_menu_item = (self.selected_menu_item - 1) % len(self.menu_items)
                elif key == curses.KEY_DOWN:
                    self.selected_menu_item = (self.selected_menu_item + 1) % len(self.menu_items)
                elif key == ord('\n') or key == ord(' '):  # Enter or Space key
                    self.handle_menu_selection()
                    
            return True
        except Exception as e:
            return False
    
    def handle_menu_selection(self):
        """Handle menu item selection"""
        if self.selected_menu_item == 0:  # Toggle seconds
            self.show_seconds = not self.show_seconds
        elif self.selected_menu_item == 1:  # Toggle date
            self.show_date = not self.show_date
        elif self.selected_menu_item == 2:  # DD/MM/YYYY
            self.date_format = "%d/%m/%Y"
        elif self.selected_menu_item == 3:  # MM/DD/YYYY
            self.date_format = "%m/%d/%Y"
        elif self.selected_menu_item == 4:  # YYYY/MM/DD
            self.date_format = "%Y/%m/%d"
        elif self.selected_menu_item == 5:  # Font selection
            self.current_font = (self.current_font + 1) % len(FONTS)
        elif self.selected_menu_item == 6:  # Version info (non-actionable)
            pass  # Do nothing, just display info
        elif self.selected_menu_item == 7:  # Color selection
            self.current_color = (self.current_color + 1) % len(self.color_names)
        elif self.selected_menu_item == 8:  # Toggle 12/24-hour format
            self.time_format_12hour = not self.time_format_12hour
        elif self.selected_menu_item == 9:  # Toggle AM/PM display
            self.show_ampm = not self.show_ampm
        elif self.selected_menu_item == 10:  # Run at startup (Arch Linux)
            self.toggle_startup()
        elif self.selected_menu_item == 11:  # Check for updates
            self.check_for_updates_menu()
        elif self.selected_menu_item == 12:  # Exit menu
            self.menu_open = False
            self.selected_menu_item = 0
        
        # Update menu items to reflect changes (except for version, startup and updates)
        if self.selected_menu_item not in [6, 10, 11]:
            self.update_menu_items()
        
        # Save configuration whenever settings change (except for version, startup and updates)
        if self.selected_menu_item not in [6, 10, 11]:
            config = {
                "show_seconds": self.show_seconds,
                "show_date": self.show_date,
                "date_format": self.date_format,
                "show_menu_hint": self.show_menu_hint,
                "current_font": self.current_font,
                "current_color": self.current_color,
                "time_format_12hour": self.time_format_12hour,
                "show_ampm": self.show_ampm
            }
            save_config(config)
    
    def check_for_updates_menu(self):
        """Check for updates and display result in menu"""
        # Update menu item to show checking status
        self.menu_items[11] = "Checking for updates..."
        self.display_menu()
        self.stdscr.refresh()
        
        # Check for updates
        update_info = check_for_updates()
        
        if update_info['available']:
            # Compare versions (simple string comparison for now)
            if update_info['version'] > VERSION:
                # Update available, prompt user to update
                self.menu_items[11] = f"Update {update_info['version']} available. Updating..."
                self.display_menu()
                self.stdscr.refresh()
                
                # Perform auto-update
                success, message = auto_update()
                
                if success:
                    self.menu_items[11] = "Update successful! Restarting..."
                    self.display_menu()
                    self.stdscr.refresh()
                    time.sleep(2)
                    
                    # Save current configuration before restarting
                    config = {
                        "show_seconds": self.show_seconds,
                        "show_date": self.show_date,
                        "date_format": self.date_format,
                        "show_menu_hint": self.show_menu_hint,
                        "current_font": self.current_font,
                        "current_color": self.current_color,
                        "time_format_12hour": self.time_format_12hour,
                        "show_ampm": self.show_ampm
                    }
                    save_config(config)
                    
                    # Restart the application
                    curses.endwin()
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    self.menu_items[11] = message
            else:
                self.menu_items[11] = "No updates available"
        else:
            self.menu_items[11] = "No updates available"
        
        # Keep the message visible for a few seconds (if not restarting)
        self.display_menu()
        self.stdscr.refresh()
        time.sleep(3)
        
        # Reset menu item
        self.menu_items[11] = "Check for updates"

    def is_arch_linux(self):
        """Check if the system is Arch Linux"""
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read()
                return 'ID=arch' in content
        except:
            return False

    def is_enabled_at_startup(self):
        """Check if the application is enabled to run at startup"""
        if not self.is_arch_linux():
            return False
            
        try:
            # Check if the systemd user service file exists
            service_file = os.path.expanduser('~/.config/systemd/user/that-clock-sucks.service')
            return os.path.exists(service_file)
        except:
            return False

    def toggle_startup(self):
        """Enable or disable the application to run at startup"""
        if not self.is_arch_linux():
            # Update menu to show error
            self.menu_items[8] = "Error: Not Arch Linux"
            self.display_menu()
            self.stdscr.refresh()
            time.sleep(2)
            self.menu_items[8] = "Run at startup (Arch Linux)"
            return
            
        try:
            # Create the systemd user directory if it doesn't exist
            systemd_dir = os.path.expanduser('~/.config/systemd/user')
            os.makedirs(systemd_dir, exist_ok=True)
            
            service_file = os.path.join(systemd_dir, 'that-clock-sucks.service')
            
            # If service file exists, disable and remove it
            if os.path.exists(service_file):
                # Disable the service
                os.system('systemctl --user disable that-clock-sucks.service 2>/dev/null')
                # Remove the service file
                os.remove(service_file)
                # Update menu to show disabled
                self.menu_items[8] = "Startup disabled"
            else:
                # Create the service file
                script_path = os.path.abspath(__file__)
                service_content = f"""[Unit]
Description=That Clock Sucks
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {script_path}
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
"""
                with open(service_file, 'w') as f:
                    f.write(service_content)
                
                # Reload systemd user daemon
                os.system('systemctl --user daemon-reload 2>/dev/null')
                # Enable the service
                os.system('systemctl --user enable that-clock-sucks.service 2>/dev/null')
                # Update menu to show enabled
                self.menu_items[8] = "Startup enabled"
                
            self.display_menu()
            self.stdscr.refresh()
            time.sleep(2)
            self.menu_items[8] = "Run at startup (Arch Linux)"
            
        except Exception as e:
            # Update menu to show error
            self.menu_items[8] = f"Error: {str(e)}"
            self.display_menu()
            self.stdscr.refresh()
            time.sleep(2)
            self.menu_items[8] = "Run at startup (Arch Linux)"

    def run(self):
        """Main application loop"""
        while True:
            self.display_clock()
            if not self.handle_input():
                break

def main():
    # Check if running in a terminal
    if not sys.stdin.isatty() or not os.environ.get('TERM'):
        # Fall back to simple clock if not in a proper terminal
        simple_clock()
        return
        
    try:
        curses.wrapper(curses_main)
    except Exception as e:
        # Fall back to simple clock if curses fails
        print(f"Terminal interface failed: {e}")
        print("Falling back to simple clock...")
        time.sleep(2)
        simple_clock()

def curses_main(stdscr):
    app = ClockApp(stdscr)
    app.run()

def simple_clock():
    """Simple version of the clock without curses interface"""
    # Use the original font for the simple clock
    digits = FONTS[0]
    while True:
        t = time.strftime('%H:%M:%S')
        rows = [''] * 5
        for char in t:
            seg = digits.get(char, ['     '] * 5)
            for i in range(5):
                rows[i] += seg[i] + '  '
        print('\033[2J\033[H' + '\n'.join(rows))
        time.sleep(1)

if __name__ == "__main__":
    main()