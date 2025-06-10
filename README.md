# Codeforces Problem Rating Counter 📊🚀

A sleek Python desktop application built with PyQt5 to track and analyze problems solved on Codeforces, categorized by rating (800–3500) and year. Perfect for competitive programmers looking to monitor their progress! 🎯💻

## ✨ Features

- **Display Results**: View a table of solved problems per rating and year, with a total row. 📈
- **Total Problems**: See your overall solved problem count at a glance. 🔢
- **JSON/CSV Export**: Export your data for offline analysis. 📥
- **Filtering**: Customize results by year and rating ranges. 🔍
- **Caching**: Speed up fetches with local API response caching. ⚡
- **Progress Tracking**: Record and review your solving history with timestamps. ⏳
- **Refresh API**: Fetch the latest data by clearing the cache. 🔄
- **Clear Cache**: Delete the cache file for a fresh start. 🗑️

## 🛠️ Setup

1. **Install Python**: Ensure Python 3.6+ is installed on your system. 🐍
2. **Install Dependencies**: Run the following command to install required libraries:
   ```
   pip install -r requirements.txt
   ```
   This includes `requests`, `PyQt5`, and `requests_cache`. 📦
3. **Directory Structure**: Organize your project files as follows:
   ```
   cf-problem-counter/
   ├── api.py
   ├── processor.py
   ├── gui.py
   ├── main.py
   ├── README.md
   └── requirements.txt
   ```

## 🚀 Usage

1. Navigate to the project root directory:
   ```
   cd codeforces_problem_counter
   ```
2. Launch the application:
   ```
   python main.py
   ```
3. Explore the GUI:
   - Enter your Codeforces handle (e.g., “tourist”). 👤
   - Adjust year (2000–2025) and rating (800–3500) filters. 🎚️
   - Click **Fetch Results** to load data. 🔍
   - Check the table for results and the **Total Problems Solved** label. 📊
   - Export data with **Export to JSON** or **Export to CSV**. 💾
   - Track progress with **View Progress**. 📅
   - Refresh data with **Refresh API** or clear the cache with **Clear Cache**. 🔄🗑️

## 📋 Example Table

| Year  | 800 | 900 | 1000 | ... | 3500 |
|-------|-----|-----|------|-----|------|
| 2023  | 5   | 3   | 2    | ... | 0    |
| 2024  | 4   | 6   | 1    | ... | 1    |
| Total | 9   | 9   | 3    | ... | 1    |

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 📜

