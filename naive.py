import re
import numpy as np

# Sample training data
data = [
    ("This is a spam email", "spam"),
    ("Buy one get one free", "spam"),
    ("Hello, how are you?", "ham"),
    ("Congratulations, you've won a prize!", "spam"),
    ("Meeting at 3 PM", "ham"),
    ("Get a discount on your next purchase", "spam"),  # Replaced "Viagra for sale"
]

# Preprocess the training data
word_set = set()
for text, label in data:
    words = re.findall(r'\w+', text.lower())
    word_set.update(words)

word_list = list(word_set)
word_list.sort()

# Create a vocabulary
vocab = {word: index for index, word in enumerate(word_list)}

# Initialize counts for spam and ham
spam_count = 0
ham_count = 0

# Count the occurrences of words in spam and ham messages
spam_word_count = np.zeros(len(vocab))
ham_word_count = np.zeros(len(vocab))

# Populate the counts
for text, label in data:
    words = re.findall(r'\w+', text.lower())
    label_count = spam_word_count if label == 'spam' else ham_word_count
    for word in words:
        if word in vocab:
            word_index = vocab[word]
            label_count[word_index] += 1

# Calculate the prior probabilities
total_messages = len(data)
prior_spam = spam_count / total_messages
prior_ham = ham_count / total_messages

# Input text to classify
input_text = "You've won a free vacation!"

# Tokenize and process the input text
input_words = re.findall(r'\w+', input_text.lower())

# Calculate likelihoods and apply the Naive Bayes formula
likelihood_spam = 1.0
likelihood_ham = 1.0
for word in input_words:
    if word in vocab:
        word_index = vocab[word]
        likelihood_spam *= (spam_word_count[word_index] + 1) / (spam_count + len(vocab))
        likelihood_ham *= (ham_word_count[word_index] + 1) / (ham_count + len(vocab))

# Apply Bayes' theorem
posterior_spam = prior_spam * likelihood_spam
posterior_ham = prior_ham * likelihood_ham

# Classify as spam or ham
if posterior_spam > posterior_ham:
    print("Classified as: spam")
else:
    print("Classified as: ham")
