import string

# ---------------------------------------------------
# Step 1: Document Collection
# ---------------------------------------------------
documents = {
    1: "Python is an interpreted programming language used for web development and data science.",
    2: "Java is a compiled object oriented programming language used for android apps and enterprise systems.",
    3: "JavaScript is an interpreted programming language used for web development.",
    4: "C++ is a compiled programming language used for game development and system programming.",
    5: "Ruby is an interpreted programming language used for web development with the Rails framework.",
    6: "Go is a compiled programming language developed by Google used for cloud systems.",
    7: "Rust is a compiled programming language used for safe system programming.",
    8: "Swift is a compiled programming language developed by Apple used for iOS apps."
}

# Function to add a new document to the collection
def add_document(doc_id, text):
    documents[doc_id] = text

# ---------------------------------------------------
# Step 2: Preprocessing
# ---------------------------------------------------
def preprocess(text):
    text = text.lower()
    for punct in string.punctuation:
        text = text.replace(punct, " ")
    tokens = text.split()
    return tokens

# ---------------------------------------------------
# Step 3: Building Dictionary and Inverted Index
# ---------------------------------------------------
def build_index(documents):
    dictionary = set()
    inverted_index = {}

    for doc_id, text in documents.items():
        tokens = preprocess(text)
        for token in tokens:
            dictionary.add(token)
            if token not in inverted_index:
                inverted_index[token] = set()
            inverted_index[token].add(doc_id)

    return sorted(dictionary), inverted_index

# ---------------------------------------------------
# Step 4: Boolean Retrieval Functions
# ---------------------------------------------------
def get_postings(term, inverted_index):
    return inverted_index.get(term.lower(), set())

def boolean_and(term1, term2, inverted_index):
    return get_postings(term1, inverted_index) & get_postings(term2, inverted_index)

def boolean_or(term1, term2, inverted_index):
    return get_postings(term1, inverted_index) | get_postings(term2, inverted_index)

def boolean_not(term, inverted_index, all_doc_ids):
    return all_doc_ids - get_postings(term, inverted_index)

# ---------------------------------------------------
# Step 5: Print Query Results
# ---------------------------------------------------
def print_result(query_label, doc_ids):
    print("QUERY:", query_label)
    print("Result:")
    for doc_id in sorted(doc_ids):
        print(f"doc{doc_id}: {documents[doc_id]}")
    print()

# ---------------------------------------------------
# Step 6: Run the System
# ---------------------------------------------------
if __name__ == "__main__":
    dictionary, inverted_index = build_index(documents)
    all_doc_ids = set(documents.keys())

    print("Documents:")
    for doc_id, text in documents.items():
        print(doc_id, ":", text)

    print("\nDictionary (Vocabulary):")
    print(dictionary)

    print("\nInverted Index:")
    for term in dictionary:
        print(term, "->", sorted(inverted_index[term]))

    print("\nSample Boolean Queries:")
    print("python ->", get_postings("python", inverted_index))
    print("web AND development ->", boolean_and("web", "development", inverted_index))
    print("compiled OR interpreted ->", boolean_or("compiled", "interpreted", inverted_index))
    print("programming AND NOT web ->", get_postings("programming", inverted_index) & boolean_not("web", inverted_index, all_doc_ids))
    print("NOT web ->", boolean_not("web", inverted_index, all_doc_ids))

    print("\nFormatted Query Results:")
    print_result("python", get_postings("python", inverted_index))
    print_result("web AND development", boolean_and("web", "development", inverted_index))
    print_result("compiled OR interpreted", boolean_or("compiled", "interpreted", inverted_index))
    print_result("programming AND NOT web", get_postings("programming", inverted_index) & boolean_not("web", inverted_index, all_doc_ids))
    print_result("NOT web", boolean_not("web", inverted_index, all_doc_ids))