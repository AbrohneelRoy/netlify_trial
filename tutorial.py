file = open("sample.txt", "r")
frequent_word = ""
frequency = 0
words = []

for line in file:
    line_word = line.lower().strip().split(" ")
    for w in line_word:
        words.append(w)

for i in range(0, len(words)):
    count = 1
    for j in range(i + 1, len(words)):
        if words[i] == words[j]:
            count += 1
    if count > frequency:
        frequent_word = words[i]
        frequency = count

print("Most repeated word: " + frequent_word)
print("Frequency: " + str(frequency))
file.close()
