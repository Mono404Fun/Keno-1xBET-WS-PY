import time
import sqlite3
import pandas as pd
from collections import defaultdict, Counter
from itertools import combinations
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pyfiglet
import questionary
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
import matplotlib.pyplot as plt

# ======================
# ENHANCED CLI INTERFACE
# ======================
console = Console()
WARNING_COLOR = "bold red"
SUCCESS_COLOR = "bold green"
INFO_COLOR = "bold blue"

def display_banner():
    banner = pyfiglet.figlet_format("KENO AI", font="slant")
    console.print(Panel.fit(banner, style="bold magenta"))
    console.print("⚡ [bold cyan]Advanced Keno Number Analyzer[/] ⚡\n")

# ======================
# DATA STORAGE (SQLITE)
# ======================
def init_database():
    db_path = Path("keno_data.db")
    if not db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keno_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                numbers TEXT,
                round_type TEXT
            )
        ''')
        conn.commit()
        conn.close()
        console.print("✅ [green]Database initialized successfully![/]")
    return db_path

# ======================
# WEB AUTOMATION ENGINE
# ======================
class KenoScraper:
    def __init__(self, headless=True):
        self.driver = None
        self.url = "https://tvbetframe29.com/?lng=FR&token=5a7db4ce-09f2-45c4-8a05-00d370655f26&clientId=5753&tagId=10&singleGame=9#/game/9/"
        self.headless = headless
        self.setup_driver()

    def setup_driver(self):
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(executable_path="chromedriver.exe")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_window_position(-10000, 0)
        except Exception as e:
            console.print(f"❌ [red]Driver setup failed: {e}[/]")
            raise

    def scrape_rounds(self, num_rounds=50):
        console.print(f"\n🔮 [yellow]Scraping {num_rounds} rounds...[/]")
        results = []
        
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-game-variation__text'))
            
            for _ in track(range(num_rounds), description="Processing..."):
                try:
                    self.driver.find_element(By.CLASS_NAME, 'btn-game-variation__text').click()
                    time.sleep(1.5)  # Reduced from 2s for faster scraping
                    
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    numbers = [n.get_text() for n in soup.find_all('div', class_='game-cell--has-selected')]
                    
                    if numbers:
                        results.append(numbers)
                        self.save_to_db(numbers, "auto")
                        console.print(f"🌀 Round {_+1}: [cyan]{numbers}[/]")
                    else:
                        console.print(f"⚠️ [yellow]Empty round detected (retrying...)[/]")
                        continue
                        
                except Exception as e:
                    console.print(f"⚠️ [yellow]Round error: {str(e)}[/]")
                    continue
            
            return results
            
        except Exception as e:
            console.print(f"❌ [red]Scraping failed: {str(e)}[/]")
            return None

    def save_to_db(self, numbers, round_type):
        conn = sqlite3.connect("keno_data.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO keno_results (timestamp, numbers, round_type) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), ",".join(numbers), round_type)
        )
        conn.commit()
        conn.close()

# ======================
# ADVANCED ANALYTICS
# ======================
class KenoAnalyzer:
    def __init__(self):
        self.db_path = "keno_data.db"
        self.console = Console()

    def get_all_numbers(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT numbers FROM keno_results", conn)
        conn.close()
        return [num for sublist in df['numbers'].str.split(',') for num in sublist]

    def frequency_analysis(self):
        numbers = self.get_all_numbers()
        freq = Counter(numbers)
        
        table = Table(title="🔥 Hot Numbers (Most Frequent)")
        table.add_column("Number", style="cyan")
        table.add_column("Frequency", style="magenta")
        
        for num, count in freq.most_common(10):
            table.add_row(num, str(count))
        
        self.console.print(table)
        return freq

    def combination_analysis(self, combo_size=2):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT numbers FROM keno_results", conn)
        conn.close()
        
        combo_counter = defaultdict(int)
        for numbers in df['numbers'].str.split(','):
            for combo in combinations(numbers, combo_size):
                combo_counter[tuple(sorted(combo))] += 1
                
        top_combos = sorted(combo_counter.items(), key=lambda x: x[1], reverse=True)[:5]
        
        table = Table(title=f"🤝 Top {combo_size}-Number Combinations")
        table.add_column("Numbers", style="cyan")
        table.add_column("Occurrences", style="green")
        
        for combo, count in top_combos:
            table.add_row(" + ".join(combo), str(count))
        
        self.console.print(table)
        return top_combos

    def plot_frequency(self):
        numbers = self.get_all_numbers()
        freq = Counter(numbers)
        
        plt.figure(figsize=(12, 6))
        freq.most_common(20)[::-1].plot(kind='barh')
        plt.title("Top 20 Most Frequent Numbers")
        plt.xlabel("Frequency")
        plt.tight_layout()
        plt.savefig("frequency_plot.png")
        self.console.print(f"📊 [green]Frequency plot saved as frequency_plot.png[/]")

# ======================
# MAIN APPLICATION FLOW
# ======================
def main():
    display_banner()
    init_database()
    
    scraper = KenoScraper(headless=True)
    analyzer = KenoAnalyzer()
    
    while True:
        choice = questionary.select(
            "Select operation:",
            choices=[
                "🎲 Scrape New Rounds",
                "📊 Analyze Frequency",
                "🔄 Analyze Combinations",
                "📈 Generate Frequency Plot",
                "🚪 Exit"
            ]).ask()
        
        if choice == "🎲 Scrape New Rounds":
            rounds = questionary.text("How many rounds to scrape?", default="50").ask()
            scraper.scrape_rounds(int(rounds))
            
        elif choice == "📊 Analyze Frequency":
            analyzer.frequency_analysis()
            
        elif choice == "🔄 Analyze Combinations":
            analyzer.combination_analysis(combo_size=2)
            
        elif choice == "📈 Generate Frequency Plot":
            analyzer.plot_frequency()
            console.print("✅ [green]Plot generated successfully![/]")
            
        elif choice == "🚪 Exit":
            console.print("\n✨ [bold magenta]Good luck with your Keno games![/] ✨")
            if scraper.driver:
                scraper.driver.quit()
            break

if __name__ == "__main__":
    main()
