from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

tests = []

print("===================================")
print("FILE-BASED TEST SYSTEM")
print("DATE:",today)
print("===================================")

#------------- Input system ----------------

while True:
    name = input("Test name (or 'q' to quit): ")
    if  name == 'q':
        break
    result = input("Result (pass/fail): ").lower()

    test ={
        "name": name,
        "result": result
    }
    
    tests.append(test)

#-------------- processimg ------------------
pass_count = 0
fail_count = 0

for t in tests:
    if t["result"] == "pass":
        pass_count += 1
    else:
        fail_count += 1

total = len(tests)

#============= file automation ----------------
file_name = f"test_report_{today}.txt"

with open(file_name, "w", encoding="utf-8") as file:
    file.write("FILE-BASED TEST REPORT\n")
    file.write(f"DATE: {today}\n")
    file.write("-------------------------------\n")

    for i,t in enumerate(tests,start=1):
        file.write(f"{i}.{t['name']} : {t['result']}\n")
    
    file.write("\n====== SUMMARY ======\n")
    file.write(f"Total: {total}\n")
    file.write(f"Pass : {pass_count}\n")
    file.write(f"Fail: {fail_count}\n")

    if fail_count == 0:
        file.wrtie("Status: ALL PASS\n")
    else:
        file.write("Status: NEED INVESTIGATION\n")

print("\nReport generated",file_name)

#-------------- read file back ------------------

print("\n===== LOADING REPORT =====")
with open(file_name, "r", encoding="utf-8") as file:
    print(file.read())
