"""
Empati ve Sevgi Dili Dönüştürücüsü (Empathy Generator).
Sert, ayrıştırıcı ve ötekileştirici ifadeleri; birleştirici, şefkatli ve onarıcı
bir dile dönüştürür.
"""

import re
import random
from typing import Dict, Any


# Türkçe kural bazlı dönüşümler (Türkçe ses uyumuna dikkat edilerek)
TR_TRANSFORMATIONS = [
    # Çoğul ve yönelme/bulunma/ayrılma durumları
    (r"\byabancılar(a|da|dan|ı|la)?\b", r"misafirler\1"),
    (r"\byabancıya\b", "misafire"),
    (r"\byabancıyı\b", "misafiri"),
    (r"\byabancıda\b", "misafirde"),
    (r"\byabancıdan\b", "misafirden"),
    (r"\byabancıyla\b", "misafirle"),
    (r"\byabancı\b", "misafir"),

    (r"\bbarbarlar(a|da|dan|ı|la)?\b", r"yol arkadaşlarımız\1"),
    (r"\bbarbar(a|da|dan|ı|la)?\b", r"kültür elçisi\1"),

    (r"\bonlara\b", "kardeşlerimize"),
    (r"\bonları\b", "kardeşlerimizi"),
    (r"\bonlarda\b", "kardeşlerimizde"),
    (r"\bonlardan\b", "kardeşlerimizden"),
    (r"\bonlarla\b", "kardeşlerimizle"),
    (r"\bonların\b", "kardeşlerimizin"),
    (r"\bonlar\b", "kardeşlerimiz"),

    (r"\bötekiler(e|de|den|i|le)?\b", r"yol yoldaşlarımız\1"),
    (r"\böteki\b", "yol arkadaşı"),

    (r"\bnefret ediyorum\b", "anlamakta henüz zorlanıyorum ama gayret ediyorum"),
    (r"\bnefret ediyoruz\b", "ortak noktalarımızı bulmaya çalışıyoruz"),
    (r"\bistenmiyor(lar)?\b", "sevgiyle karşılanmayı hak ediyorlar"),
    (r"\bistemiyoruz\b", "birlikte öğrenmeye niyet ediyoruz"),
    (r"\bdefol(un)?\b", "birlikte soframızı paylaşalım"),
    (r"\bgit(sinler)? buradan\b", "gelin konuşalım"),
    (r"\byobaz(lar)?\b", "farklı pencerelerden bakan canlar"),
    (r"\bgerici(ler)?\b", "kendi yolunda yürüyen insanlar"),
    (r"\başağılık\b", "onurlu"),
    (r"\büstün ırk\b", "tüm ırkların kardeşliği"),
]

# İngilizce dönüşümler
EN_TRANSFORMATIONS = [
    (r"\bthey are inferior\b", "we all possess inherent equal dignity"),
    (r"\bget out\b", "welcome to our shared space"),
    (r"\bwe hate them\b", "we are seeking to understand each other"),
    (r"\bthose people\b", "our fellow neighbors"),
    (r"\bsavages?\b", "our global brothers and sisters"),
    (r"\buncivilized\b", "rich with varied traditions"),
    (r"\bthey always\b", "each individual has unique gifts")
]

# Fransızca dönüşümler
FR_TRANSFORMATIONS = [
    (r"\bsous-hommes?\b", "êtres humains égaux en dignité"),
    (r"\braces? supérieure(s)?\b", "fraternité humaine universelle"),
    (r"\bils sont toujours comme ça\b", "chacun porte sa propre lumière"),
    (r"\bbarbares?\b", "frères et sœurs du monde")
]

HARMONY_TIPS = [
    "Farklılıklar bizi zayıflatmaz; tıpkı bir ormanın türlü ağaçları gibi derinleştirir ve zenginleştirir.",
    "Onun ayakkabılarıyla birkaç adım attığını hayal etmeyi dene; her kalp anlaşılmayı bekler.",
    "Sevgi, her türlü karanlığı dağıtan tek ışıktır. Bir mum başka bir mumu yakmakla ışığından kaybetmez.",
    "Yetmiş iki millete aynı gözle bakabilen gönül, hiçbir köprüde takılıp kalmaz.",
    "Söz ola kese savaşı, söz ola kestire başı / Söz ola ağulu aşı bal ile yağ ede bir söz. — Yunus Emre",
    "Bütün insanlar tek bir bedenin azaları gibidir; bir uzuv acırsa hepsi sızlar. — Sadi Şirazi",
    "Ubuntu: Ben, biz olduğumuz için benim. Başkasının onurunu korumak, kendi onurunu korumaktır."
]


def generate_empathy(text: str) -> Dict[str, Any]:
    """
    Sert dili empatik ve birleştirici bir dile dönüştürür.
    
    Args:
        text: Dönüştürülecek metin.
        
    Returns:
        dict: Dönüştürülmüş metin, değişim olup olmadığı ve Gönül Esintisi önerisi.
    """
    if not text or not isinstance(text, str):
        return {
            "original": "",
            "transformed": "",
            "changed": False,
            "harmony_tip": random.choice(HARMONY_TIPS)
        }

    result = text

    # Sırayla dönüşümleri uygula (harf büyüklüğü duyarsız)
    all_rules = TR_TRANSFORMATIONS + EN_TRANSFORMATIONS + FR_TRANSFORMATIONS
    for pattern, replacement in all_rules:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    # Baş harfi büyük yap
    if result:
        result = result[0].upper() + result[1:]

    changed = (result.strip().lower() != text.strip().lower())

    return {
        "original": text,
        "transformed": result,
        "changed": changed,
        "harmony_tip": random.choice(HARMONY_TIPS)
    }


if __name__ == "__main__":
    toxic_inputs = [
        "Biz onlardan nefret ediyoruz, bu barbarlar buraya gelmemeli.",
        "Yabancılar bu sokakta istenmiyor, defolun!",
        "They are inferior and uncivilized, get out!",
        "Sous-homme et barbare ne sont pas les bienvenus."
    ]

    for inp in toxic_inputs:
        res = generate_empathy(inp)
        print(f"Orijinal : {inp}")
        print(f"Empatik  : {res['transformed']}")
        print(f"Değişti  : {res['changed']}")
        print(f"Gönül İzi: {res['harmony_tip']}\n")
