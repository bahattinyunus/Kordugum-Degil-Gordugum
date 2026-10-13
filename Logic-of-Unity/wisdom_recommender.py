"""
Gönül ve Hikmet Tavsiye Motoru (Wisdom Recommender).
Kullanıcının metninde veya hissettiği temada geçen duyguya göre
kadim bilgelerden, evrensel manifestolardan ve barış şiirlerinden
iyileştirici söz ve şiirler önerir.
"""

import json
import os
import random
from typing import Dict, List, Any, Optional


CURATED_WISDOM = [
    {
        "source": "Yunus Emre",
        "era": "13. Yüzyıl Anadolu",
        "tags": ["sevgi", "birlik", "önyargı", "hoşgörü", "kin"],
        "quote": "Düşmanımız kindir bizim, kamu alem birdir bize. Yaratılanı severiz, Yaradan'dan ötürü.",
        "context": "Ayrılık ve düşmanlık duygusuna karşı birliğin ebedi ilacı."
    },
    {
        "source": "Mevlana Celaleddin-i Rumi",
        "era": "13. Yüzyıl Konya",
        "tags": ["kucaklaşma", "af", "hata", "ayrılık", "umut"],
        "quote": "Gel, gel, ne olursan ol yine gel! İster kâfir, ister mecusi, ister puta tapan ol yine gel. Bizim dergâhımız ümitsizlik dergâhı değildir.",
        "context": "Hiç kimseyi dışarıda bırakmayan sonsuz şefkat kapısı."
    },
    {
        "source": "Hacı Bektaş-i Veli",
        "era": "13. Yüzyıl Horasan & Kapadokya",
        "tags": ["eşitlik", "millet", "ırkçılık", "insan"],
        "quote": "Yetmiş iki milleti bir gör. Bir olalım, iri olalım, diri olalım. İncinsen de incitme.",
        "context": "Farklılıkların tek bir canda buluşma çağrısı."
    },
    {
        "source": "Martin Luther King Jr.",
        "era": "1963 ABD",
        "tags": ["nefret", "karanlık", "adalet", "ışık", "ırkçılık"],
        "quote": "Karanlık karanlığı kovamaz; bunu sadece ışık yapabilir. Nefret nefreti kovamaz; bunu sadece sevgi yapabilir.",
        "context": "Nefret döngüsünü şiddetsiz sevgiyle kırma ilkesi."
    },
    {
        "source": "Nelson Mandela",
        "era": "1994 Güney Afrika",
        "tags": ["öğrenme", "çocuk", "özgürlük", "ırk", "affetme"],
        "quote": "Hiç kimse derisinin rengi, geçmişi ya da dini yüzünden bir diğerinden nefret ederek doğmaz. İnsanlar nefret etmeyi öğrenirler; ve eğer nefret etmeyi öğrenebiliyorlarsa, onlara sevmeyi de öğretebiliriz; çünkü sevgi insan kalbine nefretten çok daha doğal gelir.",
        "context": "Sevginin insanın fıtratındaki en doğal güç olduğu gerçeği."
    },
    {
        "source": "Aşık Veysel",
        "era": "20. Yüzyıl Sivas",
        "tags": ["toprak", "eşitlik", "kibir", "ayrımcılık"],
        "quote": "Beni hor görme gardaşım, sen altınsın ben tunç muyum? Aynı vardan var olmuşuz, sen gümüşsün ben saç mıyım?",
        "context": "İnsanın topraktan gelen kökünde kibir ve üstünlüğün manasızlığı."
    },
    {
        "source": "Desmond Tutu",
        "era": "Güney Afrika",
        "tags": ["ubuntu", "bağlılık", "insanlık", "ortaklık"],
        "quote": "Ubuntu: 'Ben, biz olduğumuz için benim.' Benim insanlığım senin insanlığına sıkı sıkıya bağlıdır.",
        "context": "İnsanın ancak bir başkasıyla bütünleştiğinde insan olabileceği felsefesi."
    },
    {
        "source": "Maya Angelou",
        "era": "ABD",
        "tags": ["farklılık", "insan", "şiir", "birlik"],
        "quote": "Küçük şeylerde farklıyız, büyük şeylerde aynıyız. Farklılıklarımız çok, ama dostlarım, benzerliğimiz benzemezliğimizden çok daha büyüktür.",
        "context": "Dış kabuğun altındaki ortak insanlık cevheri."
    },
    {
        "source": "Sadi Şirazi",
        "era": "13. Yüzyıl Şiraz",
        "tags": ["beden", "acı", "merhamet", "dayanışma"],
        "quote": "Âdemoğulları bir vücudun uzuvları gibidir; çünkü aynı cevherden yaratılmışlardır. Felek bir uzva dert verirse, diğer uzuvlarda da huzur kalmaz.",
        "context": "Bir insanın acısının bütün insanlığın acısı olduğu şuur."
    },
    {
        "source": "Khalil Gibran",
        "era": "Lübnan & Dünya",
        "tags": ["vatan", "evrensel", "sınır", "kardeşlik"],
        "quote": "Yeryüzü benim memleketimdir ve insanlık benim ailemdir.",
        "context": "Coğrafi sınırların ötesindeki kozmik aile bilinci."
    }
]


def recommend_wisdom(text: str = "", tag: Optional[str] = None) -> Dict[str, Any]:
    """
    Metin içeriğine, anahtar kelimeye veya rastgele bir esintiye göre hikmetli söz önerir.
    
    Args:
        text: İncelenen metin.
        tag: Doğrudan tema filtresi (ör: 'adalet', 'nefret', 'birlik').
        
    Returns:
        dict: Seçilen bilge, söz, dönem ve bağlam.
    """
    candidates = []

    # 1. Etikete göre ara
    if tag:
        tag_lower = tag.lower()
        candidates = [item for item in CURATED_WISDOM if any(tag_lower in t for t in item["tags"])]

    # 2. Metne göre eşleştir
    if not candidates and text:
        text_lower = text.lower()
        for item in CURATED_WISDOM:
            score = sum(1 for t in item["tags"] if t in text_lower)
            if score > 0:
                candidates.append((score, item))
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]

    # 3. Eğer eşleşme yoksa veya girdi boşsa rastgele seç
    if not candidates:
        return random.choice(CURATED_WISDOM)

    return random.choice(candidates) if isinstance(candidates[0], dict) else candidates[0][1]


def get_all_sages() -> List[str]:
    """Sistemde kayıtlı bilgelerin isim listesini döner."""
    return [item["source"] for item in CURATED_WISDOM]


if __name__ == "__main__":
    print("Rastgele Hikmet:")
    print(recommend_wisdom())
    print("\n'nefret' Temalı Hikmet:")
    print(recommend_wisdom(tag="nefret"))
    print("\nMetin Eşleştirmesi:")
    print(recommend_wisdom(text="onlardan nefret ediyorum ayrılık var"))
