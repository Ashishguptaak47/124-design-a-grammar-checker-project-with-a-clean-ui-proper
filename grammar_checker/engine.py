import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class IssueType(Enum):
    SPELLING = "Spelling"
    GRAMMAR = "Grammar"
    PUNCTUATION = "Punctuation"
    STYLE = "Style"


@dataclass
class Issue:
    issue_type: IssueType
    message: str
    start: int
    end: int
    original: str
    suggestions: List[str]


class GrammarEngine:
    """Rule-based grammar, style, and spell checking engine."""

    # Common phrase corrections
    PHRASE_REPLACEMENTS = {
        r"\bcould of\b": ("could have", IssueType.GRAMMAR, "Did you mean 'could have'?"),
        r"\bshould of\b": ("should have", IssueType.GRAMMAR, "Did you mean 'should have'?"),
        r"\bwould of\b": ("would have", IssueType.GRAMMAR, "Did you mean 'would have'?"),
        r"\byour welcome\b": ("you're welcome", IssueType.GRAMMAR, "'your' indicates possession; use 'you're'."),
        r"\btheir going\b": ("they're going", IssueType.GRAMMAR, "'their' indicates possession; use 'they're'."),
        r"\bthere car\b": ("their car", IssueType.GRAMMAR, "Use 'their' for possession."),
        r"\balot\b": ("a lot", IssueType.SPELLING, "'alot' is not a standard word. Use 'a lot'."),
        r"\birregardless\b": ("regardless", IssueType.STYLE, "'irregardless' is non-standard. Use 'regardless'."),
    }

    # Basic English dictionary for spell check
    COMMON_WORDS = {
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on",
        "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we",
        "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their",
        "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
        "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into",
        "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now",
        "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two",
        "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any",
        "these", "give", "day", "most", "us", "is", "are", "was", "were", "been", "has", "had",
        "grammar", "checker", "spelling", "text", "sentence", "project", "python", "engine"
    }

    def __init__(self):
        pass

    def check(self, text: str) -> List[Issue]:
        """Analyze text and return a list of identified issues."""
        if not text:
            return []

        issues: List[Issue] = []
        issues.extend(self._check_repeated_words(text))
        issues.extend(self._check_capitalization(text))
        issues.extend(self._check_punctuation(text))
        issues.extend(self._check_articles(text))
        issues.extend(self._check_phrases(text))
        issues.extend(self._check_passive_voice(text))
        issues.extend(self._check_spelling(text))

        # Sort issues by start position
        issues.sort(key=lambda x: x.start)
        return issues

    def _check_repeated_words(self, text: str) -> List[Issue]:
        issues = []
        pattern = re.compile(r"\b([a-zA-Z]+)\s+\1\b", re.IGNORECASE)
        for match in pattern.finditer(text):
            word = match.group(1)
            issues.append(Issue(
                issue_type=IssueType.GRAMMAR,
                message=f"Repeated word '{word}'.",
                start=match.start(),
                end=match.end(),
                original=match.group(0),
                suggestions=[word]
            ))
        return issues

    def _check_capitalization(self, text: str) -> List[Issue]:
        issues = []
        # Lowercase 'i' standalone
        for match in re.finditer(r"\b(i)\b", text):
            issues.append(Issue(
                issue_type=IssueType.GRAMMAR,
                message="Pronoun 'I' should be capitalized.",
                start=match.start(),
                end=match.end(),
                original=match.group(1),
                suggestions=["I"]
            ))

        # Start of sentence capitalization
        sentence_start_pattern = re.compile(r"(?:^|[\.!\?]\s+)([a-z])")
        for match in sentence_start_pattern.finditer(text):
            char_idx = match.start(1)
            original_char = match.group(1)
            issues.append(Issue(
                issue_type=IssueType.GRAMMAR,
                message="Sentence should start with a capital letter.",
                start=char_idx,
                end=char_idx + 1,
                original=original_char,
                suggestions=[original_char.upper()]
            ))
        return issues

    def _check_punctuation(self, text: str) -> List[Issue]:
        issues = []
        # Missing space after comma/period/exclamation/question mark followed by a letter
        pattern = re.compile(r"([,\.!\?])([a-zA-Z])")
        for match in pattern.finditer(text):
            punc, char = match.group(1), match.group(2)
            issues.append(Issue(
                issue_type=IssueType.PUNCTUATION,
                message=f"Missing space after '{punc}'.",
                start=match.start(),
                end=match.end(),
                original=match.group(0),
                suggestions=[f"{punc} {char}"]
            ))
        return issues

    def _check_articles(self, text: str) -> List[Issue]:
        issues = []
        # 'a' before vowel sound heuristic
        pattern_a = re.compile(r"\b(a)\s+([aeiouAEIOU]\w+)\b")
        for match in pattern_a.finditer(text):
            word = match.group(2)
            issues.append(Issue(
                issue_type=IssueType.GRAMMAR,
                message=f"Use 'an' before words starting with a vowel sound.",
                start=match.start(),
                end=match.end(),
                original=match.group(0),
                suggestions=[f"an {word}"]
            ))

        # 'an' before consonant sound heuristic
        pattern_an = re.compile(r"\b(an)\s+([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]\w+)\b")
        for match in pattern_an.finditer(text):
            word = match.group(2)
            # Exception heuristic (e.g., 'hour', 'honest')
            if word.lower() in ["hour", "hours", "honest", "honor", "heir"]:
                continue
            issues.append(Issue(
                issue_type=IssueType.GRAMMAR,
                message=f"Use 'a' before words starting with a consonant sound.",
                start=match.start(),
                end=match.end(),
                original=match.group(0),
                suggestions=[f"a {word}"]
            ))
        return issues

    def _check_phrases(self, text: str) -> List[Issue]:
        issues = []
        for pattern_str, (replacement, issue_type, msg) in self.PHRASE_REPLACEMENTS.items():
            for match in re.finditer(pattern_str, text, re.IGNORECASE):
                issues.append(Issue(
                    issue_type=issue_type,
                    message=msg,
                    start=match.start(),
                    end=match.end(),
                    original=match.group(0),
                    suggestions=[replacement]
                ))
        return issues

    def _check_passive_voice(self, text: str) -> List[Issue]:
        issues = []
        # Simple heuristic: be-verb + word ending in 'ed'
        pattern = re.compile(r"\b(am|is|are|was|were|be|been|being)\s+(\w+ed)\b", re.IGNORECASE)
        for match in pattern.finditer(text):
            issues.append(Issue(
                issue_type=IssueType.STYLE,
                message="Passive voice detected. Consider active voice for clearer writing.",
                start=match.start(),
                end=match.end(),
                original=match.group(0),
                suggestions=[]
            ))
        return issues

    def _check_spelling(self, text: str) -> List[Issue]:
        issues = []
        words = re.finditer(r"\b[a-zA-Z]{3,}\b", text)
        for match in words:
            word = match.group(0)
            word_lower = word.lower()
            if word_lower not in self.COMMON_WORDS and not word.istitle():
                # Generate close candidates using simple edit distance
                suggestions = self._get_spelling_suggestions(word_lower)
                if suggestions:
                    issues.append(Issue(
                        issue_type=IssueType.SPELLING,
                        message=f"Possible spelling mistake: '{word}'.",
                        start=match.start(),
                        end=match.end(),
                        original=word,
                        suggestions=suggestions
                    ))
        return issues

    def _get_spelling_suggestions(self, word: str) -> List[str]:
        matches = []
        for cand in self.COMMON_WORDS:
            if abs(len(cand) - len(word)) <= 1:
                if self._levenshtein_distance(word, cand) <= 1:
                    matches.append(cand)
        return matches[:3]

    @staticmethod
    def _levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return GrammarEngine._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def calculate_stats(self, text: str) -> dict:
        """Calculate text statistics and readability score."""
        if not text.strip():
            return {"words": 0, "chars": 0, "sentences": 0, "readability": 100.0}

        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)
        char_count = len(text)
        sentences = [s for s in re.split(r"[\.\?!]+", text) if s.strip()]
        sentence_count = max(1, len(sentences))

        # Syllables estimation heuristic
        syllable_count = 0
        for w in words:
            syllables = len(re.findall(r"[aeiouyAEIOUY]+", w))
            syllable_count += max(1, syllables)

        # Flesch Reading Ease score formula
        if word_count > 0:
            score = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
            score = max(0.0, min(100.0, round(score, 1)))
        else:
            score = 100.0

        return {
            "words": word_count,
            "chars": char_count,
            "sentences": sentence_count,
            "readability": score
        }
