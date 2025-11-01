# BirdBoard - TouchDesigner Ambient Audio Control System

A TouchDesigner-based ambient audio playback system with web-based remote control interface. Designed for installations that require dynamic audio playback with day/night variations and special track triggers.

This application uses sound recordings from [myNoise.net](www.mynoise.net). I encourage you to purchase some credits and download a few of your favorite tracks. You can always add some of your own audio recordings just the same.

## Overview

BirdBoard plays ambient audio tracks with automatic day/night variations, featuring:
- **2 audio layers**: Nature sounds and atmospheric ambience
- **Individual volume control** for each layer plus global volume
- **Special playback modes**: Garden (special nature) and Duduk modes
- **Track triggers**: Play specific songs (Hotel California, Like a Virgin, Pretty Girl Rock)
- **Web-based control panel** accessible from any device on the network
- **System controls**: Remote reboot and shutdown capabilities

## System Architecture

```
Web Browser (any device)
    ↓ HTTP GET requests
TouchDesigner WebServer DAT (port 9980)
    ↓ Python callbacks
BirdBoard Audio System (TD operators)
```

### Key Components

1. **Web Interface** (`index.html`) - Browser-based control panel
2. **WebServer DAT** - TouchDesigner's built-in web server
3. **Callbacks** (`webserver_callbacks.py`) - Routes web requests to audio functions
4. **Audio Controller** (`ext_app_birdboard.py`) - Manages all audio playback
5. **Config** (`ext_birdboard_config.py`) - Network utilities for finding local IP
6. **Execute DAT** (`execute.py`) - Auto-launches web interface on TD startup

## File Structure

```
/project1/bird_board_micro/
├── comms/
│   ├── webserver1 (WebServer DAT)
│   ├── html_formatted (Text DAT with HTML content)
│   └── web_rx (Table DAT for logging received commands)
├── birdboard_audio/
│   ├── Hotel_California (Audio File In CHOP)
│   ├── Pretty_Girl_Rock (Audio File In CHOP)
│   ├── Like_A_Virgin (Audio File In CHOP)
│   ├── filein_ambi_day (Audio File In CHOP)
│   ├── filein_ambi_night (Audio File In CHOP)
│   ├── filein_nature_day (Audio File In CHOP)
│   ├── filein_nature_night (Audio File In CHOP)
│   ├── special (Constant CHOP)
│   ├── special_nature (Constant CHOP)
│   └── audio_par (Table DAT with filter parameters)
├── birdboard_ctrl/
│   └── volume (Table DAT with volume values)
├── birdboard_comms (Base COMP with ext_app_birdboard.py)
├── config (Base COMP with ext_birdboard_config.py)
└── triggers/ (Trigger CHOPs for each command)
```

## Setup Instructions

### 1. TouchDesigner Setup

1. Open your BirdBoard TouchDesigner project
2. Ensure the following components exist:
   - `/project1/bird_board_micro/comms/webserver1` (WebServer DAT)
   - `/project1/bird_board_micro/comms/html_formatted` (Text DAT)
   - `/project1/bird_board_micro/comms/web_rx` (Table DAT)
   - `/project1/bird_board_micro/birdboard_comms` (Base COMP)
   - `/project1/bird_board_micro/birdboard_ctrl` (Base COMP)
   - `/project1/bird_board_micro/birdboard_audio` (Base COMP)

### 2. Configure WebServer DAT

1. Select the `webserver1` DAT
2. Set parameters:
   - **Port**: `9980`
   - **Active**: `On`
   - **Callbacks DAT**: Point to the DAT with `webserver_callbacks.py`

### 3. Load HTML Content

1. Copy the contents of `index.html`
2. Paste into the `html_formatted` Text DAT

### 4. Load Python Scripts

**WebServer Callbacks:**
1. Create a new Text DAT for callbacks
2. Copy contents of `webserver_callbacks.py`
3. Link this DAT to the WebServer's Callbacks parameter

**Extension Classes:**
1. In `birdboard_comms` Base COMP → Extensions
   - Add `ext_app_birdboard.py` as extension
   - Class name: `app_birdboard`
   - Promote as: `birdboard_comms`

2. In `config` Base COMP → Extensions
   - Add `ext_birdboard_config.py` as extension
   - Class name: `BirdBoard`

**Execute DAT (Optional):**
1. Create an Execute DAT
2. Copy contents of `execute.py`
3. This will auto-open the web interface when TD starts

