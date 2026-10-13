#!/usr/bin/env python3
"""
Test Koşturucu (Test Runner) — Kördüğüm Değil Gördüğüm
Tüm birim testleri çalıştırır ve temiz bir özet raporlar.
"""

import unittest
import sys
import os

if __name__ == "__main__":
    # Test klasörünü doğrudan yükle
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(os.path.dirname(__file__), "tests"), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)
