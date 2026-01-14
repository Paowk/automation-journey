from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

print("=================================")
print("MINI TEST MANAGEMENT SYSTEM")
print("DATE:", today)
print("=================================")

print("Mini Test Management System")
print("---------------------------")

tests = []

while True:
    test_name = input("Test name (or 'q' to quit): ")
    if test_name == 'q':
        break

    result = input("Result (pass/fail): ").lower()

    test = {
        "name" : test_name,
        "result" : result
    }

    tests.append(test)

print("\nAll test record:")
print(tests)

pass_count = 0
fail_count = 0

for t in tests:
    if t["result"]=="pass":
        pass_count +=1
    else:
        fail_count +=1
total = len(tests)

print("\n===== TEST SUMMARY =====")
print("Total:", total)
print("Pass :", pass_count)
print("Fail :", fail_count)

if fail_count == 0:
    print("Status: ALL PASS")
else:
    print("Status: NEED INVESTIGATION")

print("\n===== TEST DEATAIL ====== ")
for i, t in enumerate(tests,start=1):
    print(i,"-",t["name"],":",t["result"])