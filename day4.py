import csv
from datetime import datetime

today = datetime.now().strftime("%y-%m-%d")
file_name = f"test_data_{today}.csv"


print("==================================")
print("CSV-BASE TEST SYSTEM")
print("Date",today)
print("==================================")

#----------- Input system ---------------
tests = []

while True:
    name = input("Test name (or 'q' to quit): ")
    if name == 'q':
        break
    
    result = input("Result (pass/fail): ").lower()

    tests.append([name, result])

#------------ write csv ---------------
with open(file_name, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Test Name", "Result"]) #Header

    for t in tests:
        writer.writerow(t)

print("\nCSV file generated", file_name)

#------------- read csv ---------------

print("\n===== LOADING CSV DATA =====")

loaded_tests = []

with open(file_name, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader) # skip headr

    for row in reader:
        loaded_tests.append(row)

#----------- processing ---------------
pass_count = 0
fail_count = 0

for t in loaded_tests:
    if t[1] == "pass":
        pass_count += 1
    else:
        fail_count += 1
total = len(loaded_tests)

#-------------- report ----------------
print("========SUMMARY========")
print("Total:",total)
print("Pass:",pass_count)
print("Fail:",fail_count)

if fail_count == 0:
    print("Status: ALL PASS")
else:
    print("Status: NEED INVESTIGATION")