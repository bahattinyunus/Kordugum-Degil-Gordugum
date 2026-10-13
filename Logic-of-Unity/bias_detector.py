"""
Gelişmiş Önyargı ve Nefret Dili Tespit Modülü.
Çok dilli anahtar kelime/örüntü eşleme, kategori tespiti ve şiddet skoru hesaplama.
"""

import re
from typing import Dict, List, Any


BIAS_DICTIONARY = {
    "İnsanlıktan Çıkarma (Dehumanization)": {
        "weight": 12,
        "patterns": [
            r"\bbarbar(lar|ın|a|ı|ca)?\b",
            r"\b(savage|savages)\b",
            r"\b(sous-homme|barbare|barbares)\b",
            r"\başağılık\b",
            r"\bhayvan sürüsü\b",
            r"\bkemirgen(ler)?\b",
            r"\bparazit(ler)?\b",
            r"\bscum\b",
            r"\bvermin\b",
            r"\bparasites?\b",
            r"\binferior\b"
        ]
    },
    "Üstünlük Taslama (Supremacism & Xenophobia)": {
        "weight": 10,
        "patterns": [
            r"\b(üstün ırk|saf kan)\b",
            r"\bsupreme race\b",
            r"\brace supérieure\b",
            r"\bdefol(un)?\b",
            r"\bget out\b",
            r"\bhırsız millet\b",
            r"\bburası bizim(dir)?\b",
            r"\bistemiyoruz onları\b",
            r"\bistenmiyor(lar)?\b",
            r"\bgit(sinler)? buradan\b",
            r"\bülkemizden defolun\b"
        ]
    },
    "Kalıpyargı & Ötekileştirme (Stereotyping & Othering)": {
        "weight": 6,
        "patterns": [
            r"\byobaz(lar)?\b",
            r"\bmedeni olmayan\b",
            r"\bgerici(ler)?\b",
            r"\bbigot(s)?\b",
            r"\buncivilized\b",
            r"\bbackward people\b",
            r"\bthose people\b",
            r"\bétroit d'esprit\b",
            r"\bnon civilisé\b",
            r"\btuhaf bunlar\b"
        ]
    },
    "İnce Ayrımcılık & Genelleme (Subtle Bias & Generalization)": {
        "weight": 4,
        "patterns": [
            r"\bonlar hep böyle\b",
            r"\bzaten belliydi\b",
            r"\btipik bunlar\b",
            r"\bthey always\b",
            r"\bit was obvious\b",
            r"\btypical of them\b",
            r"\bils sont toujours comme ça\b",
            r"\bc'était évident\b"
        ]
    }
}


def detect_bias(text: str) -> Dict[str, Any]:
    """
    Verilen metindeki önyargılı ve ayrıştırıcı ifadeleri tespit eder.
    
    Args:
        text: Analiz edilecek metin.
        
    Returns:
        dict: Tespit edilen önyargılar, kategori dökümü, skor ve tavsiye.
    """
    if not text or not isinstance(text, str):
        return {
            "found": [],
            "categories": {},
            "score": 0,
            "status": "TEMİZ",
            "advice": "İncelenecek metin bulunamadı."
        }

    found_biases = []
    category_matches: Dict[str, List[str]] = {}
    severity_score = 0

    for category, config in BIAS_DICTIONARY.items():
        weight = config["weight"]
        matched_in_cat = []
        for pattern in config["patterns"]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matched_str = match.group(0).strip()
                if matched_str:
                    matched_in_cat.append(matched_str)
                    found_biases.append(matched_str)
                    severity_score += weight

        if matched_in_cat:
            category_matches[category] = list(set(matched_in_cat))

    normalized_score = min(100, severity_score)
    unique_found = sorted(list(set(found_biases)))

    if normalized_score >= 40:
        status = "YÜKSEK ÖNYARGI"
        advice = "Metinde yoğun ötekileştirici ve ayrımcı kalıplar var. Empatik dönüşüm önerilir."
    elif normalized_score > 0:
        status = "DİKKAT"
        advice = "Metinde genelleme veya kalıpyargı barındıran ifadeler tespit edildi."
    else:
        status = "TEMİZ"
        advice = "Ayrımcı veya önyargılı bir ifade bulunamadı; gönül dili hakim."

    return {
        "found": unique_found,
        "categories": category_matches,
        "score": normalized_score,
        "status": status,
        "advice": advice
    }


if __name__ == "__main__":
    test_cases = [
        "Bu barbarlar ve yobazlar buraya ait değil, defolun!",
        "They always behave typical like that and uncivilized.",
        "Herkes eşittir ve bir bütündür, can cana kardeşiz.",
        "Onlar hep böyle zaten belliydi."
    ]

    for test in test_cases:
        res = detect_bias(test)
        print(f"Metin: {test}")
        print(f"Durum: {res['status']} | Skor: {res['score']}/100")
        print(f"Kategoriler: {res['categories']}")
        print(f"Tavsiye: {res['advice']}\n")
