#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║             GÖNÜL TERMİNALİ - Kördüğüm Değil Gördüğüm            ║
║     Sevginin, adaletin ve empati dilinin komut satırı aracı.     ║
╚══════════════════════════════════════════════════════════════════╝

Kullanım:
  python gonul_terminali.py --hepsi "incelenecek metin"
  python gonul_terminali.py --analiz "metin"
  python gonul_terminali.py --donustur "metin"
  python gonul_terminali.py --birlik "metin"
  python gonul_terminali.py --hikmet "konu veya duygu"
  python gonul_terminali.py --json --hepsi "metin"
  python gonul_terminali.py --interaktif
"""

import argparse
import json
import os
import sys

# Windows terminali için UTF-8 ayarla
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Modül yollarını ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bias_detector import detect_bias
from empathy_generator import generate_empathy
from unity_analyzer import analyze_unity
from wisdom_recommender import recommend_wisdom


# ANSI Renk Kodları
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_MAGENTA = "\033[95m"
C_GRAY = "\033[90m"
C_WHITE = "\033[97m"

BANNER = f"""{C_MAGENTA}╔══════════════════════════════════════════════════════════════╗
║        🪢  GÖNÜL TERMİNALİ — Kördüğüm Değil Gördüğüm        ║
║          "Aşk gelicek cümle eksikler biter." — Yunus         ║
╚══════════════════════════════════════════════════════════════╝{C_RESET}"""


def draw_bar(score: int, max_val: int = 100, length: int = 20, color: str = C_GREEN) -> str:
    """Metin tabanlı renkli bir ilerleme/seviye çubuğu çizer."""
    score = max(0, min(max_val, score))
    filled = int((score / max_val) * length)
    empty = length - filled
    return f"{color}{'█' * filled}{C_GRAY}{'░' * empty}{C_RESET} {score}/{max_val}"


def print_separator():
    print(f"{C_GRAY}{'─' * 62}{C_RESET}")


def run_full_analysis(text: str, as_json: bool = False):
    """Metin için tüm analiz ve tavsiyeleri tek seferde çalıştırır."""
    bias = detect_bias(text)
    empathy = generate_empathy(text)
    unity = analyze_unity(text)
    wisdom = recommend_wisdom(text=text)

    if as_json:
        payload = {
            "input_text": text,
            "bias_analysis": bias,
            "empathy_transformation": empathy,
            "unity_analysis": unity,
            "wisdom_guidance": wisdom
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(BANNER)
    print(f"\n{C_YELLOW}📋 GİRDİ METNİ:{C_RESET}")
    print(f"  {C_WHITE}\"{text}\"{C_RESET}")
    print_separator()

    # 1. Önyargı Analizi
    bias_color = C_GREEN if bias["score"] == 0 else (C_YELLOW if bias["score"] < 40 else C_RED)
    print(f"{C_RED}🔍 ÖNYARGI & AYRIMCILIK ANALİZİ:{C_RESET}")
    print(f"  Durum     : {bias_color}{C_BOLD}{bias['status']}{C_RESET}")
    print(f"  Yoğunluk  : {draw_bar(bias['score'], color=bias_color)}")
    if bias["found"]:
        print(f"  Tespitler : {C_YELLOW}{', '.join(bias['found'])}{C_RESET}")
        for cat, items in bias["categories"].items():
            print(f"    • {C_GRAY}{cat}:{C_RESET} {', '.join(items)}")
    else:
        print(f"  Tespitler : {C_GREEN}Önyargılı ifadeye rastlanmadı.{C_RESET}")
    print(f"  Rehberlik : {bias['advice']}")
    print_separator()

    # 2. Empatik Dönüşüm
    print(f"{C_CYAN}💚 EMPATİK DÖNÜŞÜM & GÖNÜL DİLİ:{C_RESET}")
    if empathy["changed"]:
        print(f"  Onarılmış : {C_GREEN}{C_BOLD}{empathy['transformed']}{C_RESET}")
    else:
        print(f"  Onarılmış : {C_GREEN}Metin zaten nezaket ve hürmetle söylenmiş.{C_RESET}")
    print(f"  Gönül İzi : {C_CYAN}«{empathy['harmony_tip']}»{C_RESET}")
    print_separator()

    # 3. Birlik Endeksi
    unity_color = C_GREEN if unity["unity_score"] >= 50 else (C_YELLOW if unity["unity_score"] > 0 else C_GRAY)
    print(f"{C_GREEN}🌐 BİRLİK & GÖNÜL ENDEKSİ:{C_RESET}")
    print(f"  Puan      : {draw_bar(unity['unity_score'], color=unity_color)}")
    print(f"  Makam     : {C_BOLD}{unity['level']}{C_RESET} ({unity['bridge_diversity']}/6 boyut)")
    if unity["bridges"]:
        print(f"  Köprüler  :")
        for dim, tokens in unity["bridges"].items():
            print(f"    • {C_GREEN}{dim}:{C_RESET} {', '.join(tokens)}")
    else:
        print(f"  Köprüler  : Henüz açık bir birleştirici kelime yok.")
    print(f"  Mesaj     : {unity['message']}")
    print_separator()

    # 4. Hikmet & Bilgelik Rehberliği
    print(f"{C_MAGENTA}🕊️  HİKMET & BİLGELİK REHBERLİĞİ:{C_RESET}")
    print(f"  {C_BOLD}{wisdom['source']}{C_RESET} ({wisdom['era']}):")
    print(f"  {C_WHITE}«{wisdom['quote']}»{C_RESET}")
    print(f"  {C_GRAY}Bağlam: {wisdom['context']}{C_RESET}")
    print_separator()

    print(f"{C_MAGENTA}✨ 'Gözün gördüğüne gönül katılmazsa, bakış sadece bir kördüğümdür.' — Mevlana{C_RESET}\n")


def interactive_mode():
    """Kullanıcıyla birebir diyalog kuran interaktif terminal deneyimi."""
    print(BANNER)
    print(f"{C_CYAN}Gönül Terminali İnteraktif Moduna Hoş Geldiniz!{C_RESET}")
    print("Herhangi bir cümle yazarak analiz edebilir veya 'q' yazıp çıkabilirsiniz.\n")

    while True:
        try:
            user_input = input(f"{C_YELLOW}Cümleniz > {C_RESET}").strip()
            if not user_input:
                continue
            if user_input.lower() in ["q", "exit", "quit", "çıkış"]:
                print(f"\n{C_MAGENTA}Gönlünüz ferah, yolunuz bir olsun. Sevgiyle kalın! 🪢🕊️{C_RESET}\n")
                break
            run_full_analysis(user_input, as_json=False)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C_MAGENTA}Hoşça kalın!{C_RESET}")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Gönül Terminali — Metindeki önyargıyı gör, şefkate ve birliğe dönüştür.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Örnek: python gonul_terminali.py --hepsi 'onlar yabancı ve barbar'"
    )
    parser.add_argument("--analiz", help="Metni önyargı ve nefret dili açısından incele", type=str)
    parser.add_argument("--donustur", help="Metni empatik sevgi diline dönüştür", type=str)
    parser.add_argument("--birlik", help="Metindeki birlik endeksini ve gönül köprülerini ölç", type=str)
    parser.add_argument("--hikmet", help="Belirli bir duygu veya metne göre bilge sözü getir", type=str)
    parser.add_argument("--hepsi", help="Tüm analiz katmanlarını çalıştır", type=str)
    parser.add_argument("--json", help="Çıktıyı JSON formatında ver", action="store_true")
    parser.add_argument("--interaktif", "-i", help="İnteraktif terminal konsolunu başlat", action="store_true")

    args = parser.parse_args()

    if args.interaktif:
        interactive_mode()
        return

    if args.hepsi:
        run_full_analysis(args.hepsi, as_json=args.json)
    elif args.analiz:
        res = detect_bias(args.analiz)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else res)
    elif args.donustur:
        res = generate_empathy(args.donustur)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else res)
    elif args.birlik:
        res = analyze_unity(args.birlik)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else res)
    elif args.hikmet:
        res = recommend_wisdom(text=args.hikmet, tag=args.hikmet)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else f"«{res['quote']}» — {res['source']} ({res['era']})")
    else:
        # Argümansız çalışınca örnek demo sun
        demo_text = "Barbarlar ve yabancılar burada istenmiyor, defolun!"
        print(f"{C_GRAY}[Örnek Demo Çalıştırılıyor... Kendi cümleniz için --hepsi veya --interaktif kullanın]{C_RESET}\n")
        run_full_analysis(demo_text, as_json=args.json)


if __name__ == "__main__":
    main()
