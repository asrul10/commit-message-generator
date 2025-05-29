# AI Git Commit Message Generator

A simple command-line tool that generates conventional commit messages using OpenAI's GPT model based on your staged git changes.

## Features

- Automatically generates [commitizen](https://github.com/commitizen/cz-cli) style conventional commit messages
- Uses OpenAI's GPT-4o-mini model for intelligent message generation
- Option to push changes after commit
- Properly formatted commit messages with title under 50 characters and body wrapped at 72 characters

## Prerequisites

- Python 3.6+
- Git
- OpenAI API key

## Installation

### Option 1: Use as Python script

1. Clone this repository
2. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Run the script:
   ```
   python main.py
   ```

### Option 2: Use as standalone executable

Download the prebuilt executable from the releases section or build it yourself using PyInstaller (see below).

## Building with PyInstaller

To create a standalone executable:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Build the executable:
   ```
   pyinstaller --onefile main.py --name acm
   ```

3. Find the executable in the `dist` directory

## Usage

1. Stage your changes with `git add`
2. Run the script or executable
3. Review the generated commit message
4. Confirm to commit and optionally push changes