### 5. Verify Network Paths

Check that these paths in `webserver_callbacks.py` match your project:
- `HTML_DAT = 'html_formatted'` (relative path to HTML Text DAT)
- `RX_DAT = '/project1/bird_board_micro/comms/web_rx'` (absolute path to receive table)

## Usage

### Accessing the Control Panel

1. Start TouchDesigner project
2. Find your computer's local IP:
   - Run `op.config.GetAllIPAddresses()` in TD textport
   - OR check the `my_IPs` table in the config component
3. On any device on the same network, navigate to:
   ```
   http://[YOUR_IP]:9980
   ```
   Example: `http://192.168.1.100:9980`

### Control Panel Features

#### Volume Controls
- **BIRDS**: Controls nature sound layer volume (0.0 - 1.0)
- **AMBI**: Controls atmospheric ambience volume (0.0 - 1.0)
- **GLOBAL**: Master volume control for both layers (0.0 - 1.0)

#### Playback Modes
- **GARDEN**: Activates special nature mode
- **DUDUK**: Activates special duduk mode
- **NORMAL**: Returns to normal ambient playback
- **STOP**: Stops all special tracks

#### Track Selection
- **Hotel California**: Triggers playback of this specific song
- **Like a Virgin**: Triggers playback of this specific song
- **Pretty Girl Rock**: Triggers playback of this specific song

#### System Controls
- **REBOOT**: Restarts the computer (Windows only)
- **SHUT DOWN**: Shuts down the computer (Windows only)

#### Sync Mode
- **SYNC**: Enables sync mode (for future multi-device synchronization)
- **ASYNC**: Disables sync mode (direct control)

## Audio Playback Logic

### Ambient Audio
The system continuously plays two layers:
1. **Nature sounds**: Day/night variations via `filein_nature_day` and `filein_nature_night`
2. **Atmospheric ambience**: Day/night variations via `filein_ambi_day` and `filein_ambi_night`

[TODO: Document how day/night switching is triggered]

### Special Modes
- **Normal**: `special` and `special_nature` constants set to 0
- **Duduk**: `special` constant set to 1
- **Garden**: `special_nature` constant set to 1

[TODO: Document how these constants affect audio routing]

### Track Triggering
When a track button is pressed:
1. Audio File In CHOP `.par.play` is set to 1
2. `.par.cuepulse.pulse()` is triggered to start from cue point
3. Track plays over ambient audio

When STOP is pressed:
1. All track Audio File In CHOPs `.par.play` set to 0
2. All `.par.cuepulse.pulse()` triggered to reset to beginning

## Web Communication Protocol

### Request Format
All control commands use HTTP GET requests:
```
GET /set?topic=[COMMAND]&value=[VALUE]
```

### Available Commands

| Command | Value | Action |
|---------|-------|--------|
| `/vol_global` | 0.0-1.0 | Set global volume |
| `/vol_birds` | 0.0-1.0 | Set nature layer volume |
| `/vol_ambi` | 0.0-1.0 | Set ambience layer volume |
| `/special` | 1 | Activate duduk mode |
| `/special_nature` | 1 | Activate garden mode |
| `/normal` | 1 | Return to normal mode |
| `/stop` | 1 | Stop all special tracks |
| `/hotelcalifornia` | 1 | Play Hotel California |
| `/likeavirgin` | 1 | Play Like a Virgin |
| `/prettygirlrock` | 1 | Play Pretty Girl Rock |
| `/sync` | 1 | Enable sync mode |
| `/async` | 1 | Disable sync mode |
| `/reboot` | 1 | Reboot system |
| `/shutdown` | 1 | Shutdown system |

### Response Format
Success: `200 OK: [command]=[value]`
Error: `400 Missing topic or value`

## Debugging

### Enable Debug Output

The webserver callbacks include detailed logging. Look for these messages in the TouchDesigner textport:

```
==================================================
WEB | Method: GET
WEB | Path: /set
WEB | Parsed query: {'topic': ['/stop'], 'value': ['1']}
==================================================
WEB | /set endpoint hit!
WEB | Parsed topic: "/stop"
WEB | Parsed value: "1"
WEB | web_rx → /stop = 1
WEB | web_rx → Handling: /stop = 1
```

### Common Issues

**Web page not loading:**
- Check WebServer DAT is Active
- Verify port 9980 is not blocked by firewall
- Confirm `html_formatted` DAT contains HTML content

