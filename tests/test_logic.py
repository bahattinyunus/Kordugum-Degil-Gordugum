"""
Kördüğüm Değil Gördüğüm — Logic of Unity Birim Testleri.
"""

import unittest
import sys
import os

# Logic-of-Unity klasörünü path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Logic-of-Unity"))

from bias_detector import detect_bias
from empathy_generator import generate_empathy
from unity_analyzer import analyze_unity
from wisdom_recommender import recommend_wisdom, get_all_sages


class TestBiasDetector(unittest.TestCase):
    def test_clean_text(self):
        result = detect_bias("Gelin tanış olalım, sevelim sevilelim.")
        self.assertEqual(result["status"], "TEMİZ")
        self.assertEqual(result["score"], 0)
        self.assertEqual(len(result["found"]), 0)

    def test_toxic_text_detection(self):
        result = detect_bias("Barbarlar ve yabancılar burada istenmiyor, defolun!")
        self.assertIn(result["status"], ["DİKKAT", "YÜKSEK ÖNYARGI"])
        self.assertGreater(result["score"], 0)
        self.assertTrue(any("barbar" in f.lower() for f in result["found"]))

    def test_english_bias_detection(self):
        result = detect_bias("They are uncivilized savages, get out!")
        self.assertGreater(result["score"], 0)
        self.assertIn("uncivilized", [f.lower() for f in result["found"]])

    def test_empty_input(self):
        result = detect_bias("")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["status"], "TEMİZ")


class TestEmpathyGenerator(unittest.TestCase):
    def test_turkish_plural_transformation(self):
        result = generate_empathy("Yabancılar buraya gelmesin.")
        # 'yabancılar' -> 'misafirler' dönüşmeli ('misafirlar' DEĞİL)
        self.assertIn("misafirler", result["transformed"].lower())
        self.assertTrue(result["changed"])

    def test_toxic_verb_transformation(self):
        result = generate_empathy("Biz onlardan nefret ediyoruz.")
        self.assertTrue(result["changed"])
        self.assertNotIn("nefret ediyoruz", result["transformed"].lower())

    def test_english_transformation(self):
        result = generate_empathy("Those people are inferior.")
        self.assertTrue(result["changed"])

    def test_already_peaceful_text(self):
        result = generate_empathy("Dünya hepimizin ortak yuvasıdır.")
        self.assertFalse(result["changed"])


class TestUnityAnalyzer(unittest.TestCase):
    def test_high_unity_text(self):
        text = "Biz sevgiyle, dostlukla ve bütün canlarla barış içinde bir dünya kuracağız. Soframızı paylaşırız."
        result = analyze_unity(text)
        self.assertGreaterEqual(result["unity_score"], 80)
        self.assertEqual(result["level"], "Gönül Güneşi")
        self.assertGreaterEqual(result["bridge_diversity"], 4)

    def test_zero_unity_text(self):
        result = analyze_unity("Masa lambası çalışmıyor.")
        self.assertEqual(result["unity_score"], 0)
        self.assertEqual(result["level"], "Toprak Bekliyor")

    def test_multilingual_bridges(self):
        result = analyze_unity("Peace, love, unity and solidarity for everyone.")
        self.assertGreater(result["unity_score"], 40)
        self.assertIn("Barış & Adalet", result["bridges"])
        self.assertIn("Sevgi & Muhabbet", result["bridges"])


class TestWisdomRecommender(unittest.TestCase):
    def test_recommend_by_tag(self):
        result = recommend_wisdom(tag="nefret")
        self.assertIn("quote", result)
        self.assertIn("source", result)

    def test_recommend_by_text(self):
        result = recommend_wisdom(text="kin ve düşmanlık dünyayı yakıyor")
        self.assertIn("quote", result)
        self.assertTrue(len(result["quote"]) > 10)

    def test_all_sages_present(self):
        sages = get_all_sages()
        self.assertIn("Yunus Emre", sages)
        self.assertIn("Mevlana Celaleddin-i Rumi", sages)
        self.assertIn("Nelson Mandela", sages)


if __name__ == "__main__":
    unittest.main()
