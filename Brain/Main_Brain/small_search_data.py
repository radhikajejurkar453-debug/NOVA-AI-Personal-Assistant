import re

from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Functions.Nova_Speak.speak import *


# ============================================================
# EDGE DRIVER SETUP
# ============================================================

EDGE_DRIVER_PATH = (
    r"C:\Nova\Nova_Data\edge_driver\msedgedriver.exe"
)

_driver = None


# ============================================================
# CREATE EDGE DRIVER
# ============================================================

def _get_driver():

    global _driver

    if _driver is None:

        edge_options = Options()

        edge_options.add_argument(
            "--headless=new"
        )

        edge_options.add_argument(
            "--window-size=1920,1080"
        )

        edge_options.add_argument(
            "--disable-gpu"
        )

        edge_options.add_argument(
            "--disable-notifications"
        )

        edge_options.add_argument(
            "--disable-popup-blocking"
        )

        edge_options.add_argument(
            "--no-first-run"
        )

        edge_options.add_argument(
            "--disable-features=msEdgeSignin"
        )

        edge_options.add_argument(
            "--lang=en-US"
        )

        edge_options.add_argument(
            "user-agent=Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0.0.0 "
            "Safari/537.36 "
            "Edg/120.0.0.0"
        )

        edge_service = Service(
            EDGE_DRIVER_PATH
        )

        _driver = webdriver.Edge(
            service=edge_service,
            options=edge_options
        )

    return _driver


# ============================================================
# CLEAN SEARCH TEXT
# ============================================================

