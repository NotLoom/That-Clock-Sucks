# That Clock Sucks

A terminal-based digital clock with customizable display options.

<img width="961" height="520" alt="Screenshot_05-Sep_18-54-08_7501" src="https://github.com/user-attachments/assets/5aec1e1a-d4fc-4b2f-b660-75d36b921124" />

## Features

- Large ASCII digital clock display
- 5 different ASCII font variations
- Customizable time format (12/24 hour, with or without seconds)
- Date display with multiple format options
- Interactive menu for configuration
- Arrow key navigation
- Configuration persistence
- Automatic update checking
- Color customization (8 color options including rainbow mode)

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/NotLoom/That-Clock-Sucks.git
cd That-Clock-Sucks

# Make the installer executable
chmod +x install.sh

# Run the installer
./install.sh
```

### Manual Install

```bash
# Clone the repository
git clone https://github.com/NotLoom/That-Clock-Sucks.git
cd That-Clock-Sucks

# Make scripts executable
chmod +x main.py clock-sucks

# Copy to a directory in your PATH (e.g., ~/bin)
cp main.py clock-sucks ~/bin/

# Or copy to /usr/local/bin for system-wide access (requires sudo)
sudo cp main.py clock-sucks /usr/local/bin/
```

## Usage

After installation, simply type `clock-sucks` in your terminal:

```bash
clock-sucks
```

### Controls

- **F1** or **m**: Open/close the settings menu
- **F2**: Toggle visibility of "Press F1 for menu" hint
- **Up/Down Arrow Keys**: Navigate menu options
- **Enter** or **Space**: Select/toggle menu options
- **ESC**: Close the menu

### Settings Menu

- **Show seconds**: Toggle seconds display on/off
- **Show date**: Toggle date display on/off
- **Date format options**:
  - DD/MM/YYYY (Day/Month/Year)
  - MM/DD/YYYY (Month/Day/Year)
  - YYYY/MM/DD (Year/Month/Day)
- **Font**: Cycle through 5 different ASCII font variations:
  - Original (default)
  - Thick
  - Thin
  - Compact
  - Wide
- **Color**: Cycle through 8 color options:
  - White (default)
  - Red
  - Green
  - Yellow
  - Blue
  - Magenta
  - Cyan
  - Rainbow (each row a different color)
- **Time format**: Toggle between 12-hour and 24-hour format
- **AM/PM display**: Toggle AM/PM indicator for 12-hour format
- **Version**: Display current application version
- **Check for updates**: Check for new versions on GitHub
- **Exit menu**: Close the settings menu

## Requirements

- Python 3.x
- curses library (usually included with Python on Unix-like systems)
- Terminal with color support (for color features)
- Internet connection (for update checking)

## License

MIT
