import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", 20)
APP_ENV = os.environ.get("APP_ENV", "development")
AUTO_RELOAD = os.environ.get("AUTO_RELOAD", "True")
MS_NAME = os.environ.get("MS_NAME", "dbs_db")

NAV_STRUCTURE = {
    "One-off Projects": {
        "pages": [
            {"title": "m4a to mp3 encoding mismatch", "path": "pages/001_m4a_to_mp3_encoding_mismatch.py"},
            {"title": "letterboxd data", "path": "pages/002_letterboxd_data.py"},
        ]
    }
}
# print(f"test APP_ENV={APP_ENV} and reload={AUTO_RELOAD}")
