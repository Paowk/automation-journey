import csv
import os
from datetime import datetime

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
REPORT_FOLDER = "report"

summary = []
grand_total = 0
grand_pass = 0
grand_fail = 0

files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".csv")]

print("FOUND FILE:",files)

for file_name in files:
    input_path = os.path.join(INPUT_FOLDER, file_name)
    output_path = os.path.join(OUTPUT_FOLDER, "process_" + file_name)

    total = 0
    pass_count = 0
    fail_count = 0
    results = []

    with open(input_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            total += 1
            if row[1].lower() == "pass":
                pass_count += 1
            else:
                fail_count += 1
            results.append(row)
        
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Test Name","Result"])
        writer.writerows(results)

    summary.append([file_name, total, pass_count, fail_count])

    grand_total += total
    grand_pass += pass_count
    grand_fail += fail_count

#----------- master reprot ---------------
today = datetime.now().strftime("%Y-%m-%d_%H-%m")
report_file = f"master_report_{today}.csv"
report_path = os.path.join(REPORT_FOLDER, report_file)

with open(report_path,"w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["File","Total", "Pass", "Fail"])
    writer.writerows(summary)
    writer.writerow([])
    writer.writerow(["ALL", grand_total, grand_pass, grand_fail])

print("\n======== MASTER SUMMARY =========")
print("Total: ",grand_total)
print("Pass: ",grand_pass)
print("Fail: ",grand_fail)
print("Report generated: ",report_path)