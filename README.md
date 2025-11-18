# WhatsApp Bulk Sender

An automated Python solution for sending bulk messages via WhatsApp Web using Selenium WebDriver. This tool allows you to send personalized messages to multiple contacts efficiently while maintaining a human-like behavior to avoid detection.

**Note:** This project includes a pre-packaged ChromeDriver executable ([chromedriver.exe](file:///c%3A/Users/jnane/Documents/workspace/projects/whatsapp_bulk_sender/chromedriver.exe)) for Windows systems. If you're using a different operating system, you may need to download the appropriate version from the [ChromeDriver website](https://chromedriver.chromium.org/).

## Features

- **Automated Messaging**: Send customized messages to hundreds of contacts from a CSV file
- **Template Support**: Use placeholders in messages for personalization (name, phone, date, time)
- **QR Code Authentication**: Secure login through WhatsApp Web QR code scanning
- **Session Persistence**: Maintains login session between runs
- **Anti-Detection Measures**: Configured to minimize bot detection by WhatsApp
- **Retry Mechanism**: Automatically retries failed messages
- **Rate Limiting**: Random delays between messages to appear human-like
- **Progress Tracking**: Visual progress bar and detailed logging
- **Auto-Reply System**: Monitors for keywords and responds automatically
- **Error Handling**: Comprehensive error handling and recovery mechanisms
- **Audio Feedback**: Beeps for successful/failed message deliveries

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser (version compatible with included ChromeDriver)
- Active WhatsApp account on your phone

**About ChromeDriver:**
This project includes a pre-packaged ChromeDriver executable ([chromedriver.exe](file:///c%3A/Users/jnane/Documents/workspace/projects/whatsapp_bulk_sender/chromedriver.exe)) that is compatible with specific versions of Google Chrome. If you encounter compatibility issues, you may need to:
1. Check your Chrome version (Help > About Google Chrome)
2. Download the matching ChromeDriver version from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
3. Replace the existing [chromedriver.exe](file:///c%3A/Users/jnane/Documents/workspace/projects/whatsapp_bulk_sender/chromedriver.exe) file

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/whatsapp-bulk-sender.git
   cd whatsapp-bulk-sender
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Create a [contacts.csv](file:///c%3A/Users/jnane/Documents/workspace/projects/whatsapp_bulk_sender/contacts.csv) file in the project root with the following columns:
   ```csv
   Name,Phone,Message
   John Doe,+1234567890,Hello {name}, this is a test message!
   Jane Smith,+0987654321,Hi {name}, welcome to our service.
   ```

2. Customize the message templates using these placeholders:
   - `{name}` - Contact's name
   - `{phone}` - Contact's phone number
   - `{date}` - Current date (YYYY-MM-DD)
   - `{time}` - Current time (HH:MM)

## Configuration

Adjust the settings in [bulk_sender.py](file:///c%3A/Users/jnane/Documents/workspace/projects/whatsapp_bulk_sender/bulk_sender.py) according to your needs:

| Setting | Description | Default |
|---------|-------------|---------|
| `CSV_FILE` | Path to the contacts CSV file | `"contacts.csv"` |
| `RETRY_LIMIT` | Number of retry attempts for failed messages | `2` |
| `MIN_DELAY_SEC` | Minimum delay between messages (seconds) | `3` |
| `MAX_DELAY_SEC` | Maximum delay between messages (seconds) | `5` |
| `SESSION_DIR` | Directory to store WhatsApp session data | `"./whatsapp_session"` |
| `REPLY_KEYWORDS` | Keywords that trigger auto-replies | `{"help", "support", "urgent", "problem"}` |
| `AUTO_REPLY_MESSAGE` | Auto-reply message content | `"We'll contact you shortly! Our team is reviewing your request."` |
| `MONITOR_INTERVAL_SEC` | Interval for checking incoming messages | `30` |

## Usage

1. Run the script:
   ```bash
   python bulk_sender.py
   ```

2. Scan the QR code with your WhatsApp mobile app when prompted

3. The script will automatically:
   - Read contacts from your CSV file
   - Send personalized messages to each contact
   - Show progress in the console
   - Provide audio feedback for successful/failed deliveries

## How It Works

1. **Initialization**: The script initializes a headless Chrome browser with anti-detection measures
2. **Authentication**: You scan the WhatsApp Web QR code to log in
3. **Contact Loading**: Contacts are loaded from the CSV file with validation
4. **Message Sending**: For each contact:
   - Opens a new tab with the WhatsApp chat URL
   - Waits for the message input box to load
   - Sends the message using either Enter key or send button
   - Closes the tab and moves to the next contact
5. **Session Management**: Saves session data for future use

## Anti-Detection Measures

The script includes several measures to avoid detection as a bot:

- Disables automation indicators
- Suppresses browser logs
- Uses randomized delays between messages
- Mimics human-like behavior
- Maintains persistent sessions

## Error Handling

- **Network Issues**: Checks internet connectivity before starting
- **Failed Messages**: Retries failed messages up to the retry limit
- **Timeouts**: Handles page load and element wait timeouts
- **Invalid Numbers**: Skips invalid phone numbers with warnings
- **User Interruption**: Gracefully handles Ctrl+C interruption

## CSV File Format

Create a CSV file with the following structure:

```csv
Name,Phone,Message
John Doe,+1234567890,Hello {name}! Your account was created on {date}.
Jane Smith,+0987654321,Welcome {name}. Please contact us if you need help.
```

Notes:
- Phone numbers should include country codes
- Messages support template placeholders
- Invalid phone numbers will be skipped automatically

## Auto-Reply Feature

The script can monitor for keywords in incoming messages and respond automatically:

1. Keywords are defined in `REPLY_KEYWORDS`
2. Response message is set in `AUTO_REPLY_MESSAGE`
3. Checks for messages every `MONITOR_INTERVAL_SEC` seconds

## Troubleshooting

### Common Issues

1. **QR Code Not Showing**: 
   - Ensure you have a stable internet connection
   - Check that WhatsApp Web is not already open in another browser
   
2. **Messages Not Sending**:
   - Verify phone numbers are in the correct format
   - Check if you've been temporarily blocked by WhatsApp
   - Increase delay settings if sending too fast

3. **Chrome/ChromeDriver Issues**:
   - Ensure Chrome is updated to the latest version
   - Check that ChromeDriver is compatible with your Chrome version

### Logs and Debugging

The script provides detailed colored logging:
- 🟢 Green: Successful operations
- 🔵 Blue: Informational messages
- 🟡 Yellow: Warnings
- 🔴 Red: Errors
- 🟣 Magenta: Process start/progress

## Legal Disclaimer

This tool is for educational purposes only. Please ensure you comply with:
- WhatsApp's Terms of Service
- Local laws and regulations regarding messaging
- Privacy policies of your contacts
- Anti-spam legislation in your jurisdiction

The authors are not responsible for any misuse of this tool.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Selenium team for the excellent WebDriver library
- Inspired by various WhatsApp automation projects in the community