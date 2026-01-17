tests = []

while True:
    name = input("Test name : ")
    if name == 'q':
        break
    result = input("Result (pass/fail); ").lower()
    tests.append(result)

total = len(tests)
pass_count = tests.count("pass")
fail_count = tests.count("fail")

print("\n======= SUMMARY =========")
print("Total:", total)
print("Pass:", pass_count)
print("Fail:", fail_count)