import sys
from collections import Counter


def edit_dist(str1, str2):
    m = len(str1)
    n = len(str2)
    mem = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                mem[i][j] = j
            elif j == 0:
                mem[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                mem[i][j] = mem[i - 1][j - 1]
            else:
                mem[i][j] = 1 + min(mem[i][j - 1],
                                    mem[i - 1][j],
                                    mem[i - 1][j - 1])

    return mem[m][n]


def find_best_match(all_best_matches):
    freq = 0
    match_found = all_best_matches[0]
    for match in all_best_matches:
        if (match in freq_counter):
            if (freq_counter[match] > freq):
                freq = freq_counter[match]
                match_found = match
    return match_found

# reading text file
dictionary = set(line.strip() for line in open('words_alpha.txt'))
f = open('austen-sense-corrupted.txt', 'r')
raw_data = f.read()
f.close()

# tokenization
delims = ['\n', '.', '!', '?', ',', ';', ':', '-', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
tokenized_data = [raw_data]
for delim in delims:
    temp = []
    for data in tokenized_data:
        if (data == ''):
            continue
        split_data = data.split(delim)
        res = [delim] * (2 * len(split_data) - 1)
        res[::2] = split_data
        split_data = res
        temp = temp + split_data
        split_data.clear()
    tokenized_data = temp

tokenized_data = tokenized_data[:50]
# frequent table for tie breaking
temp_tokenized_data = [x.lower() for x in tokenized_data]
freq_counter = dict(Counter(temp_tokenized_data))

# spell checking and getting corrected word from dictionary
corrected_text = []
local_dictionary = {}
for token in tokenized_data:
    if (not token.isalpha()):
        corrected_text.append(token)
    else:
        if (token.lower() in dictionary):
            corrected_text.append(token)
        elif (token in local_dictionary):
            corrected_text.append(local_dictionary[token])
        else:
            best_matches = []
            best_dist = sys.maxsize
            # case with words in all lowercase or all uppercase
            if (token.islower() or token.isupper()):
                for word in dictionary:
                    dist = edit_dist(token.lower(), word)
                    if (dist < best_dist):
                        best_matches.clear()
                        best_matches.append(word)
                        best_dist = dist
                    elif (dist == best_dist):
                        best_matches.append(word)
                best_match = find_best_match(best_matches)
                if (token.isupper()):
                    best_match = best_match.upper()
                corrected_text.append(best_match)
                local_dictionary[token] = best_match
            else:
                for word in dictionary:
                    dist = edit_dist(token.lower(), word)
                    if (dist < best_dist):
                        best_matches.clear()
                        best_matches.append(word)
                        best_dist = dist
                    elif (dist == best_dist):
                        best_matches.append(word)
                # don't correct if distance too big for words starting with uppercase letters
                if (best_dist > len(token) / 2):
                    corrected_text.append(token)
                    local_dictionary[token] = token
                else:
                    best_match = find_best_match(best_matches)
                    corrected_text.append(best_match)
                    local_dictionary[token] = best_match

# writing to output file
output_text = ''.join(corrected_text)
f = open('austen-sense-correct2.txt', 'wt')
f.write(output_text)
f.close()
