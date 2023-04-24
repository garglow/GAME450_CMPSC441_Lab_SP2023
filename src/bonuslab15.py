# Import the required libraries


from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Load a pre-trained model from the Sentence Transformers library
model = SentenceTransformer('bert-base-nli-mean-tokens')

#comparison sentences based off of prompt:
# Is computer science the best degree someone can get within a 4-year undergraduate college?
sentence1 = "The answer to this question depends on the individual's interests, career goals, and personal circumstances. Computer Science is an excellent field with a lot of potential for growth, innovation, and career opportunities. It is a popular degree choice because of the high demand for professionals in the industry and the potential for high salaries. However, there are many other degrees that can provide excellent career prospects and personal satisfaction."
sentence2 = "There is no single 'best' degree that someone can get within a 4-year undergraduate college. The value of a degree depends on a variety of factors, including the individual's career goals, interests, and personal strengths."

# Convert the sentences to embeddings
embedding1 = model.encode(sentence1, convert_to_tensor=True)
embedding2 = model.encode(sentence2, convert_to_tensor=True)

# Calculate the cosine similarity between the embeddings
similarity = 1 - cosine(embedding1, embedding2)

# Print the similarity score
print(f"The similarity score between the two sentences is: {similarity}")
#it was 0.42956796288490295


#a different metric to discuss similiraities between text written by the same individual
# is reused and popular words, bigrams(2 word phrases), and trigrams(3 word phrases)
"""
sentence 1 uses:
career	3
personal	2
excellent	2
potential	2
high	2
degree 1

while sentence 2 uses
career 1
degree 1


sentence 1 uses:
and personal	2
potential for	2

while sentence 2 uses none of them

and sentence 2 uses no popular or reoccuring bigrams


therefore, the prompt being the same, generated 2 very disimilar responses from chatgpt
their sentence similarities are also below .50




"""
