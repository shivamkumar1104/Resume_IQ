"""Resume contact and basic structure extractor.

Extracts:
- Name
- Email
- Phone
- LinkedIn
- GitHub
- Portfolio / personal website
- Resume sections
- Estimated experience
- Project count
"""

import re
import datetime
from typing import Dict, Optional, List

import spacy


# ---------------------------------------------------------------------
# SpaCy model
# ---------------------------------------------------------------------

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = spacy.blank("en")


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

_SECTION_HEADERS = [
    "summary",
    "professional summary",
    "objective",
    "profile",

    "experience",
    "work experience",
    "professional experience",
    "employment",
    "work history",

    "education",
    "academic background",

    "skills",
    "technical skills",
    "core competencies",
    "tech stack",

    "projects",
    "personal projects",
    "key projects",

    "certifications",
    "certificates",

    "achievements",
    "awards",

    "publications",

    "languages",
    "interests",
]


# Common portfolio hosting platforms.
PORTFOLIO_HOSTS = (
    "vercel.app",
    "netlify.app",
    "github.io",
    "pages.dev",
    "web.app",
    "firebaseapp.com",
)


# ---------------------------------------------------------------------
# URL extraction
# ---------------------------------------------------------------------

URL_PATTERN = re.compile(
    r"""
    (?:
        https?://
    )?
    (?:
        www\.
    )?
    [a-zA-Z0-9-]+
    (?:
        \.[a-zA-Z0-9-]+
    )+
    (?:
        /[^\s<>()\[\]]*
    )?
    """,
    re.VERBOSE | re.IGNORECASE,
)


