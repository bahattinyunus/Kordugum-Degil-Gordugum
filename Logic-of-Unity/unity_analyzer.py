"""
Birlik ve Gönül Endeksi Analiz Aracı (Unity Analyzer).
Metindeki birleştirici, kucaklayıcı ve şefkatli 'Gönül Köprüleri'ni çok dilli
olarak analiz eder ve kapsamlı bir Gönül Skoru hesaplar.
"""

import re
from typing import Dict, Any, List


UNITY_DIMENSIONS = {
    "Sevgi & Muhabbet": [
        r"\bsevgi\w*\b",
        r"\bsevelim\b",
        r"\başk\w*\b",
        r"\bmuhabbet\w*\b",
        r"\bşefkat\w*\b",
        r"\bmerhamet\w*\b",
        r"\blove\w*\b",
        r"\bcompassion\w*\b",
        r"\bamour\w*\b",
        r"\bamor\w*\b",
        r"\bliebe\w*\b",
        r"\bmahabbah\b"
    ],
    "Birlik & Tevhid": [
        r"\bbirlik\w*\b",
        r"\bberaber\w*\b",
        r"\bbütün\w*\b",
        r"\btevhid\w*\b",
        r"\btek yürek\b",
        r"\bcan cana\b",
        r"\bunity\b",
        r"\boneness\b",
        r"\btogether\w*\b",
        r"\bunité\w*\b",
        r"\bunidad\w*\b",
        r"\beinheit\b",
        r"\bubuntu\b",
        r"\bwahda\b"
    ],
    "Kardeşlik & Dayanışma": [
        r"\bkardeş\w*\b",
        r"\bdost\w*\b",
        r"\byol arkadaş\w*\b",
        r"\bdayanışma\w*\b",
        r"\bomuz omuza\b",
        r"\bcan(lar|ımız|la|larla)?\b",
        r"\bbrother\w*\b",
        r"\bsister\w*\b",
        r"\bsolidarity\b",
        r"\bfraternité\w*\b",
        r"\bsolidaridad\b",
        r"\bbrüderlichkeit\b"
    ],
    "Hoşgörü & Empati": [
        r"\bhoşgörü\w*\b",
        r"\banlayış\w*\b",
        r"\bempati\w*\b",
        r"\bsabır\w*\b",
        r"\bkucakla\w*\b",
        r"\btolerance\b",
        r"\bempathy\b",
        r"\bunderstanding\b",
        r"\btolérance\b",
        r"\btolerancia\b",
        r"\bverständnis\b"
    ],
    "Paylaşım & Cömertlik": [
        r"\bpaylaş\w*\b",
        r"\bbölüş\w*\b",
        r"\bortak sofra\w*\b",
        r"\bsofra\w*\b",
        r"\bcömert\w*\b",
        r"\bshare\w*\b",
        r"\bsharing\b",
        r"\bpartage\w*\b",
        r"\bcompartir\b",
        r"\bteilen\b"
    ],
    "Barış & Adalet": [
        r"\bbarış\w*\b",
        r"\badalet\w*\b",
        r"\bhuzur\w*\b",
        r"\bsulh\w*\b",
        r"\bselamet\w*\b",
        r"\bpeace\w*\b",
        r"\bjustice\b",
        r"\bharmony\b",
        r"\bpaix\b",
        r"\bpaz\b",
        r"\bfrieden\b",
        r"\bsalam\b"
    ]
}


def analyze_unity(text: str) -> Dict[str, Any]:
    """
    Metindeki birlik dilini analiz eder, Gönül Köprülerini tespit eder ve puanlar.
    
    Args:
        text: Analiz edilecek metin.
        
    Returns:
        dict: unity_score (0-100), bridges detayı, bridge_diversity, level ve mesaj.
    """
    if not text or not isinstance(text, str):
        return {
            "unity_score": 0,
            "bridge_diversity": 0,
            "bridges": {},
            "level": "Toprak Bekliyor",
            "message": "Analiz edilecek bir metin girilmedi."
        }

    bridges_found: Dict[str, List[str]] = {}
    total_matches = 0

    for category, patterns in UNITY_DIMENSIONS.items():
        matched_tokens = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                token = match.group(0).strip().lower()
                if token:
                    matched_tokens.append(token)
        if matched_tokens:
            bridges_found[category] = sorted(list(set(matched_tokens)))
            total_matches += len(matched_tokens)

    diversity = len(bridges_found)

    # Skor hesabı: toplam kelime eşleşmesi + kategori çeşitliliği primi
    raw_score = (total_matches * 12) + (diversity * 8)
    unity_score = min(100, max(0, raw_score))

    if unity_score >= 80:
        level = "Gönül Güneşi"
        message = "Gönül kapıları sonuna kadar açık! İnsanlığı kuşatan muazzam bir birlik frekansı."
    elif unity_score >= 50:
        level = "Birlik Çerağı"
        message = "Güçlü köprüler kurulmuş; sevgi ve kardeşlik dili metne can vermiş."
    elif unity_score >= 20:
        level = "Filizlenen Umut"
        message = "İlk tohumlar atılmış, güzel bağlar var. Biraz daha derinleştirebiliriz."
    elif unity_score > 0:
        level = "Uyanan Yankı"
        message = "Birlik diline dair bir kıvılcım var; yeni köprüler kurmaya davetlisiniz."
    else:
        level = "Toprak Bekliyor"
        message = "Henüz birleştirici köprü kelime tespit edilemedi. Bir tatlı söz dünyayı değiştirir."

    return {
        "unity_score": unity_score,
        "bridge_diversity": diversity,
        "bridges": bridges_found,
        "level": level,
        "message": message
    }


if __name__ == "__main__":
    samples = [
        "Biz sevgiyle, dostlukla ve bütün canlarla barış içinde bir dünya kuracağız. Her soframızı paylaşırız.",
        "Nefret değil, hoşgörü, adalet ve kardeşlik bizi kurtaracak. We believe in unity and peace.",
        "Sıradan bir masa ve sandalye.",
        "Ubuntu: Ben, biz olduğumuz için varım."
    ]

    for s in samples:
        res = analyze_unity(s)
        print(f"Metin: {s}")
        print(f"Skor: {res['unity_score']}/100 | Seviye: {res['level']} | Çeşitlilik: {res['bridge_diversity']}/6")
        print(f"Köprüler: {res['bridges']}")
        print(f"Mesaj: {res['message']}\n")