def _clean_text(text):

    if not text:
        return ""

    # --------------------------------------------------------
    # REMOVE URLS
    # --------------------------------------------------------

    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # REMOVE TRUNCATION
    # --------------------------------------------------------

    text = re.sub(
        r"\s*…\s*$",
        "",
        text
    )

    text = re.sub(
        r"\s*\.\.\.\s*$",
        "",
        text
    )

    # --------------------------------------------------------
    # REMOVE BING DATE PREFIX
    # --------------------------------------------------------

    text = re.sub(
        r"^[A-Z][a-z]{2}\s+\d{1,2},\s*\d{4}"
        r"\s*[·\-–]\s*",
        "",
        text
    )

    # --------------------------------------------------------
    # REMOVE BING ANNOTATIONS
    # --------------------------------------------------------

    text = re.sub(
        r"Missing:\s*\S+\s*Must include:\s*\S+",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # REMOVE COMMON WEBSITE LABELS
    # --------------------------------------------------------

    unwanted_patterns = [

        # Wikipedia
        r"\bWikipedia\b",
        r"\bWiki\b",

        # Programming sites
        r"\bGeeksforGeeks\b",
        r"\bStack Overflow\b",
        r"\bW3Schools\b",

        # Social / promotional
        r"\bFollow me\b",
        r"\bFollow us\b",
        r"\bFollow for more\b",
        r"\bFollow\b",

        # Navigation
        r"\bRead more\b",
        r"\bLearn more\b",
        r"\bSee more\b",
        r"\bMore\b",
        r"\bSearch\b",
        r"\bWeb results\b",

        # Search categories
        r"\bImages\b",
        r"\bVideos\b",
        r"\bNews\b",
        r"\bShopping\b",
        r"\bMaps\b",
        r"\bBooks\b",
        r"\bTools\b",

        # Account / website UI
        r"\bSign in\b",
        r"\bLog in\b",
        r"\bLogin\b",
        r"\bSubscribe\b",
        r"\bSubscriptions\b",

        # Advertisement
        r"\bAdvertisement\b",
        r"\bSponsored\b",
        r"\bAd\b",

        # Website messages
        r"\bCookie policy\b",
        r"\bPrivacy policy\b",
        r"\bTerms of service\b",
        r"\bAccept cookies\b",

        # Other common noise
        r"\bIntroduction\b",
        r"\bHome\b",
        r"\bMenu\b",
        r"\bShare\b",
        r"\bRelated\b",
        r"\bRecommended\b",
        r"\bAll rights reserved\b"

    ]

    for pattern in unwanted_patterns:

        text = re.sub(
            pattern,
            " ",
            text,
            flags=re.IGNORECASE
        )

    # --------------------------------------------------------
    # REMOVE RAW URL SLUGS
    # --------------------------------------------------------

    text = re.sub(
        r"\b[\w-]+_[\w-]+\b",
        " ",
        text
    )

    # --------------------------------------------------------
    # REMOVE BREADCRUMB SYMBOLS
    # --------------------------------------------------------

    text = text.replace(
        "›",
        " "
    )

    text = text.replace(
        "»",
        " "
    )

    text = text.replace(
        "•",
        " "
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATE SPACES
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# EXTRACT FIRST USEFUL BING RESULT
# ============================================================

def _get_bing_result(driver):

    selectors = [

        "li.b_algo",
        "div.b_algo",
        "li.b_ans"

    ]

    for selector in selectors:

        try:

            results = driver.find_elements(
                By.CSS_SELECTOR,
                selector
            )

            for result in results:

                try:

                    title = ""
                    snippet = ""

                    # ------------------------------------------------
                    # TITLE
                    # ------------------------------------------------

                    try:

                        title = result.find_element(
                            By.CSS_SELECTOR,
                            "h2"
                        ).text.strip()

                    except Exception:

                        pass

                    # ------------------------------------------------
                    # SNIPPET
                    # ------------------------------------------------

                    try:

                        caption = result.find_element(
                            By.CSS_SELECTOR,
                            ".b_caption"
                        )

                        try:

                            snippet = caption.find_element(
                                By.CSS_SELECTOR,
                                "p"
                            ).text.strip()

                        except Exception:

                            snippet = caption.text.strip()

                    except Exception:

                        pass

                    # ------------------------------------------------
                    # FALLBACK SNIPPET
                    # ------------------------------------------------

                    if not snippet:

                        raw_text = result.text.strip()

                        if title:

                            raw_text = raw_text.replace(
                                title,
                                "",
                                1
                            )

                        snippet = raw_text

                    # ------------------------------------------------
                    # CLEAN
                    # ------------------------------------------------

                    title = _clean_text(
                        title
                    )

                    snippet = _clean_text(
                        snippet
                    )

                    # ------------------------------------------------
                    # REMOVE DUPLICATED TITLE
                    # ------------------------------------------------

                    if (
                        title
                        and
                        snippet.lower().startswith(
                            title.lower()
                        )
                    ):

                        snippet = snippet[
                            len(title):
                        ].strip(
                            " .:-"
                        )

                    # ------------------------------------------------
                    # BUILD RESULT
                    # ------------------------------------------------

                    if title and snippet:

                        answer = (
                            title
                            + ". "
                            + snippet
                        )

                    elif snippet:

                        answer = snippet

                    elif title:

                        answer = title

                    else:

                        continue

                    answer = _clean_text(
                        answer
                    )

                    if len(answer) >= 30:

                        return answer

                except Exception:

                    continue

        except Exception:

            continue

    return None


# ============================================================
# MAKE SMALL ANSWER
# ============================================================

def _make_small_answer(text):

    if not text:
        return None

    text = _clean_text(
        text
    )

    # --------------------------------------------------------
    # REMOVE WEBSITE LABELS AT BEGINNING
    # --------------------------------------------------------

    text = re.sub(
        r"^(Wikipedia|Wiki)\s*[-:.]\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^(Microsoft|Bing)\s*[-:.]\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # SPLIT SENTENCES
    # --------------------------------------------------------

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    sentences = [

        sentence.strip()

        for sentence in sentences

        if sentence.strip()

    ]

    # --------------------------------------------------------
    # REMOVE USELESS SENTENCES
    # --------------------------------------------------------

    useless_phrases = [

        "follow me",
        "follow us",
        "read more",
        "learn more",
        "see more",
        "subscribe",
        "sign in",
        "log in",
        "advertisement",
        "cookie policy",
        "privacy policy",
        "terms of service",
        "geeksforgeeks",
        "wikipedia",
        "wiki"

    ]

    selected = []

    for sentence in sentences:

        if len(sentence) < 20:
            continue

        sentence_lower = (
            sentence.lower()
        )

        if any(
            phrase in sentence_lower
            for phrase in useless_phrases
        ):
            continue

        selected.append(
            sentence
        )

        if len(selected) >= 2:
            break

    # --------------------------------------------------------
    # CREATE ANSWER
    # --------------------------------------------------------

    if selected:

        answer = " ".join(
            selected
        )

    else:

        answer = text

    # --------------------------------------------------------
    # WORD LIMIT
    # --------------------------------------------------------

    words = answer.split()

    if len(words) > 45:

        answer = " ".join(
            words[:45]
        )

        answer = answer.rstrip(
            " .,;:"
        )

        answer += "..."

    # --------------------------------------------------------
    # FINAL CLEAN
    # --------------------------------------------------------

    answer = _clean_text(
        answer
    )

    return answer


# ============================================================
# SEARCH AND READ
# ============================================================

def search_and_read(text):

    if not text or not text.strip():

        return None

    try:

        driver = _get_driver()

        # ----------------------------------------------------
        # CREATE SEARCH URL
        # ----------------------------------------------------

        search_url = (
            "https://www.bing.com/search?q="
            + quote_plus(
                text.strip()
            )
        )

        # ----------------------------------------------------
        # OPEN BING
        # ----------------------------------------------------

        driver.get(
            search_url
        )

        # ----------------------------------------------------
        # WAIT FOR RESULTS
        # ----------------------------------------------------

        try:

            WebDriverWait(
                driver,
                8
            ).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "li.b_algo"
                    )
                )
            )

        except Exception:

            pass

        # ----------------------------------------------------
        # GET RESULT
        # ----------------------------------------------------

        result = _get_bing_result(
            driver
        )

        if not result:

            return None

        # ----------------------------------------------------
        # MAKE SMALL ANSWER
        # ----------------------------------------------------

        answer = _make_small_answer(
            result
        )

        if not answer:

            return None

        return answer

    except Exception as e:

        print(
            f"[ERROR] Search error: {e}"
        )

        return None


# ============================================================
# CLOSE EDGE DRIVER
# ============================================================

def close_driver():

    global _driver

    if _driver is not None:

        try:

            _driver.quit()

        except Exception:

            pass

        _driver = None

"""
# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":


    question = "what is Python"

    print(
        "\n" + "=" * 60
    )

    print(
        f"NOVA: {question}"
    )

    result = search_and_read(
        question
    )

    if result:


        speak(
            result
        )

    else:

        print(
            "NOVA: I couldn't find enough information."
        )

        speak(
            "I couldn't find enough information."
        )

    print(
        "=" * 60
    )

    close_driver()
"""