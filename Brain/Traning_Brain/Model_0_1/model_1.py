import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Functions.Nova_Speak.speak import speak


# =========================================================
# SETTINGS
# =========================================================

DATASET_PATH = r"C:\Nova\Nova_Data\QNA_Data\qna.txt"

# Minimum similarity required to accept a Q&A match
MATCH_THRESHOLD = 0.35


# =========================================================
# LOAD Q&A DATASET
# =========================================================

def load_dataset(file_path):

    dataset = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # Q&A format:
                # question:answer

                if ":" not in line:
                    continue

                question, answer = line.split(
                    ":",
                    1
                )

                question = question.strip()
                answer = answer.strip()

                if question and answer:

                    dataset.append({
                        "question": question,
                        "answer": answer
                    })

        print(
            f"[Nova QNA] Loaded "
            f"{len(dataset)} Q&A pairs."
        )

        return dataset

    except FileNotFoundError:

        print(
            f"[Nova QNA] File not found:"
        )

        print(DATASET_PATH)

        return []

    except Exception as e:

        print(
            f"[Nova QNA] Dataset error: {e}"
        )

        return []


# =========================================================
# PREPROCESS TEXT
# =========================================================

def preprocess_text(text):

    stop_words = set(
        stopwords.words("english")
    )

    ps = PorterStemmer()

    tokens = word_tokenize(
        text.lower()
    )

    tokens = [
        ps.stem(token)
        for token in tokens
        if token.isalnum()
        and token not in stop_words
    ]

    return " ".join(tokens)


# =========================================================
# TRAIN TF-IDF
# =========================================================

def train_tfidf_vectorizer(dataset):

    corpus = [
        preprocess_text(
            qa["question"]
        )
        for qa in dataset
    ]

    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(
        corpus
    )

    return vectorizer, X


# =========================================================
# FIND BEST ANSWER
# =========================================================

def get_answer(
    question,
    vectorizer,
    X,
    dataset
):

    processed_question = preprocess_text(
        question
    )

    # Nothing useful after preprocessing
    if not processed_question:

        return None, 0.0


    question_vec = vectorizer.transform(
        [processed_question]
    )


    similarities = cosine_similarity(
        question_vec,
        X
    )[0]


    best_match_index = similarities.argmax()

    best_score = similarities[
        best_match_index
    ]


    print(
        f"[Nova QNA] Similarity: "
        f"{best_score:.3f}"
    )

    print(
        f"[Nova QNA] Best match: "
        f"{dataset[best_match_index]['question']}"
    )


    # =====================================================
    # CHECK SIMILARITY THRESHOLD
    # =====================================================

    if best_score < MATCH_THRESHOLD:

        print(
            "[Nova QNA] No reliable Q&A match."
        )

        return None, best_score


    answer = dataset[
        best_match_index
    ]["answer"]


    return answer, best_score


# =========================================================
# MAIN Q&A FUNCTION
# =========================================================

def mind(text):

    if not text:

        return False


    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------

    dataset = load_dataset(
        DATASET_PATH
    )


    if not dataset:

        return False


    try:

        # -------------------------------------------------
        # Train TF-IDF
        # -------------------------------------------------

        vectorizer, X = train_tfidf_vectorizer(
            dataset
        )


        # -------------------------------------------------
        # Find answer
        # -------------------------------------------------

        answer, score = get_answer(
            text,
            vectorizer,
            X,
            dataset
        )


        # -------------------------------------------------
        # Q&A MATCH FOUND
        # -------------------------------------------------

        if answer:

            print(
                "[Nova QNA] Answer found."
            )

            speak(answer)

            return True


        # -------------------------------------------------
        # NO MATCH
        # -------------------------------------------------

        print(
            "[Nova QNA] Sending question "
            "to next handler..."
        )

        return False


    except Exception as e:

        print(
            f"[Nova QNA] Error: {e}"
        )

        return False


# =========================================================
# TESTING ONLY
# =========================================================

"""
mind("hello assistant")
"""
