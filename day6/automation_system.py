import csv
import os
import json
import logging
import shutil
from datetime import datetime
import sys

# -------- load config ---------
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

INPUT_FOLDER = config["input_folder"]
OUTPUT_FOLDER = config["output_folder"]
REPORT_FOLDER = config["report_folder"]
LOG_FOLDER = config["log_folder"]
ACCEPTED = config["accepted_result"]
PROCESSED_FOLDER = config["processed_folder"]
BAD_FOLDER = config["bad_folder"]

os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(BAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# --------- setup logging -----------
log_file = os.path.join(
    LOG_FOLDER, f"automation_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("SYSTEM STARTED")

# --------- system status ----------
system_failed = False
bad_files = []

# ------------- scan input ----------------
try:
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".csv")]
    logging.info(f"Found {len(files)} csv files")
except Exception as e:
    logging.critical("Cannot access input folder")
    logging.critical(str(e))
    sys.exit(1)

summary = []
grand_total = 0
grand_pass = 0
grand_fail = 0

# ----------- batch processing -------------
for file_name in files:
    logging.info(f"Processing file: {file_name}")

    input_path = os.path.join(INPUT_FOLDER, file_name)
    output_path = os.path.join(OUTPUT_FOLDER, "processed_" + file_name)

    total = pass_count = fail_count = 0
    results = []
    file_has_error = False

    try:
        with open(input_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) < 2:
                    logging.warning(f"Bad row format in {file_name}")
                    file_has_error = True
                    continue

                result = row[1].strip().lower()

                if result not in ACCEPTED:
                    logging.warning(f"Unknown result '{row[1]}' in {file_name}")
                    file_has_error = True
                    continue

                total += 1
                if result == "pass":
                    pass_count += 1
                else:
                    fail_count += 1

                results.append(row)

    except Exception as e:
        logging.error(f"Failed to read file {file_name}")
        logging.error(str(e))
        shutil.move(input_path, os.path.join(BAD_FOLDER, file_name))
        bad_files.append(file_name)
        system_failed = True
        continue

    # -------- write output --------
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Test Name", "Result"])
        writer.writerows(results)

    # -------- file lifecycle --------
    if file_has_error:
        shutil.move(input_path, os.path.join(BAD_FOLDER, file_name))
        bad_files.append(file_name)
        system_failed = True
    else:
        shutil.move(input_path, os.path.join(PROCESSED_FOLDER, file_name))

    summary.append([file_name, total, pass_count, fail_count])

    grand_total += total
    grand_pass += pass_count
    grand_fail += fail_count

# -------------- master report ----------------
report_name = f"master_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
report_path = os.path.join(REPORT_FOLDER, report_name)

with open(report_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["File", "Total", "Pass", "Fail"])
    writer.writerows(summary)
    writer.writerow([])
    writer.writerow(["ALL", grand_total, grand_pass, grand_fail])

# -------------- execution summary ----------------
run_summary = f"""
SYSTEM RUN SUMMARY
-----------------------
Total files : {len(files)}
Total tests : {grand_total}
Pass        : {grand_pass}
Fail        : {grand_fail}
Bad files   : {bad_files}
Status      : {"FAILED" if system_failed else "SUCCESS"}
Time        : {datetime.now()}
"""

with open(os.path.join(REPORT_FOLDER, "run_summary.txt"), "w", encoding="utf-8") as f:
    f.write(run_summary)

# -------------- system ending ----------------
if system_failed:
    logging.critical("SYSTEM FINISHED WITH ERRORS")
    logging.critical(f"Bad files: {bad_files}")
    logging.info(f"TOTAL={grand_total} Pass={grand_pass} Fail={grand_fail}")
    logging.info(f"Report: {report_path}")
    sys.exit(1)
else:
    logging.info("SYSTEM FINISHED SUCCESSFULLY")
    logging.info(f"TOTAL={grand_total} Pass={grand_pass} Fail={grand_fail}")
    logging.info(f"Report: {report_path}")
    sys.exit(0)