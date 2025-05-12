
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", 20)
APP_ENV = os.environ.get("APP_ENV", "development")
AUTO_RELOAD = os.environ.get("AUTO_RELOAD", "True")

DASHBOARD_PAGES = {
    "about_daniel_belay.py": [
        "000_one_off_projects.py",
    ],
    "000_one_off_projects.py": [
        "m4a_to_mp3_encoding_mismatch.py",
    ],
}

print(f"Loaded configuration with APP_ENV={APP_ENV} and AUTO_RELOAD={AUTO_RELOAD}")
