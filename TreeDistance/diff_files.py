f1 = open("e1.txt", "r")
f2 = open("e2.txt", "r")

miss = 0
lines = {}
count = 0

for x in f1:
  lines[str(count)] = x
  count += 1

count = 0
for x in f2:
  if lines[str(count)] != x:
    print(count, "before", lines[str(count)], "after", x)
    miss += 1

  count += 1

print("misses: ", miss)
