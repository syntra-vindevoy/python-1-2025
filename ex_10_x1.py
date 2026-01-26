from pathlib import Path

words = Path("words.txt").read_text().splitlines()
counts = {}

for word in words:
    s = str(sorted(word))

    if s in counts:
        counts[s].append(word)
    else:
        counts[s] = [word]

counts = sorted(counts.items(), key=lambda x: len(x[1]), reverse=True)
max_ana = len(counts[0][1])
counts = {k:v for k,v in counts if len(v) == max_ana}
print(max_ana)
print(counts)