**Buttons not working:**
- Open browser console (F12) and check for JavaScript errors
- Verify fetch requests are being made in Network tab
- Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)

**Commands not executing:**
- Check that operator paths match your project structure
- Verify extension classes are properly loaded
- Look for Python errors in TD textport

**"Missing topic or value" error:**
- JavaScript may have syntax errors
- Check that fetch URL is properly formatted
- Verify query parameters are being sent

### Browser Console Debugging

In the web interface, open Developer Tools (F12) and check the Console tab:
```
✅ Page loaded and ready!
🖱️ Button clicked: STOP
📤 Sending: /stop = 1
📤 URL: /set?topic=%2Fstop&value=1
📥 Response status: 200
📥 Response data: OK: /stop=1
```

## Network Configuration

### Firewall Rules
Ensure port 9980 is allowed through the firewall:

**Windows:**
```powershell
netsh advfirewall firewall add rule name="TouchDesigner WebServer" dir=in action=allow protocol=TCP localport=9980
```

**macOS:**
```bash
# System Preferences → Security & Privacy → Firewall → Firewall Options
# Add TouchDesigner to allowed applications
```

### Multiple Devices
Any device on the same local network can access the control panel:
- Tablets
- Smartphones  
- Other computers
- Touch panel controllers

Simply navigate to `http://[TOUCHDESIGNER_IP]:9980` from any browser.

## Customization

### Adding New Commands

1. **Add HTML control** in `index.html`:
   ```html
   <button type="button" class="btn" data-topic="/newcommand" data-val="1">New Command</button>
   ```

2. **Add handler** in `webserver_callbacks.py` → `_handle_command()`:
   ```python
   elif topic == '/newcommand':
       op.birdboard_comms.NewFunction()
   ```

3. **Add function** in `ext_app_birdboard.py`:
   ```python
   def NewFunction(self):
       print('NEW COMMAND EXECUTED')
       # Your audio control code here
       return
   ```

### Styling the Web Interface

Modify the `<style>` section in `index.html`:
```css
body { background: #your-color; }
.btn { background: #your-button-color; }
```

## System Requirements

- **TouchDesigner** 2022.20000+ (tested version)
- **Python** 3.9+ (included with TouchDesigner)
- **Network**: Local network access for remote control
- **OS**: Windows 10/11, macOS 10.15+

## Troubleshooting

### WebServer DAT won't start
- Check if another application is using port 9980
- Try changing to a different port (update both WebServer DAT and `execute.py`)

### Audio not playing
[TODO: Add audio troubleshooting steps specific to your audio routing setup]

### Reboot/Shutdown not working
- These commands only work on Windows
- Requires administrator privileges
- For macOS, update commands in `ext_app_birdboard.py`:
  ```python
  os.system("sudo shutdown -r now")  # Reboot
  os.system("sudo shutdown -h now")  # Shutdown
  ```

## Architecture Notes

### Why WebServer DAT Instead of Node.js?

The previous version used Node.js with Express and node-osc. This new version uses TouchDesigner's built-in WebServer DAT because:

1. **No external dependencies**: Everything runs within TouchDesigner
2. **Simpler deployment**: No need to install Node.js on playback machines
3. **Direct integration**: Python callbacks directly control TD operators
4. **Easier maintenance**: One less system to manage

### Communication Flow

```
Browser → HTTP GET → WebServer DAT → Python Callback → Extension Class → TD Operators
```

No OSC layer is needed since everything runs in the same TD process.

## Future Enhancements

- [ ] Add authentication for system controls
- [ ] Implement true sync mode for multi-device installations
- [ ] Add day/night automatic switching logic
- [ ] Create preset system for different scenes/modes
- [ ] Add audio level monitoring visualization
- [ ] Mobile-optimized responsive design
- [ ] Save/load volume presets
- [ ] Add fade in/out transitions between modes

## License

[TODO: Add your license information]

## Credits

[TODO: Add credits/attribution]

## Version History

### v2.0 (Current)
- Switched from Node.js/OSC to WebServer DAT
- Simplified architecture
- Fixed JavaScript template literal bugs
- Added comprehensive debugging

### v1.0 (Legacy)
- Node.js + Express + node-osc
- OSC communication between Node and TD
- Multiple OSC receiver ports

---

**Note**: This documentation is a work in progress. Sections marked with [TODO] need additional project-specific information that only you can provide based on your actual TouchDesigner network setup.
