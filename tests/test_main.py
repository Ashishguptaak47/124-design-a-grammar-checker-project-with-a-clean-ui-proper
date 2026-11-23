import unittest
from grammar_checker.engine import GrammarEngine, IssueType


class TestGrammarEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GrammarEngine()

    def test_repeated_words(self):
        text = "This is the the test sentence."
        issues = self.engine.check(text)
        repeated_issues = [i for i in issues if "Repeated word" in i.message]
        self.assertEqual(len(repeated_issues), 1)
        self.assertEqual(repeated_issues[0].original, "the the")
        self.assertEqual(repeated_issues[0].suggestions, ["the"])

    def test_capitalization(self):
        text = "i am happy. python is great."
        issues = self.engine.check(text)
        cap_issues = [i for i in issues if "capital" in i.message.lower() or "pronoun" in i.message.lower()]
        self.assertTrue(len(cap_issues) >= 2)

    def test_articles(self):
        text = "She ate a apple and an banana."
        issues = self.engine.check(text)
        article_issues = [i for i in issues if "vowel" in i.message or "consonant" in i.message]
        self.assertEqual(len(article_issues), 2)

    def test_phrases(self):
        text = "You could of done it better."
        issues = self.engine.check(text)
        phrase_issues = [i for i in issues if "could have" in i.suggestions]
        self.assertEqual(len(phrase_issues), 1)

    def test_passive_voice(self):
        text = "The project was completed yesterday."
        issues = self.engine.check(text)
        passive_issues = [i for i in issues if i.issue_type == IssueType.STYLE]
        self.assertEqual(len(passive_issues), 1)

    def test_readability_stats(self):
        text = "This is a simple sentence. It is easy to read."
        stats = self.engine.calculate_stats(text)
        self.assertEqual(stats["words"], 10)
        self.assertEqual(stats["sentences"], 2)
        self.assertGreater(stats["readability"], 50.0)


if __name__ == "__main__":
    unittest.main()
