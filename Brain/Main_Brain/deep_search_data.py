# Nova DEEP WEB SEARCH - UPDATED VERSION
#
# Pipeline:
#
#   User Query
#        ↓
#   DuckDuckGo + Brave Search
#        ↓
#   Collect Results
#        ↓
#   Normalize URLs
#        ↓
#   Remove Duplicate Sources
#        ↓
#   Rank Sources
#        ↓
#   Open Best Sources
#        ↓
#   Extract Webpage Content
#        ↓
#   Clean Content
#        ↓
#   Remove Duplicate Information
#        ↓
#   LSA Summarization
#        ↓
#   Final Nova Answer
#
# USER OUTPUT:
#   Only final answer is displayed.
#
# Nova SPEAK:
#   Only final answer is spoken.
#
# SAFETY:
#   No Google login
#   No CAPTCHA bypass
#   No verification automation
# ============================================================


import re
import time
import hashlib
import shutil

from pathlib import Path
from typing import Optional, List, Dict
from urllib.parse import quote_plus, urlparse, parse_qsl, urlencode, urlunparse

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer

from Functions.Nova_Speak.speak import speak

# ============================================================
# CONFIGURATION
# ============================================================

MAX_SEARCH_RESULTS = 10

MAX_SOURCES_TO_OPEN = 5

MAX_PAGE_CHARS = 12000

MAX_TOTAL_TEXT_CHARS = 45000

SUMMARY_SENTENCES = 7

REQUEST_TIMEOUT = 10

SELENIUM_TIMEOUT = 10

BRAVE_WAIT_TIME = 2

MIN_PARAGRAPH_LENGTH = 50

MAX_FINAL_ANSWER_CHARS = 1400

# ============================================================
# TRUSTED DOMAINS
# ============================================================

TRUSTED_DOMAINS = [
    "wikipedia.org",
    "britannica.com",
    "nasa.gov",
    "nih.gov",
    "who.int",
    "bbc.com",
    "reuters.com",
    "nature.com",
    "sciencedirect.com",
    "developer.mozilla.org",
    "python.org",
    "microsoft.com",
    "apple.com",
    "ibm.com",
    "oracle.com",
    "geeksforgeeks.com"
]


# ============================================================
# Nova DEEP SEARCH
# ============================================================

