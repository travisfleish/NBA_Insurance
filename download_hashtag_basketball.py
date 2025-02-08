from playwright.sync_api import sync_playwright
import pandas as pd
import datetime
import os
import time

# URL for the NBA Transactions search page
BASE_URL = "https://prosportstransactions.com/basketball/Search/Search.php"

# Set the start date to 04/16/2023 (Day after last Kaggle data) and today's date as end date
start_date = "2023-04-16"
end_date = datetime.datetime.today().strftime("%Y-%m-%d")

# File paths for saving progress
DATA_FILE = "data/injury_data/nba_injuries_2023_present.csv"
CHECKPOINT_FILE = "data/nba_injuries_checkpoint.csv"

def load_existing_data():
    """Loads existing data if script was interrupted."""
    if os.path.exists(CHECKPOINT_FILE):
        print("🔄 Resuming from last checkpoint...")
        return pd.read_csv(CHECKPOINT_FILE).values.tolist()
    return []

def scrape_nba_injuries():
    """Scrapes NBA injury data from 04/16/2023 to the present using Playwright (Visible Mode)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Open browser visibly
        page = browser.new_page()
        page.goto(BASE_URL)

        # ✅ Step 1: Fill in the search form
        print(f"🔎 Searching for NBA injuries from {start_date} to {end_date}...")
        page.fill('input[name="BeginDate"]', start_date)  # Start date (after Kaggle dataset)
        page.fill('input[name="EndDate"]', end_date)  # End date (today)

        # ✅ Step 2: Uncheck default "Player/Coach/Executive Movement" box
        page.uncheck('input[name="PlayerMovementChkBx"]')

        # ✅ Step 3: Check ONLY the relevant injury options
        page.check('input[name="InjuriesChkBx"]')  # ✅ Check "Missed games due to injury"
        page.check('input[name="ILChkBx"]')  # ✅ Check "Movement to/from injured/inactive list (IL)"

        # ✅ Step 4: Submit the form
        page.click('input[type="submit"]')  # Click Search Button
        page.wait_for_timeout(5000)  # Wait for results to load

        all_data = load_existing_data()
        page_num = len(all_data) // 50 + 1  # Resume from last saved page

        while True:
            print(f"🔎 Scraping page {page_num}...")

            # ✅ Step 5: Extract the injury table
            rows = page.locator('table.datatable tr').all()
            for row in rows[1:]:  # Skip header row
                cols = row.locator('td').all()
                if len(cols) < 5:  # Ensure all columns exist
                    continue  # Skip malformed rows

                date = cols[0].inner_text().strip()
                team = cols[1].inner_text().strip()
                acquired = cols[2].inner_text().strip()  # ✅ Extract "Acquired"
                relinquished = cols[3].inner_text().strip()  # ✅ Extract "Relinquished"
                notes = cols[4].inner_text().strip()  # ✅ Extract "Notes"

                all_data.append([date, team, acquired, relinquished, notes])

            # ✅ Step 6: Save Progress After Every Page
            df = pd.DataFrame(all_data, columns=["Date", "Team", "Acquired", "Relinquished", "Notes"])
            df.to_csv(CHECKPOINT_FILE, index=False)
            print(f"💾 Saved progress at page {page_num} ({len(df)} records)")

            # ✅ Step 7: Click "Next Page" if available
            next_button = page.locator('a:text("Next")')
            if next_button.count() == 0:  # Stop if no next page
                break

            try:
                with page.expect_navigation(timeout=60000):  # ✅ Wait for full navigation
                    next_button.click()
                print(f"➡️ Navigated to page {page_num + 1}")
            except:
                print(f"⚠️ Timeout on page {page_num}, retrying...")
                continue  # If it fails, try again

            page.wait_for_timeout(5000)  # Give extra time for loading
            page_num += 1

        # ✅ Step 8: Final Save Once Scraping is Complete
        df.to_csv(DATA_FILE, index=False)
        print(f"✅ Scraped {len(df)} injury records and saved to {DATA_FILE}!")

        # ✅ Delete the checkpoint file (since we're done)
        os.remove(CHECKPOINT_FILE)
        browser.close()

if __name__ == "__main__":
    scrape_nba_injuries()