def normalize_url(url: str) -> str:
    """Clean and normalize an extracted URL."""

    url = url.strip()
    url = url.rstrip(".,;:!?)]}\"'")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from resume text."""

    matches = URL_PATTERN.findall(text)

    urls = []

    for url in matches:
        normalized = normalize_url(url)

        if normalized not in urls:
            urls.append(normalized)

    return urls


# ---------------------------------------------------------------------
# Contact extraction
# ---------------------------------------------------------------------

def extract_contact_info(
    text: str,
) -> Dict[str, Optional[str]]:
    """
    Extract contact information from resume text.

    Returns:
        name
        email
        phone
        linkedin
        github
        portfolio
    """

    name = None
    email = None
    phone = None
    linkedin = None
    github = None
    portfolio = None

    # -------------------------------------------------------------
    # Email
    # -------------------------------------------------------------

    email_match = re.search(
        r"\b[a-zA-Z0-9._%+\-]+"
        r"@[a-zA-Z0-9.\-]+\."
        r"[a-zA-Z]{2,}\b",
        text,
        re.IGNORECASE,
    )

    if email_match:
        email = email_match.group(0).strip()


    # -------------------------------------------------------------
    # Phone
    # -------------------------------------------------------------

    phone_patterns = [
        r"\+?\d{1,3}[\s.-]?\(?\d{2,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}",
        r"\b\d{10}\b",
    ]

    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)

        if phone_match:
            phone = phone_match.group(0).strip()
            break


    # -------------------------------------------------------------
    # Extract URLs
    # -------------------------------------------------------------

    urls = extract_urls(text)


    # -------------------------------------------------------------
    # Identify LinkedIn / GitHub / Portfolio
    # -------------------------------------------------------------

    for url in urls:

        lower_url = url.lower()

        # LinkedIn
        if "linkedin.com/in/" in lower_url:
            linkedin = url
            continue

        # GitHub
        if "github.com/" in lower_url:
            github = url
            continue

        # Known portfolio hosting platforms
        if any(host in lower_url for host in PORTFOLIO_HOSTS):
            if portfolio is None:
                portfolio = url
            continue

        # Generic personal website
        #
        # We don't assume every unknown domain is a portfolio.
        # However, if it is not LinkedIn/GitHub and looks like a
        # personal domain, consider it a portfolio candidate.
        if portfolio is None:
            portfolio = url


    # -------------------------------------------------------------
    # SpaCy NER name extraction
    # -------------------------------------------------------------

    header_text = text[:1000]

    doc = nlp(header_text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            candidate = ent.text.strip()

            words = candidate.split()

            if 2 <= len(words) <= 4:
                name = candidate
                break


    # -------------------------------------------------------------
    # Name fallback
    # -------------------------------------------------------------

    if not name:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        # Usually the candidate's name is near the top.
        for line in lines[:10]:

            # Remove common labels.
            cleaned = re.sub(
                r"^(name|resume|cv)\s*[:\-]\s*",
                "",
                line,
                flags=re.IGNORECASE,
            ).strip()

            # Basic name pattern.
            if re.fullmatch(
                r"[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3}",
                cleaned,
            ):
                name = cleaned
                break


    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
    }


# ---------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------

def detect_sections(text: str) -> Dict[str, bool]:
    """
    Detect standard resume sections.

    Uses line-based matching to reduce false positives.
    """

    detected = {
        header: False
        for header in _SECTION_HEADERS
    }

    lines = [
        re.sub(r"[^a-zA-Z\s]", "", line).strip().lower()
        for line in text.splitlines()
    ]

    normalized_lines = {
        re.sub(r"\s+", " ", line)
        for line in lines
        if line
    }

    for header in _SECTION_HEADERS:

        normalized_header = re.sub(
            r"\s+",
            " ",
            header.lower(),
        )

        if normalized_header in normalized_lines:
            detected[header] = True

    return detected


# ---------------------------------------------------------------------
# Experience calculation
# ---------------------------------------------------------------------

MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def _parse_date(value: str) -> Optional[datetime.date]:
    """Parse common resume date formats."""

    value = value.strip().lower()

    # Present / current
    if value in {"present", "current", "now"}:
        today = datetime.date.today()
        return datetime.date(today.year, today.month, 1)

    # Month + year
    month_year = re.fullmatch(
        r"([a-z]+)\.?\s+(\d{4})",
        value,
    )

    if month_year:

        month_name = month_year.group(1)
        year = int(month_year.group(2))

        month = MONTHS.get(month_name)

        if month:
            return datetime.date(year, month, 1)

    # Year only
    if re.fullmatch(r"\d{4}", value):

        year = int(value)

        return datetime.date(year, 1, 1)

    return None


def extract_experience_years(text: str) -> float:
    """
    Estimate total experience from date ranges.

    Supports:
        2021 - 2024
        Jan 2021 - Mar 2024
        January 2022 - Present
    """

    date_pattern = re.compile(
        r"""
        (
            (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|
            Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|
            Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|
            Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{4}
            |
            \d{4}
        )
        \s*[-–—]\s*
        (
            (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|
            Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|
            Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|
            Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{4}
            |
            \d{4}
            |
            present
            |
            current
            |
            now
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    intervals = []

    for match in date_pattern.finditer(text):

        start = _parse_date(match.group(1))
        end = _parse_date(match.group(2))

        if not start or not end:
            continue

        if end < start:
            continue

        intervals.append((start, end))


    # Remove duplicate intervals
    intervals = list(set(intervals))

    if not intervals:
        return 0.0


    # Merge overlapping employment periods.
    intervals.sort()

    merged = []

    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:

        if start <= current_end:

            if end > current_end:
                current_end = end

        else:

            merged.append(
                (current_start, current_end)
            )

            current_start = start
            current_end = end

    merged.append((current_start, current_end))


    # Calculate total months
    total_months = 0

    for start, end in merged:

        months = (
            (end.year - start.year) * 12
            + (end.month - start.month)
            + 1
        )

        total_months += max(months, 0)


    return round(total_months / 12, 1)


# ---------------------------------------------------------------------
# Project counting
# ---------------------------------------------------------------------

def count_projects(text: str) -> int:
    """
    Estimate number of projects in the resume.

    Uses the Projects section and project-like headings.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    project_section_start = None
    project_section_end = None

    # -------------------------------------------------------------
    # Find Projects section
    # -------------------------------------------------------------

    section_pattern = re.compile(
        r"^(projects?|personal projects|key projects)$",
        re.IGNORECASE,
    )

    for index, line in enumerate(lines):

        cleaned = re.sub(
            r"[^a-zA-Z\s]",
            "",
            line,
        ).strip()

        if section_pattern.match(cleaned):

            project_section_start = index
            break


    if project_section_start is None:
        return 0


    # -------------------------------------------------------------
    # Find next major section
    # -------------------------------------------------------------

    major_sections = {
        "experience",
        "work experience",
        "education",
        "skills",
        "technical skills",
        "certifications",
        "achievements",
        "awards",
        "publications",
        "languages",
        "interests",
    }

    for index in range(
        project_section_start + 1,
        len(lines),
    ):

        cleaned = re.sub(
            r"[^a-zA-Z\s]",
            "",
            lines[index],
        ).strip().lower()

        if cleaned in major_sections:

            project_section_end = index
            break


    if project_section_end is None:
        project_section_end = len(lines)


    project_lines = lines[
        project_section_start + 1:
        project_section_end
    ]


    # -------------------------------------------------------------
    # Detect project headings
    # -------------------------------------------------------------

    project_count = 0

    for line in project_lines:

        # Example:
        # Resume Analyzer
        # AI Resume Parser
        # E-Commerce Platform

        if re.match(
            r"^[A-Z][A-Za-z0-9&\-\s]{2,60}"
            r"(?:\s*\|.*)?$",
            line,
        ):

            # Ignore bullet points
            if not line.startswith(("-", "•", "*")):
                project_count += 1


    # -------------------------------------------------------------
    # Fallback: project numbers
    # -------------------------------------------------------------

    numbered_projects = re.findall(
        r"\bproject\s*\d+\b",
        "\n".join(project_lines),
        re.IGNORECASE,
    )

    project_count = max(
        project_count,
        len(numbered_projects),
    )


    return min(project_count, 20)