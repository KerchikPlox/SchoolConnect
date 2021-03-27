inp = open('input.txt', 'r')
lines = inp.readlines()
inp.close()
answers = []
out = open('output.txt', 'w')
a, b, d = lines[0].split()
k = 0
for i in range(int(a), int(b)):
    if i % 10 == int(d):
        k += 1
out.write(str(k))
