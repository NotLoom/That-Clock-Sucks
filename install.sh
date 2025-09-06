#!/bin/bash
# Installer script for That Clock Sucks

echo "Installing That Clock Sucks..."

# Check if running on a supported system
if [[ "$OSTYPE" != "linux-gnu"* && "$OSTYPE" != "darwin"* ]]; then
    echo "Warning: This installer is designed for Linux/macOS systems."
fi

# Make scripts executable
chmod +x main.py clock-sucks

# Determine installation directory
if [ -d "$HOME/bin" ]; then
    INSTALL_DIR="$HOME/bin"
elif [ -d "$HOME/.local/bin" ]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    # Create ~/bin if it doesn't exist
    INSTALL_DIR="$HOME/bin"
    mkdir -p "$INSTALL_DIR"
fi

# Copy files to installation directory
echo "Installing to $INSTALL_DIR..."
cp main.py "$INSTALL_DIR/"
cp clock-sucks "$INSTALL_DIR/"

# Check if INSTALL_DIR is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Warning: $INSTALL_DIR is not in your PATH."
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\$PATH:$INSTALL_DIR"
fi

echo "Installation complete!"
echo "You can now run the clock by typing 'clock-sucks' in your terminal."