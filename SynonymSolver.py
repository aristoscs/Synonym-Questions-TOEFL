import collections
import time
import math
import re

def get_sentence_lists_from_files(books):
    sentences = []
    for i in range(0, len(books)):
        sentences += getSentenceLists(books[i])
    return sentences

def getSentenceLists(book):
    sentences = []
    with open(book, "r", buffering = 16777216, encoding = 'utf-8') as file:
        text = file.read().lower().strip("\n")
        Sentences = re.compile("[?.!]+").split(text)
        for i in range(0, len(Sentences)):
            sentences += [re.compile("[\W0-9]+").split(Sentences[i])]
            sentences[i] = [x for x in sentences[i] if len(x) > 0]
    return [sentences]

def build_semantic_descriptors(sentences):
    descriptors = collections.defaultdict(int)
    for book in range(0, len(sentences)):
        sentencesOfBook = sentences[book]
        for sentence in range(0, len(sentencesOfBook)):
            Sentence = sentencesOfBook[sentence]
            for word in range(0, len(Sentence)):
                string = Sentence[word]
                if string not in descriptors:
                    descriptors[string] = collections.defaultdict(int)
                for previous_word in range(0, word):
                    previous_string = Sentence[previous_word]
                    descriptors[string][previous_string] += 1
                    descriptors[previous_string][string] += 1
    return descriptors

answers = ""
def run_similarity_test(filename, semantic_descriptors):
    global answers
    questionCount = 0
    guessedRight = 0
    with open(filename, "r", encoding = "utf-8") as file:
        for line in file:
            split = line.strip("\n").split(" ")
            question = split[0]
            answer = split[1]
            questionCount += 1
            if most_similar_word(question, split, semantic_descriptors) == answer:
                answers += "\tAnswer is " + answer + " and AI guessed correctly\n\n"
                guessedRight += 1
            else:
                answers += "\tAnswer is " + answer + " and AI guessed incorrectly\n\n"
    answers += "Number of questions: " + str(questionCount) + "\n"
    answers += "Number of correct guesses: " + str(guessedRight) + "\n"
    answers += "AI was correct " + str((guessedRight / questionCount) * 100) + "% of the times!\n"
    print(answers)
    file = open("logs.txt", "w")
    file.write(answers)
    file.close()

def most_similar_word(word, choices, descriptors):
    global answers
    answers += word + ":\n"
    indexOfSynonym = 0
    biggestSimilarity = 0.0
    for i in range(2, len(choices)):
        similarity = 0.0
        if word in descriptors and choices[i] in descriptors:
            similarity = cosine_similarity(descriptors[word], descriptors[choices[i]])
        if similarity > biggestSimilarity:
            biggestSimilarity = similarity
            indexOfSynonym = i
        answers += "\t(" + chr(97 + i - 2) + ") " + choices[i]
        answers += ", " + str(similarity * 100) + "% to be synonym\n"
    return choices[indexOfSynonym]

def norm(vec):
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    dot_product = 0.0
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    return dot_product / (norm(vec1) * norm(vec2))

# Main program
start_time = time.time()
books = ["b1.txt", "b2.txt", "b3.txt"]
sentences = get_sentence_lists_from_files(books)
semantic_descriptors = build_semantic_descriptors(sentences)
run_similarity_test("toefel.txt", semantic_descriptors)
print("%s seconds" % (time.time() - start_time))