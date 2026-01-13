from datetime import datetime

project_name = "Auto Test Report System"
today = datetime.now().strftime("%Y-%m-%d")

print("===================================")
print("PROJECT :", project_name)
print("DATE    :", today)
print("TYPE    : Daily Test Report")
print("===================================")

name = input("Engineer name: ")

test_count = int(input("Total tests: "))
pass_count = int(input("Passed tests: "))
fail_count = test_count - pass_count

print("-----------------------------------")
print("TEST SUMMARY")
print("-----------------------------------")
print("Total :", test_count)
print("Pass  :", pass_count)
print("Fail  :", fail_count)

if fail_count == 0:
    print("Status: ALL PASS")
else:
    print("Status: NEED INVESTIGATION")

print("===================================")
print("End of report")