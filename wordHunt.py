import time


class Trie:
    """
    A data structure to efficiently find word possibilities - the fantastic thing about tries is that they will cut down on
    an enormous amount of time by helping us return early if the permutation of letters that we are currently on
    is not a fragment of a real word.
    """

    def __init__(self):
        self.children = {}

    def insert(self, word: str) -> None:
        current = self.children
        for i in word:
            if i not in current:
                current[i] = {}
            current = current[i]
        current["word"] = True

    def search(self, word: str) -> bool:
        current = self.children
        for i in word:
            if i not in current:
                return False
            current = current[i]
        return "word" in current

    def startsWith(self, prefix: str) -> bool:
        current = self.children
        for i in prefix:
            if i not in current:
                return False
            current = current[i]
        return True


class WordHunt:

    def __init__(self):
        # I build a word-checker trie off of collins_words.txt to efficiently check for valid words
        self._word_dict = Trie()
        for line in open('collins_words.txt'):
            self._word_dict.insert(line.strip())
        self._visited = [[False for _ in range(4)] for i in range(4)]
        self._w_matrix = self.parse_input()
        self._directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, -1), (1, 1), (-1, -1)]
        self._result = set()

    @staticmethod
    def parse_input() -> [[]]:
        """Asks for letters and parses it into a relevant matrix"""
        letters = input("Enter letters: ")
        counter = 0
        words = [[] for _ in range(4)]
        for i in range(16):
            words[counter].append(letters[i].upper())
            if (i + 1) % 4 == 0:
                counter += 1
        return words

    def get_words(self) -> None:
        """Starts looking for words in the matrix using the recursive search_strings func"""
        for row in range(len(self._w_matrix)):
            for col in range(len(self._w_matrix)):
                self.search_strings(row, col, "")

    def search_strings(self, row: int, col: int, word: str) -> None:
        """Uses DFS recursively to build new words and checks if they're valid or not"""
        if row < 0 or row >= 4 or col < 0 or col >= 4 or self._visited[row][col]:
            return
        word += self._w_matrix[row][col]
        if self._word_dict.startsWith(word):
            if self._word_dict.search(word):
                self._result.add(word)
        else:
            return
        self._visited[row][col] = True
        for direction in self._directions:
            self.search_strings(row + direction[0], col + direction[1], word)
        self._visited[row][col] = False

    def get_result(self) -> set:
        return self._result


def run():
    """Runs all relevant functions together"""
    word_hunt = WordHunt()
    start = time.time()
    word_hunt.get_words()
    found = word_hunt.get_result()
    end = time.time()
    for i in sorted(found, key=lambda x: len(x)):
        print(i)
    print("Seconds: ", (end - start))


if __name__ == '__main__':
    run()
