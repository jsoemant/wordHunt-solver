import time

"""
NOTE: This is the fast(er) wordHunt solver for reasons I detail in the README of the repo.
This wordHunt solver is around 1.4x faster than the other one and depending on your computer that may factor
in a few extra seconds, but in most cases I doubt it will make a real difference.
"""

# I build a word-checker set off of collins_words.txt to efficiently check for valid words
d = set(line.strip() for line in open('collins_words.txt'))


def parse_input() -> [[]]:
    """Asks for letters and parses it into a relevant matrix"""
    letters = input("Enter letters: ")
    counter = 0
    words = [[] for i in range(4)]
    for i in range(16):
        words[counter].append(letters[i].upper())
        if (i + 1) % 4 == 0:
            counter += 1
    return words


def get_words(words: [[]]) -> set:
    """Starts looking for words in the matrix using the recursive search_strings func"""
    result = set()
    visited = [[False for i in range(len(words[0]))] for i in range(len(words))]
    for row in range(len(words)):
        for col in range(len(words)):
            visited[row][col] = True
            search_strings(row, col, words, result, visited, "")
            visited[row][col] = False
    return result


def search_strings(row: int, col: int, words: [[]], result: set, visited: [[]], word: str) -> None:
    """Uses DFS recursively to build new words and checks if they're valid or not"""
    if len(word) >= 10:
        return
    word += words[row][col]
    if len(word) >= 4:
        if word in d:
            result.add(word)
    # top
    if row != 0 and not visited[row - 1][col]:
        visited[row - 1][col] = True
        search_strings(row - 1, col, words, result, visited, word)
        visited[row - 1][col] = False
    # bottom
    if row != len(words) - 1 and not visited[row + 1][col]:
        visited[row + 1][col] = True
        search_strings(row + 1, col, words, result, visited, word)
        visited[row + 1][col] = False
    # left
    if col != 0 and not visited[row][col - 1]:
        visited[row][col - 1] = True
        search_strings(row, col - 1, words, result, visited, word)
        visited[row][col - 1] = False
    # right
    if col != len(words[0]) - 1 and not visited[row][col + 1]:
        visited[row][col + 1] = True
        search_strings(row, col + 1, words, result, visited, word)
        visited[row][col + 1] = False
    # top left
    if row != 0 and col != 0 and not visited[row - 1][col - 1]:
        visited[row - 1][col - 1] = True
        search_strings(row - 1, col - 1, words, result, visited, word)
        visited[row - 1][col - 1] = False
    # top right
    if row != 0 and col != len(words[0]) - 1 and not visited[row - 1][col + 1]:
        visited[row - 1][col + 1] = True
        search_strings(row - 1, col + 1, words, result, visited, word)
        visited[row - 1][col + 1] = False
    # bottom left
    if row != len(words) - 1 and col != 0 and not visited[row + 1][col - 1]:
        visited[row + 1][col - 1] = True
        search_strings(row + 1, col - 1, words, result, visited, word)
        visited[row + 1][col - 1] = False
    # bottom right
    if row != len(words) - 1 and col != len(words[0]) - 1 and not visited[row + 1][col + 1]:
        visited[row + 1][col + 1] = True
        search_strings(row + 1, col + 1, words, result, visited, word)
        visited[row + 1][col + 1] = False


def run():
    """Runs all relevant functions together and prints out valid results"""
    words = parse_input()
    start = time.time()
    found = get_words(words)
    end = time.time()
    for i in sorted(list(found), key=lambda x: len(x)):
        print(i)
    print("Seconds: ", (end - start))


if __name__ == '__main__':
    run()
