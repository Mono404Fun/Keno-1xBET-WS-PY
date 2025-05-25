# 🔮 Keno AI: Advanced 1xBet Keno Number Analyzer  

![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)  ![Selenium](https://img.shields.io/badge/selenium-4.0+-green?logo=selenium)  ![License](https://img.shields.io/badge/license-MIT-orange)  ![Maintenance](https://img.shields.io/badge/maintenance-active-brightgreen)  

An intelligent web scraper and statistical analyzer for identifying number patterns in 1xBet/TVBet Keno games.  

⚠️ **Disclaimer**: This tool provides statistical insights only. Keno outcomes are random - no winning guarantees. Use at your own risk.  

## 🌟 Core Features

### 🕸️ Web Automation
- **Headless browser** scraping with anti-detection
- Automatic round simulation (50+ rounds/minute)
- Dynamic element waiting with smart timeouts

### 📊 Statistical Analysis
- **Hot/Cold numbers** tracking
- **Combination frequency** (pairs/triplets)
- Odd/Even & High/Low distribution
- Historical trend visualization

### 💾 Data Management
- SQLite database storage
- CSV export/import capability
- Automated data backup system

### 🖥️ User Experience
- Interactive CLI with `rich` formatting
- Progress tracking during operations
- Error handling with recovery modes

  ## 🛠️ Installation Guide

### Prerequisites
- [Python 3.9+](https://www.python.org/downloads/)
- [Chrome Browser](https://www.google.com/chrome/)
- ChromeDriver ([Download](https://chromedriver.chromium.org/downloads))

## Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/keno-ai.git
   cd keno-ai
   ```

2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
```

3. Install Dependencies
```bash
pip install -r requirements.txt
source venv/bin/activate
```

4. Configure ChromeDriver

1. Check Chrome version at `chrome://settings/help`
2. Download matching driver from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads)
3. Choose one method:

**Method A**: Project root
```bash
mv chromedriver /project/root/folder/
```

**Method B**: System PATH
```bash
sudo mv chromedriver /usr/local/bin/
```

**Method C**: Custom path (edit config.ini)
```ini
[selenium]
chromedriver_path = C:\path\to\chromedriver.exe
```

5. Verify Installation

```bash
# Test Selenium
python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit()"

# Test dependencies
python -c "import pandas as pd; print('Pandas version:', pd.__version__)"
```

### Expected output:
```text
DevTools listening on ws://127.0.0.1:.../
Pandas version: 2.1.0
```

## Interactive Menu:
```text
⚡ Advanced Keno Number Analyzer ⚡

? Select operation:
  🎲 Scrape New Rounds
  📊 Analyze Frequency
  🔄 Analyze Combinations
  📈 Generate Frequency Plot
  🚪 Exit
```


---

## 📊 Sample Output

![Frequency Analysis](https://i.imgur.com/JQ8W5xO.png)

```text
🔥 Hot Numbers (Most Frequent)
┏━━━━━━━━┳━━━━━━━━━━━┓
┃ Number ┃ Frequency ┃
┡━━━━━━━━╇━━━━━━━━━━━┩
│ 42     │ 87        │
│ 17     │ 83        │
│ 64     │ 80        │
└────────┴───────────┘
```


---

## 🛠️ Configuration

Edit `config.ini` (create if missing):
```ini
[settings]
headless = true
rounds_to_scrape = 50
database_path = keno_data.db
```


---

## 🤖 Technical Stack

- **Web Automation**: Selenium + Undetected ChromeDriver
- **Data Analysis**: Pandas + Matplotlib
- **CLI Interface**: Rich + Questionary
- **Database**: SQLite3

## ⚠️ Legal Disclaimer

This project is for **educational purposes only**. Gambling involves risk. Please:
- Check local laws before using
- Never gamble with money you can't afford to lose
- Use at your own risk

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.
