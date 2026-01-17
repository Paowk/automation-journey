from datetime import datetime

file_name = f"report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt"

tests = ["pass", "fail", "total"]

with open(file_name, "w", encoding="utf-8") as file:
    file.write("TEST REPORT\n")
    for t in tests:
        file.write(t+ "\n")

print("Report created:",file_name)

print("\n===== LOAD REPORT =====")
with open(file_name,"r",encoding="utf-8") as file:
    print(file.read())