import sys
import os

sys.path.append(os.path.dirname(__file__))  # Add project root to path
from api import fetch_user_submissions, RATING_STEP
from processor import process_submissions
from gui import MainWindow
from PyQt5.QtWidgets import QApplication


def fetch_results(handle, min_year, max_year, min_rating, max_rating):
    submissions = fetch_user_submissions(handle)
    if submissions is None:
        return None
    return process_submissions( submissions, min_rating, max_rating, RATING_STEP, min_year, max_year)


def main():
    app = QApplication(sys.argv)
    window = MainWindow(fetch_results)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