class NovaDeepSearch:

    def __init__(self, timeout: int = SELENIUM_TIMEOUT):

        self.timeout = timeout

        self.driver = None

        self.initialized = False

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0.0.0 "
                "Safari/537.36"
            )
        })

        self.init_driver()

    # ========================================================
    # EDGE DRIVER
    # ========================================================

    def init_driver(self) -> bool:

        try:

            options = Options()

            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1366,768")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")

            options.add_argument(
                "--user-agent=Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0.0.0 "
                "Safari/537.36 "
                "Edg/131.0.0.0"
            )

            driver_path = self._find_edgedriver()

            if not driver_path:
                print(
                    "[Nova] msedgedriver.exe not found."
                )

                return False

            service = Service(driver_path)

            self.driver = webdriver.Edge(
                service=service,
                options=options
            )

            self.driver.set_page_load_timeout(
                self.timeout
            )

            self.initialized = True

            return True

        except Exception as e:

            print(
                f"[Nova] Edge initialization failed: {e}"
            )

            self.driver = None
            self.initialized = False

            return False

    # ========================================================
    # FIND EDGE DRIVER
    # ========================================================

    @staticmethod
    def _find_edgedriver() -> Optional[str]:

        # ----------------------------------------------------
        # SYSTEM PATH
        # ----------------------------------------------------

        driver = shutil.which(
            "msedgedriver"
        )

        if driver:
            return driver

        # ----------------------------------------------------
        # CURRENT DIRECTORY
        # ----------------------------------------------------

        local_driver = Path(
            "msedgedriver.exe"
        )

        if local_driver.exists():
            return str(
                local_driver.resolve()
            )

        # ----------------------------------------------------
        # Nova DRIVER LOCATION
        # ----------------------------------------------------

        Nova_driver = Path(r"C:\Nova\Nova_Data\edge_driver\msedgedriver.exe"
                           )

        if Nova_driver.exists():
            return str(
                Nova_driver.resolve()
            )

        return None

    # ========================================================
    # MAIN DEEP SEARCH
    # ========================================================

    def search(
            self,
            query: str
    ) -> Optional[str]:

        if not self.initialized:
            return None

        query = query.strip()

        if not query:
            return None

        try:
            # ------------------------------------------------
            # STEP 1 - DUCKDUCKGO
            # ------------------------------------------------
            ddg_results = (
                self._duckduckgo_search(
                    query
                )
            )

            # ------------------------------------------------
            # STEP 2 - BRAVE
            # ------------------------------------------------

            brave_results = (
                self._brave_search(
                    query
                )
            )
            # ------------------------------------------------
            # STEP 3 - COMBINE
            # ------------------------------------------------

            all_results = (
                    ddg_results +
                    brave_results
            )

            if not all_results:

                return None

            # ------------------------------------------------
            # STEP 4 - REMOVE DUPLICATES
            # ------------------------------------------------

            unique_results = (
                self._remove_duplicates(
                    all_results
                )
            )
            if not unique_results:
                return None

            # ------------------------------------------------
            # STEP 5 - RANK RESULTS
            # ------------------------------------------------

            ranked_results = (
                self._rank_results(
                    query,
                    unique_results
                )
            )

            if not ranked_results:
                return None

            # ------------------------------------------------
            # STEP 6 - OPEN BEST SOURCES
            # ------------------------------------------------

            selected_sources = (
                ranked_results[
                    :MAX_SOURCES_TO_OPEN
                ]
            )
            page_contents = []

            for index, result in enumerate(
                    selected_sources,
                    start=1
            ):

                title = result.get(
                    "title",
                    "Unknown source"
                )

                url = result.get(
                    "url",
                    ""
                )

                if not url:
                    continue

                page_text = (
                    self._extract_webpage(
                        url
                    )
                )

                if page_text:
                    page_contents.append({

                        "title": title,

                        "url": url,

                        "text": page_text

                    })


            # ------------------------------------------------
            # STEP 7 - FALLBACK
            # ------------------------------------------------

            if not page_contents:

                snippets = []

                for result in ranked_results[:8]:

                    snippet = result.get(
                        "snippet",
                        ""
                    )

                    if snippet:
                        snippets.append(
                            snippet
                        )

                combined_snippets = " ".join(
                    snippets
                )

                if not combined_snippets:
                    return None

                return self._summarize(
                    query,
                    combined_snippets
                )

            # ------------------------------------------------
            # STEP 8 - COMBINE CONTENT
            # ------------------------------------------------

            combined_text = (
                self._combine_page_content(
                    page_contents
                )
            )

            if not combined_text:
                return None

            # ------------------------------------------------
            # STEP 9 - FINAL SUMMARY
            # ------------------------------------------------


            return self._summarize(
                query,
                combined_text
            )

        except Exception as e:

            print(
                f"[Nova] Deep search error: {e}"
            )

            return None

        finally:

            self.close()

    # ========================================================
    # DUCKDUCKGO SEARCH
    # ========================================================

    def _duckduckgo_search(
            self,
            query: str
    ) -> List[Dict]:

        results = []

        try:

            url = (
                    "https://html.duckduckgo.com/html/?q="
                    + quote_plus(query)
            )

            self.driver.get(url)

            try:

                WebDriverWait(
                    self.driver,
                    8
                ).until(

                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.result"
                        )
                    )
                )

            except TimeoutException:

                return results

            elements = (
                self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.result"
                )
            )

            for element in elements:

                if len(results) >= MAX_SEARCH_RESULTS:
                    break

                # ------------------------------------------------
                # TITLE + URL
                # ------------------------------------------------

                try:

                    title_element = (
                        element.find_element(
                            By.CSS_SELECTOR,
                            "a.result__a"
                        )
                    )

                    title = (
                        title_element
                        .text
                        .strip()
                    )

                    result_url = (
                        title_element
                        .get_attribute(
                            "href"
                        )
                    )

                except Exception:

                    continue

                # ------------------------------------------------
                # SNIPPET
                # ------------------------------------------------

                try:

                    snippet = (
                        element
                        .find_element(
                            By.CSS_SELECTOR,
                            ".result__snippet"
                        )
                        .text
                        .strip()
                    )

                except Exception:

                    snippet = ""

                if not title or not result_url:
                    continue

                results.append({

                    "title": title,

                    "snippet": snippet,

                    "url": result_url,

                    "engine": "DuckDuckGo"

                })

        except WebDriverException as e:

            print(
                f"[DuckDuckGo] Browser error: {e}"
            )

        except Exception as e:

            print(
                f"[DuckDuckGo] Error: {e}"
            )

        return results

    # ========================================================
    # BRAVE SEARCH
    # ========================================================

    def _brave_search(
            self,
            query: str
    ) -> List[Dict]:

        results = []

        try:

            url = (
                    "https://search.brave.com/search?q="
                    + quote_plus(query)
            )

            self.driver.get(url)

            time.sleep(
                BRAVE_WAIT_TIME
            )

            # ------------------------------------------------
            # POSSIBLE BRAVE RESULT CONTAINERS
            # ------------------------------------------------

            selectors = [

                "div.snippet",

                "div[data-type='web']",

                ".snippet",

                "article",

                "[data-testid='result']"

            ]

            elements = []

            for selector in selectors:

                try:

                    found = (
                        self.driver.find_elements(
                            By.CSS_SELECTOR,
                            selector
                        )
                    )

                    if found:
                        elements = found

                        break

                except Exception:

                    continue

            # ------------------------------------------------
            # EXTRACT RESULTS
            # ------------------------------------------------

            for element in elements:

                if len(results) >= MAX_SEARCH_RESULTS:
                    break

                try:

                    text = (
                        element
                        .text
                        .strip()
                    )

                    if len(text) < 30:
                        continue

                    links = (
                        element.find_elements(
                            By.TAG_NAME,
                            "a"
                        )
                    )

                    if not links:
                        continue

                    # Find the most useful link
                    link = None

                    for candidate in links:

                        href = (
                            candidate
                            .get_attribute(
                                "href"
                            )
                        )

                        if href and (
                                href.startswith(
                                    "http://"
                                )
                                or
                                href.startswith(
                                    "https://"
                                )
                        ):
                            link = candidate

                            break

                    if not link:
                        continue

                    title = (
                        link
                        .text
                        .strip()
                    )

                    href = (
                        link
                        .get_attribute(
                            "href"
                        )
                    )

                    if not href:
                        continue

                    if not title:
                        title = text[:150]

                    results.append({

                        "title": title,

                        "snippet": text,

                        "url": href,

                        "engine": "Brave"

                    })

                except Exception:

                    continue

            # ------------------------------------------------
            # BRAVE FALLBACK
            # ------------------------------------------------

            if not results:

                try:

                    body = (
                        self.driver
                        .find_element(
                            By.TAG_NAME,
                            "body"
                        )
                        .text
                    )

                    lines = [

                        line.strip()

                        for line
                        in body.splitlines()

                        if line.strip()

                    ]

                    for line in lines:

                        if len(results) >= MAX_SEARCH_RESULTS:
                            break

                        if len(line) < 40:
                            continue

                        results.append({

                            "title": line[:150],

                            "snippet": line,

                            "url": "",

                            "engine": "Brave"

                        })

                except Exception:

                    pass

        except WebDriverException as e:

            print(
                f"[Brave] Browser error: {e}"
            )

        except Exception as e:

            print(
                f"[Brave] Error: {e}"
            )

        return results

    # ========================================================
    # NORMALIZE URL
    # ========================================================

    @staticmethod
    def _normalize_url(
            url: str
    ) -> str:

        if not url:
            return ""

        try:

            parsed = urlparse(
                url.strip()
            )

            if parsed.scheme not in (
                    "http",
                    "https"
            ):
                return ""

            # Remove tracking parameters
            tracking_parameters = {
                "utm_source",
                "utm_medium",
                "utm_campaign",
                "utm_term",
                "utm_content",
                "gclid",
                "fbclid",
                "ref",
            }

            query_items = []

            for key, value in parse_qsl(
                    parsed.query,
                    keep_blank_values=True
            ):

                if key.lower() not in tracking_parameters:
                    query_items.append(
                        (key, value)
                    )

            clean_query = urlencode(
                query_items
            )

            normalized = urlunparse((
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path.rstrip("/"),
                "",
                clean_query,
                ""
            ))

            return normalized

        except Exception:

            return url.strip().lower()

    # ========================================================
    # REMOVE DUPLICATE SOURCES
    # ========================================================

    @classmethod
    def _remove_duplicates(
            cls,
            results: List[Dict]
    ) -> List[Dict]:

        unique = []

        seen_urls = set()

        seen_titles = set()

        for result in results:

            raw_url = result.get(
                "url",
                ""
            )

            raw_title = result.get(
                "title",
                ""
            )

            clean_url = cls._normalize_url(
                raw_url
            )

            title = (
                raw_title
                .strip()
                .lower()
            )

            title_key = re.sub(
                r"\W+",
                " ",
                title
            ).strip()

            # ------------------------------------------------
            # URL DUPLICATE
            # ------------------------------------------------

            if clean_url:

                if clean_url in seen_urls:
                    continue

                seen_urls.add(
                    clean_url
                )

            # ------------------------------------------------
            # TITLE DUPLICATE
            # ------------------------------------------------

            if title_key:

                if title_key in seen_titles:
                    continue

                seen_titles.add(
                    title_key
                )

            # Save normalized URL
            result["url"] = clean_url

            unique.append(
                result
            )

        return unique

    # ========================================================
    # RANK RESULTS
    # ========================================================

    @staticmethod
    def _rank_results(
            query: str,
            results: List[Dict]
    ) -> List[Dict]:

        query_words = set(

            word.lower()

            for word in re.findall(
                r"\b[a-zA-Z]{3,}\b",
                query
            )

        )

        scored = []

        for result in results:

            title = result.get(
                "title",
                ""
            )

            snippet = result.get(
                "snippet",
                ""
            )

            url = result.get(
                "url",
                ""
            ).lower()

            title_lower = title.lower()

            snippet_lower = snippet.lower()

            score = 0

            # ------------------------------------------------
            # QUERY MATCHING
            # ------------------------------------------------

            for word in query_words:

                if word in title_lower:
                    score += 5

                if word in snippet_lower:
                    score += 2

            # ------------------------------------------------
            # EXACT QUERY PHRASE
            # ------------------------------------------------

            query_lower = query.lower()

            if query_lower in title_lower:

                score += 8

            elif query_lower in snippet_lower:

                score += 4

            # ------------------------------------------------
            # TRUSTED DOMAIN
            # ------------------------------------------------

            for domain in TRUSTED_DOMAINS:

                if domain in url:
                    score += 5

                    break

            # ------------------------------------------------
            # HAS GOOD SNIPPET
            # ------------------------------------------------

            if len(snippet) > 100:
                score += 2

            # ------------------------------------------------
            # HAS URL
            # ------------------------------------------------

            if url:
                score += 1

            # ------------------------------------------------
            # SEARCH ENGINE BALANCE
            # ------------------------------------------------

            if result.get(
                    "engine"
            ) == "DuckDuckGo":
                score += 1

            scored.append(
                (
                    score,
                    result
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [

            result

            for score, result
            in scored

        ]

    # ========================================================
    # EXTRACT WEBPAGE
    # ========================================================

    def _extract_webpage(
            self,
            url: str
    ) -> Optional[str]:

        if not url:
            return None

        try:

            parsed = urlparse(
                url
            )

            if parsed.scheme not in (
                    "http",
                    "https"
            ):
                return None

            response = self.session.get(
                url,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code != 200:
                return None

            content_type = (
                response
                .headers
                .get(
                    "Content-Type",
                    ""
                )
                .lower()
            )

            if "text/html" not in content_type:
                return None

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # ------------------------------------------------
            # REMOVE USELESS ELEMENTS
            # ------------------------------------------------

            for tag in soup([

                "script",
                "style",
                "noscript",
                "svg",
                "nav",
                "footer",
                "header",
                "aside",
                "form",
                "iframe",
                "button",
                "input",
                "select",
                "textarea"

            ]):
                tag.decompose()

            # ------------------------------------------------
            # FIND MAIN CONTENT
            # ------------------------------------------------

            content = (

                    soup.find("article")

                    or

                    soup.find("main")

                    or

                    soup.find(
                        "div",
                        {
                            "role": "main"
                        }
                    )

                    or

                    soup.body

            )

            if not content:
                return None

            # ------------------------------------------------
            # EXTRACT PARAGRAPHS
            # ------------------------------------------------

            paragraphs = []

            for paragraph in content.find_all(
                    "p"
            ):

                text = (
                    paragraph
                    .get_text(
                        " ",
                        strip=True
                    )
                )

                text = self._clean_text(
                    text
                )

                if len(text) >= MIN_PARAGRAPH_LENGTH:
                    paragraphs.append(
                        text
                    )

            if not paragraphs:
                return None

            # ------------------------------------------------
            # REMOVE DUPLICATE PARAGRAPHS
            # ------------------------------------------------

            paragraphs = (
                self._remove_text_duplicates(
                    paragraphs
                )
            )

            text = " ".join(
                paragraphs
            )

            if len(text) > MAX_PAGE_CHARS:
                text = text[
                    :MAX_PAGE_CHARS
                ]

            return text.strip()

        except requests.RequestException as e:

            print(
                f"[PAGE] Request failed: "
                f"{url[:60]} - {e}"
            )

            return None

        except Exception as e:

            print(
                f"[PAGE] Extraction failed: "
                f"{url[:60]} - {e}"
            )

            return None

    # ========================================================
    # CLEAN WEBPAGE TEXT
    # ========================================================

    @staticmethod
    def _fix_encoding(text: str) -> str:

        if not text:
            return ""

        replacements = {
            "â€™": "’",
            "â€˜": "‘",
            "â€œ": "“",
            "â€": "”",
            "â€“": "–",
            "â€”": "—",
            "â€¦": "…",
            "Â": "",
            "â": "’",
            "â": "–",
            "â": "—",
            "â¦": "…",
        }

        for bad, good in replacements.items():
            text = text.replace(bad, good)

        if any(marker in text for marker in ("Ã", "Â", "â")):
            try:
                repaired = text.encode("latin1").decode("utf-8")
                if repaired.count("�") <= text.count("�"):
                    text = repaired
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

        return text

    @staticmethod
    def _clean_text(text: str) -> str:

        if not text:
            return ""

        text = NovaDeepSearch._fix_encoding(text)

        text = re.sub(
            r"https?://\S+|www\.\S+",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\[\s*\d+(?:\s*[,;-]\s*\d+)*\s*\]",
            "",
            text
        )

        # Remove common mathematical/markup artifacts without destroying
        # ordinary text.
        text = re.sub(r"\{\s*\\displaystyle\s*", "", text)
        text = re.sub(r"\\(?:mathbf|mathrm|text|operatorname)\s*", "", text)
        text = re.sub(r"[{}]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        noise_patterns = [
            r"cookie policy",
            r"privacy policy",
            r"terms of service",
            r"accept cookies",
            r"subscribe",
            r"sign in",
            r"log in",
            r"advertisement",
            r"all rights reserved",
            r"enable javascript",
            r"javascript",
            r"geeksforgeeks",
        ]

        for pattern in noise_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        return re.sub(r"\s+", " ", text).strip()

    # ========================================================
    # REMOVE DUPLICATE TEXT
    # ========================================================

    @staticmethod
    def _remove_text_duplicates(
            paragraphs: List[str]
    ) -> List[str]:

        unique = []

        seen = set()

        for paragraph in paragraphs:

            normalized = re.sub(
                r"\W+",
                " ",
                paragraph.lower()
            ).strip()

            if not normalized:
                continue

            fingerprint = hashlib.md5(
                normalized.encode(
                    "utf-8"
                )
            ).hexdigest()

            if fingerprint in seen:
                continue

            seen.add(
                fingerprint
            )

            unique.append(
                paragraph
            )

        return unique

    # ========================================================
    # COMBINE PAGE CONTENT
    # ========================================================

    @staticmethod
    def _combine_page_content(
            pages: List[Dict]
    ) -> str:

        sections = []

        for page in pages:

            title = page.get(
                "title",
                ""
            )

            text = page.get(
                "text",
                ""
            )

            if not text:
                continue

            if title:

                sections.append(
                    f"{title}. {text}"
                )

            else:

                sections.append(
                    text
                )

        combined = "\n".join(
            sections
        )

        if len(combined) > MAX_TOTAL_TEXT_CHARS:
            combined = combined[
                :MAX_TOTAL_TEXT_CHARS
            ]

        return combined.strip()

    # ========================================================
    # SUMMARIZE
    # ========================================================

    @staticmethod
    def _summarize(query: str, text: str) -> str:

        if not text:
            return "I couldn't find enough information to answer that."

        text = NovaDeepSearch._fix_encoding(text)
        text = re.sub(r"\s+", " ", text).strip()

        # Remove source citation artifacts and common promotional language
        # before sentence selection.
        text = re.sub(
            r"\[\s*\d+(?:\s*[,;-]\s*\d+)*\s*]",
            "",
            text
        )

        sentences = re.split(r"(?<=[.!?])\s+", text)
        query_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", query.lower())
        )

        promotional_patterns = (
            "learn more",
            "consider enrolling",
            "with this certificate",
            "you can read",
            "free programming tutorials",
            "sign up",
            "subscribe to",
            "start learning today",
        )

        candidates = []
        seen = set()

        for sentence in sentences:
            sentence = NovaDeepSearch._clean_text(sentence).strip(" -")

            if len(sentence) < 45:
                continue

            lower = sentence.lower()

            if any(pattern in lower for pattern in promotional_patterns):
                continue

            normalized = re.sub(r"\W+", " ", lower).strip()
            if not normalized or normalized in seen:
                continue

            # Skip obvious navigation/source-heading fragments.
            if lower in {"key takeaways", "introduction", "references", "contents"}:
                continue

            seen.add(normalized)

            words = set(re.findall(r"\b[a-zA-Z]{3,}\b", lower))
            relevance = len(query_words & words)

            if lower.startswith(("according to", "learn more", "read more")):
                relevance -= 2

            candidates.append((relevance, len(sentence), sentence))

        if not candidates:
            return (
                "I found information about "
                f"{query}, but the sources did not contain enough clear information."
            )

        # LSA remains useful for choosing source material, but it is no longer
        # trusted as the final output because it can join unrelated sentences.
        lsa_sentences = []
        try:
            cleaned_text = " ".join(item[2] for item in candidates)
            parser = PlaintextParser.from_string(
                cleaned_text,
                Tokenizer("english")
            )
            summary = LsaSummarizer()(
                parser.document,
                min(SUMMARY_SENTENCES, max(3, len(candidates)))
            )
            lsa_sentences = [
                NovaDeepSearch._clean_text(str(sentence))
                for sentence in summary
            ]
        except Exception as e:
            print(f"[SUMMARIZER] LSA failed: {e}")

        # Prefer LSA-selected sentences, then fill gaps with the most relevant
        # source sentences. Preserve source order where possible.
        selected = []
        selected_norm = set()

        def add_sentence(sentence):
            sentence = NovaDeepSearch._clean_text(sentence).strip()
            norm = re.sub(r"\W+", " ", sentence.lower()).strip()
            if len(sentence) < 45 or not norm or norm in selected_norm:
                return False
            selected.append(sentence)
            selected_norm.add(norm)
            return True

        for sentence in lsa_sentences:
            add_sentence(sentence)
            if len(selected) >= 6:
                break

        ranked_candidates = sorted(
            candidates,
            key=lambda item: (item[0], min(item[1], 240)),
            reverse=True
        )

        for _, _, sentence in ranked_candidates:
            add_sentence(sentence)
            if len(selected) >= 6:
                break

        # Put the strongest definition/explanation first when one exists.
        definition_terms = tuple(
            word for word in re.findall(r"\b[a-zA-Z]{3,}\b", query.lower())
        )

        def definition_score(sentence):
            lower = sentence.lower()
            score = sum(term in lower for term in definition_terms)
            if any(phrase in lower for phrase in (
                "is a ", "is an ", "refers to ", "is defined as ",
                "is the process of ", "is the study of "
            )):
                score += 3
            return score

        selected.sort(key=definition_score, reverse=True)

        answer = " ".join(selected)
        answer = NovaDeepSearch._clean_text(answer)

        # Remove repeated adjacent wording and finish only at a complete sentence.
        if len(answer) > MAX_FINAL_ANSWER_CHARS:
            answer = answer[:MAX_FINAL_ANSWER_CHARS]
            boundary = max(
                answer.rfind(". "),
                answer.rfind("! "),
                answer.rfind("? ")
            )
            if boundary >= 700:
                answer = answer[:boundary + 1]
            else:
                last_space = answer.rfind(" ")
                if last_space > 700:
                    answer = answer[:last_space].rstrip(" ,;:") + "."

        return answer.strip()

    # ========================================================
    # CLOSE BROWSER
    # ========================================================

    def close(self):

        try:

            if self.driver:
                self.driver.quit()

                self.driver = None

        except Exception:

            pass

        try:

            self.session.close()

        except Exception:

            pass


# ============================================================
# Nova SEARCH FUNCTION
# ============================================================

def Nova_search(
        query: str
) -> bool:
    if not query or not query.strip():
        speak(
            "Please tell me what you want "
            "me to search for."
        )

        return False

    query = query.strip()


    search_engine = NovaDeepSearch(
        timeout=SELENIUM_TIMEOUT
    )

    if not search_engine.initialized:
        speak(
            "I couldn't start the web search."
        )

        return False

    result = search_engine.search(
        query
    )

    if not result:
        print(
            "[Nova] No useful information found."
        )

        speak(
            "I couldn't find enough "
            "information to answer that."
        )

        return False
    # ========================================================
    # SPEAK ONLY FINAL ANSWER
    # ========================================================
    speak(
        result
    )

    return True


# ============================================================
# COMMAND PROCESSOR
# ============================================================

def process_web_search(
        text: str
) -> bool:
    if not text:
        return False

    text_lower = (
        text.lower()
        .strip()
    )

    # --------------------------------------------------------
    # LONGER PHRASES FIRST
    # --------------------------------------------------------

    keywords = [
        "depth",
        "deep search",
        "search for",
        "look for",
        "look up",
        "research",
        "search",
        "find",
        "duckduckgo",
        "brave"

    ]

    detected = None

    for keyword in keywords:

        if text_lower.startswith(
                keyword
        ):
            detected = keyword

            break

    if not detected:
        return False

    # --------------------------------------------------------
    # EXTRACT QUERY
    # --------------------------------------------------------

    query = text[
        len(detected):
    ].strip()

    if not query:
        speak(
            "What would you like me "
            "to search for?"
        )

        return True

    return Nova_search(
        query
    )


"""
# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    Nova_search("what is Marvals in depth")
"""
