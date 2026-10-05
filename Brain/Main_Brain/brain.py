import re

from Functions.Nova_Speak.speak import speak
from Brain.Main_Brain.deep_search_data import Nova_search
from Brain.Main_Brain.small_search_data import search_and_read


# ============================================================
# CONFIGURATION
# ============================================================

QA_FILE_PATH = (
    r"C:\Users\Radhika\OneDrive\Desktop\Nova"
    r"\Nova_Data\QNA_Data\qna.txt"
)

QA_MIN_SCORE = 0.75


# ============================================================
# LOAD Q&A DATA
# ============================================================

def load_qa_data(file_path):

    qa_dict = {}

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split(":", 1)

                if len(parts) != 2:
                    continue

                question = parts[0].strip().lower()
                answer = parts[1].strip()

                if question and answer:

                    qa_dict[question] = answer

    except FileNotFoundError:

        pass

    except Exception:

        pass

    return qa_dict


qa_dict = load_qa_data(
    QA_FILE_PATH
)


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {

    "a",
    "an",
    "the",

    "is",
    "are",
    "am",
    "was",
    "were",

    "what",
    "who",
    "where",
    "when",
    "why",
    "how",

    "can",
    "could",
    "would",
    "should",

    "do",
    "does",
    "did",

    "tell",
    "me",
    "about",
    "please",
    "give",
    "get",
    "know",

    "you",
    "your",

    "i",
    "my",

    "to",
    "for",
    "of",
    "in",
    "on",
    "with",

    "and",
    "or",

    "this",
    "that",
    "it",

    "be",
    "from",
    "as",
    "at",

    "have",
    "has",
    "had"
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CLEAN USER QUERY
# ============================================================

def clean_query(text):

    text = normalize_text(text)

    text = re.sub(
        r"\bnova\b",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT KEYWORDS
# ============================================================

def extract_keywords(text):

    text = normalize_text(text)

    words = re.findall(
        r"[a-zA-Z0-9]+",
        text
    )

    keywords = []

    for word in words:

        if word == "nova":
            continue

        if word in STOP_WORDS:
            continue

        keywords.append(word)

    return keywords


# ============================================================
# DEEP SEARCH PHRASES
# ============================================================

DEEP_SEARCH_PHRASES = [

    "in depth",
    "in detail",
    "deep search",
    "deep research",
    "detailed research",
    "detailed information",
    "research about",
    "research on",
    "do research",
    "do deep research",
    "research",
    "deeply",
    "comprehensive information",
    "complete information",
    "thorough information",
    "elaborate",
    "explain in detail",
    "explain deeply",
    "give detailed information",
    "give me detailed information",
    "tell me in detail",
    "tell me in depth"
]


# ============================================================
# CHECK DEEP SEARCH INTENT
# ============================================================

def wants_deep_search(text):

    text = normalize_text(text)

    for phrase in DEEP_SEARCH_PHRASES:

        if phrase in text:

            return True

    return False


# ============================================================
# EXTRACT DEEP SEARCH TOPIC
# ============================================================

def extract_research_topic(text):

    text = clean_query(text)

    if not text:

        return ""


    # --------------------------------------------------------
    # Remove deep-search phrases
    # --------------------------------------------------------

    for phrase in sorted(
        DEEP_SEARCH_PHRASES,
        key=len,
        reverse=True
    ):

        text = text.replace(
            phrase,
            " "
        )


    # --------------------------------------------------------
    # Remove question patterns
    # --------------------------------------------------------

    patterns = [

        r"^what is\s+",
        r"^what are\s+",
        r"^who is\s+",
        r"^who are\s+",
        r"^where is\s+",
        r"^where are\s+",
        r"^tell me about\s+",
        r"^tell me\s+about\s+",
        r"^can you tell me about\s+",
        r"^could you tell me about\s+",
        r"^give me information about\s+",
        r"^give me information on\s+",
        r"^give me details about\s+",
        r"^give me details on\s+",
        r"^give me detailed information about\s+",
        r"^give me detailed information on\s+",
        r"^explain\s+",
        r"^describe\s+",
        r"^research\s+",
        r"^research about\s+",
        r"^research on\s+",
        r"^do research on\s+",
        r"^do research about\s+"
    ]


    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text
        )


    # --------------------------------------------------------
    # Remove filler
    # --------------------------------------------------------

    filler_patterns = [

        r"\bgive me\b",
        r"\btell me\b",
        r"\babout\b",
        r"\binformation\b",
        r"\binformation on\b",
        r"\binformation about\b",
        r"\bdetails\b",
        r"\bdetails on\b",
        r"\bdetails about\b",
        r"\bplease\b",
        r"\bcan you\b",
        r"\bcould you\b",
        r"\bdo you know\b",
        r"\bwhat do you know about\b"
    ]


    for pattern in filler_patterns:

        text = re.sub(
            pattern,
            " ",
            text
        )


    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    text = re.sub(
        r"[?!.,]+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    return text


# ============================================================
# FIND BEST Q&A ANSWER
# ============================================================

def find_best_answer(text):

    clean_user = clean_query(text)

    if not clean_user:
        return None, 0.0


    # ========================================================
    # 1. EXACT QUESTION MATCH
    # ========================================================

    for question, answer in qa_dict.items():

        clean_question = clean_query(question)

        if clean_user == clean_question:
            """
            print(
                f"[Nova] Exact Q&A match: {question}"
            )"""

            return answer, 1.0


    # ========================================================
    # 2. KEYWORD MATCH
    # ========================================================

    user_keywords = extract_keywords(
        clean_user
    )

    if not user_keywords:
        return None, 0.0


    user_set = set(
        user_keywords
    )


    best_answer = None
    best_score = 0.0
    best_question = None


    for question, answer in qa_dict.items():

        clean_question = clean_query(
            question
        )

        question_keywords = extract_keywords(
            clean_question
        )

        if not question_keywords:
            continue


        question_set = set(
            question_keywords
        )


        matched_words = (
            user_set &
            question_set
        )

        if not matched_words:
            continue


        question_coverage = (
            len(matched_words)
            /
            len(question_set)
        )


        user_coverage = (
            len(matched_words)
            /
            len(user_set)
        )


        score = (
            question_coverage * 0.7
            +
            user_coverage * 0.3
        )


        # ----------------------------------------------------
        # ALL QUESTION KEYWORDS MATCH
        # ----------------------------------------------------

        if question_set.issubset(user_set):

            score += 0.15


        # ----------------------------------------------------
        # QUESTION IS INSIDE USER QUERY
        # ----------------------------------------------------

        if clean_question in clean_user:

            score += 0.20


        if score > best_score:

            best_score = score
            best_answer = answer
            best_question = question


    # ========================================================
    # ACCEPT Q&A MATCH
    # ========================================================

    if (
        best_answer
        and
        best_score >= QA_MIN_SCORE
    ):
        """
        print(
            f"[Nova] Q&A match: {best_question}"
        )

        print(
            f"[Nova] Q&A confidence: "
            f"{best_score:.2f}"
        ) """

        return best_answer, best_score


    return None, best_score


# ============================================================
# SPEAK Q&A ANSWER
# ============================================================

def speak_qa_answer(answer):

    if not answer:
        return False


    answer = str(
        answer
    ).strip()


    if not answer:
        return False


    # IMPORTANT:
    # Do NOT print the answer here.
    #
    # speak() already handles the output.
    # Printing here caused the answer to appear twice.

    try:

        speak(
            answer
        )

        return True

    except Exception as e:

        print(
            f"[Nova] Speech error: {e}"
        )

        return False


def clean_search_result(result):

    if not result:

        return None


    result = str(result)


    prefixes = [

        "wikipedia wiki",
        "wiki wikipedia",
        "wikipedia",
        "wiki"

    ]


    for prefix in prefixes:

        if result.lower().startswith(prefix):

            result = result[
                len(prefix):
            ].strip()


    result = re.sub(
        r"\s+",
        " ",
        result
    ).strip()


    # --------------------------------------------------------
    # Fix broken encoding
    # --------------------------------------------------------

    result = result.replace(
        "â",
        "'"
    )

    result = result.replace(
        "â€™",
        "'"
    )

    result = result.replace(
        "â",
        "-"
    )

    result = result.replace(
        "â",
        "-"
    )

    result = result.replace(
        "Â",
        ""
    )


    if not result:

        return None


    return result


# ============================================================
# SPEAK SEARCH RESULT
# ============================================================

def speak_search_result(result):

    result = clean_search_result(
        result
    )

    if not result:
        return False


    # IMPORTANT:
    # Do NOT print result here.
    #
    # speak() already handles the NOVA output.
    # This prevents web-search answers from appearing twice.

    try:

        speak(
            result
        )

        return True

    except Exception as e:

        print(
            f"[Nova] Speech error: {e}"
        )

        return False


# ============================================================
# BRAIN COMMAND
# ============================================================

def brain_cmd(text):

    if not text:
        return False


    # ========================================================
    # CLEAN QUERY
    # ========================================================

    query = clean_query(
        text
    )


    if not query:
        return False


    # IMPORTANT:
    # Do NOT print:
    #
    # print("NOVA:", query)
    #
    # main.py is already displaying the recognized query.
    # Printing it here causes duplicate query output.


    # ========================================================
    # STEP 1
    # DEEP SEARCH
    # ========================================================

    if wants_deep_search(query):

        research_topic = extract_research_topic(
            query
        )


        if not research_topic:

            research_topic = query

        """
        print(
            f"[Nova] Deep search topic: "
            f"{research_topic}"
        )"""


        try:

            result = Nova_search(
                research_topic
            )


            if result:

                return True


        except Exception as e:
            """
            print(
                f"[Nova] Deep search error: {e}"
            )"""


        # ----------------------------------------------------
        # SMALL SEARCH FALLBACK
        # ----------------------------------------------------

        try:

            result = search_and_read(
                research_topic
            )


            if result:

                return speak_search_result(
                    result
                )


        except Exception as e:

            print(
                f"[Nova] Small search fallback error: {e}"
            )


        return False


    # ========================================================
    # STEP 2
    # Q&A.TXT
    #
    # Q&A IS ALWAYS CHECKED BEFORE WEB SEARCH.
    # ========================================================

    answer, confidence = find_best_answer(
        query
    )


    if answer:

        return speak_qa_answer(
            answer
        )


    # ========================================================
    # STEP 3
    # SMALL WEB SEARCH
    # ========================================================

    try:

        result = search_and_read(
            query
        )


        if result:

            return speak_search_result(
                result
            )


    except Exception as e:
        """ 
        print(
            f"[Nova] Small search error: {e}"
        )"""


    # ========================================================
    # STEP 4
    # DEEP SEARCH FALLBACK
    # ========================================================

    try:

        research_topic = extract_research_topic(
            query
        )


        if not research_topic:

            research_topic = query


        result = Nova_search(
            research_topic
        )


        if result:

            return True


    except Exception as e:

        print(
            f"[Nova] Deep search fallback error: {e}"
        )


    # ========================================================
    # NOTHING FOUND
    # ========================================================

    message = (
        "I couldn't find enough information "
        "to answer that."
    )


    try:

        speak(
            message
        )

    except Exception:

        pass


    return False
"""

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_questions = [

        "Nova what is programming",

        "Nova what is nashik",

        "how can i improve Nova's recognition",

        "Nova what is Nashik",

        "Nova tell me about Earth",

        "Nova tell me about Earth in depth",

        "Nova explain machine learning in detail",

        "Nova give me detailed information about cybersecurity"

    ]


    for question in test_questions:

        print(
            "\n============================================================"
        )

        print(
            "NOVA:",
            question
        )

        try:

            brain_cmd(
                question
            )

        except Exception:

            pass
"""