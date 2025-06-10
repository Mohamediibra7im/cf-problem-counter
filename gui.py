from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QSpinBox,
    QDialog,
    QVBoxLayout as QVBoxLayoutDialog,
    QTableWidget as QTableWidgetDialog,
)
from PyQt5.QtCore import Qt, QDateTime
from typing import Dict
import json
import csv
from datetime import datetime
from api import MIN_RATING, MAX_RATING, RATING_STEP, clear_cache


class MainWindow(QMainWindow):
    def __init__(self, fetch_results_callback):
        super().__init__()
        self.fetch_results_callback = fetch_results_callback
        self.year_rating_counts = {}
        self.setWindowTitle("Codeforces Problem Rating Counter")
        self.setMinimumSize(800, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        input_layout = QHBoxLayout()
        self.handle_label = QLabel("Codeforces Handle:")
        self.handle_input = QLineEdit()
        self.handle_input.setPlaceholderText("Enter your handle")
        self.fetch_button = QPushButton("Fetch Results")
        self.fetch_button.clicked.connect(self.fetch_results)
        input_layout.addWidget(self.handle_label)
        input_layout.addWidget(self.handle_input)
        input_layout.addWidget(self.fetch_button)
        self.layout.addLayout(input_layout)

        filter_layout = QHBoxLayout()
        self.min_year = QSpinBox()
        self.min_year.setRange(2000, 2025)
        self.min_year.setValue(2000)
        self.max_year = QSpinBox()
        self.max_year.setRange(2000, 2025)
        self.max_year.setValue(2025)
        self.min_rating = QSpinBox()
        self.min_rating.setRange(MIN_RATING, MAX_RATING)
        self.min_rating.setValue(MIN_RATING)
        self.min_rating.setSingleStep(RATING_STEP)
        self.max_rating = QSpinBox()
        self.max_rating.setRange(MIN_RATING, MAX_RATING)
        self.max_rating.setValue(MAX_RATING)
        self.max_rating.setSingleStep(RATING_STEP)
        filter_layout.addWidget(QLabel("Year Range:"))
        filter_layout.addWidget(self.min_year)
        filter_layout.addWidget(QLabel("to"))
        filter_layout.addWidget(self.max_year)
        filter_layout.addWidget(QLabel("Rating Range:"))
        filter_layout.addWidget(self.min_rating)
        filter_layout.addWidget(QLabel("to"))
        filter_layout.addWidget(self.max_rating)
        self.layout.addLayout(filter_layout)

        action_layout = QHBoxLayout()
        self.export_json_button = QPushButton("Export to JSON")
        self.export_json_button.clicked.connect(self.export_to_json)
        self.export_csv_button = QPushButton("Export to CSV")
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.view_progress_button = QPushButton("View Progress")
        self.view_progress_button.clicked.connect(self.view_progress)
        self.refresh_api_button = QPushButton("Refresh API")
        self.refresh_api_button.clicked.connect(self.refresh_api)
        action_layout.addWidget(self.export_json_button)
        action_layout.addWidget(self.export_csv_button)
        action_layout.addWidget(self.view_progress_button)
        action_layout.addWidget(self.refresh_api_button)
        self.layout.addLayout(action_layout)

        self.total_label = QLabel("Total Problems Solved: 0")
        self.layout.addWidget(self.total_label)

        self.status_label = QLabel("Ready to fetch results")
        self.layout.addWidget(self.status_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def fetch_results(self):
        handle = self.handle_input.text().strip()
        if not handle:
            self.status_label.setText("Error: Please enter a valid handle")
            return

        if self.min_year.value() > self.max_year.value():
            self.status_label.setText("Error: Min year cannot be greater than max year")
            return
        if self.min_rating.value() > self.max_rating.value():
            self.status_label.setText(
                "Error: Min rating cannot be greater than max rating"
            )
            return

        self.status_label.setText("Fetching results...")
        self.fetch_button.setEnabled(False)
        self.year_rating_counts = self.fetch_results_callback(
            handle,
            self.min_year.value(),
            self.max_year.value(),
            self.min_rating.value(),
            self.max_rating.value(),
        )

        if self.year_rating_counts is None:
            self.status_label.setText(
                "Error: Failed to fetch data. Check handle or network."
            )
            self.fetch_button.setEnabled(True)
            return

        self.save_progress()
        self.display_results(self.year_rating_counts)
        self.status_label.setText("✓ Results loaded successfully")
        self.fetch_button.setEnabled(True)

    def display_results(self, year_rating_counts: Dict[int, Dict[int, int]]):
        """Populate the table with results."""
        years = sorted(year_rating_counts.keys())
        if not years:
            self.status_label.setText("No solved problems found in the rating range.")
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.total_label.setText("Total Problems Solved: 0")
            return

        # Calculate columns: ratings + 'Year' column
        ratings = list(
            range(self.min_rating.value(), self.max_rating.value() + 1, RATING_STEP)
        )
        self.table.setColumnCount(len(ratings) + 1)
        self.table.setHorizontalHeaderLabels(
            ["Year"] + [str(rating) for rating in ratings]
        )

        # Rows: one per year + one for totals
        self.table.setRowCount(len(years) + 1)

        # Populate data
        total_solved_all = {rating: 0 for rating in ratings}
        for row, year in enumerate(years):
            self.table.setItem(row, 0, QTableWidgetItem(str(year)))
            for col, rating in enumerate(ratings, 1):
                count = year_rating_counts[year][rating]
                total_solved_all[rating] += count
                item = QTableWidgetItem(str(count))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

        # Total row
        self.table.setItem(len(years), 0, QTableWidgetItem("Total"))
        for col, rating in enumerate(ratings, 1):
            item = QTableWidgetItem(str(total_solved_all[rating]))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(len(years), col, item)

        # Calculate total problems
        total_problems = sum(
            sum(counts.values()) for counts in year_rating_counts.values()
        )
        self.total_label.setText(f"Total Problems Solved: {total_problems}")

        # Adjust table appearance
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)

    def export_to_json(self):
        """Export results to a JSON file in the current directory as 'results.json'."""
        if not self.year_rating_counts:
            self.status_label.setText("Error: No results to export")
            return

        filename = "results.json"
        try:
            with open(filename, "w") as f:
                json.dump(self.year_rating_counts, f, indent=2)
            self.status_label.setText(f"✓ Exported to {filename}")
        except Exception as e:
            self.status_label.setText(f"Error exporting JSON: {e}")

    def export_to_csv(self):
        """Export results to a CSV file in the current directory as 'results.csv'."""
        if not self.year_rating_counts:
            self.status_label.setText("Error: No results to export")
            return

        filename = "results.csv"
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Year"]
                    + [
                        str(r)
                        for r in range(
                            self.min_rating.value(),
                            self.max_rating.value() + 1,
                            RATING_STEP,
                        )
                    ]
                )
                for year, ratings in sorted(self.year_rating_counts.items()):
                    writer.writerow(
                        [year]
                        + [
                            ratings.get(r, 0)
                            for r in range(
                                self.min_rating.value(),
                                self.max_rating.value() + 1,
                                RATING_STEP,
                            )
                        ]
                    )
            self.status_label.setText(f"✓ Exported to {filename}")
        except Exception as e:
            self.status_label.setText(f"Error exporting CSV: {e}")

    def clear_cache(self):
        clear_cache()
        self.status_label.setText("✓ Cache file deleted")

    def save_progress(self):
        try:
            try:
                with open("progress.json", "r") as f:
                    progress_data = json.load(f)
            except FileNotFoundError:
                progress_data = []

            timestamp = QDateTime.currentDateTime().toString(Qt.ISODate)
            progress_entry = {
                "timestamp": timestamp,
                "year_rating_counts": self.year_rating_counts,
            }
            progress_data.append(progress_entry)

            with open("progress.json", "w") as f:
                json.dump(progress_data, f, indent=2)
        except Exception as e:
            self.status_label.setText(f"Error saving progress: {e}")

    def view_progress(self):
        try:
            with open("progress.json", "r") as f:
                progress_data = json.load(f)
        except FileNotFoundError:
            self.status_label.setText("Error: No progress data available")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Progress History")
        dialog_layout = QVBoxLayoutDialog(dialog)

        progress_table = QTableWidgetDialog()
        progress_table.setColumnCount(3)
        progress_table.setHorizontalHeaderLabels(
            ["Timestamp", "Total Problems", "Change"]
        )

        totals = []
        for entry in progress_data:
            total = sum(
                sum(counts.values()) for counts in entry["year_rating_counts"].values()
            )
            totals.append(total)
        
        progress_table.setRowCount(len(progress_data))
        for row, (entry, total) in enumerate(zip(progress_data, totals)):
            timestamp_item = QTableWidgetItem(entry["timestamp"])
            total_item = QTableWidgetItem(str(total))
            change_item = QTableWidgetItem(
                str(total - (totals[row - 1] if row > 0 else 0))
            )
            for item in (timestamp_item, total_item, change_item):
                item.setTextAlignment(Qt.AlignCenter)
            progress_table.setItem(row, 0, timestamp_item)
            progress_table.setItem(row, 1, total_item)
            progress_table.setItem(row, 2, change_item)

        progress_table.resizeColumnsToContents()
        dialog_layout.addWidget(progress_table)
        dialog.exec_()

        self.status_label.setText("✓ Progress viewed")

    def refresh_api(self):
        handle = self.handle_input.text().strip()
        if not handle:
            self.status_label.setText("Error: Please enter a valid handle")
            return

        if self.min_year.value() > self.max_year.value():
            self.status_label.setText("Error: Min year cannot be greater than max year")
            return
        if self.min_rating.value() > self.max_rating.value():
            self.status_label.setText(
                "Error: Min rating cannot be greater than max rating"
            )
            return

        self.status_label.setText("Refreshing API data...")
        self.refresh_api_button.setEnabled(False)
        clear_cache()
        self.year_rating_counts = self.fetch_results_callback(
            handle,
            self.min_year.value(),
            self.max_year.value(),
            self.min_rating.value(),
            self.max_rating.value(),
        )

        if self.year_rating_counts is None:
            self.status_label.setText(
                "Error: Failed to fetch data. Check handle or network."
            )
            self.refresh_api_button.setEnabled(True)
            return

        self.save_progress()
        self.display_results(self.year_rating_counts)
        self.status_label.setText("✓ API data refreshed successfully")
        self.refresh_api_button.setEnabled(True)
