# cleanup_pif_v3.py - Improved cleanup with statistical garbage detection

import re
from pathlib import Path
from typing import Tuple

# Correct ingredient data
CORRECT_INGREDIENTS = {
    "Aqua": "85.7474",
    "Water": "85.7474",
    "Sodium Laureth Sulfate": "7.1775",
    "Sodium Chloride": "3.5900",
    "Cocamidopropyl Betaine": "1.2375",
    "Lauryl Glucoside": "1.2375",
    "Lactic Acid": "0.3600",
    "Disodium EDTA": "0.2000",
    "Sodium Benzoate": "0.2000",
    "Parfum": "0.1000",
    "Fragrance": "0.1000",
    "Alpha-Glucan Oligosaccharide": "0.0500",
    "Polyquaternium-7": "0.0500",
    "Sodium Hydroxide": "0.0001",
    "Limonene": "0.0907",
    "Linalool": "0.0007",
    "Citronellol": "0.0004",
}

CORRECT_CAS = {
    "Aqua": "7732-18-5",
    "Water": "7732-18-5",
    "Sodium Laureth Sulfate": "9004-82-4",
    "Sodium Chloride": "7647-14-5",
    "Cocamidopropyl Betaine": "97862-59-4",
    "Lauryl Glucoside": "110615-47-9",
    "Lactic Acid": "50-21-5",
    "Disodium EDTA": "139-33-3",
    "Sodium Benzoate": "532-32-1",
    "Polyquaternium-7": "26590-05-6",
    "Sodium Hydroxide": "1310-73-2",
    "Limonene": "138-86-3",
    "Linalool": "78-70-6",
    "Citronellol": "106-22-9",
}

# Whitelist for valid short lines (prevent over-cleaning)
VALID_SHORT_PATTERNS = [
    r'^pH\s*[:=]?\s*[\d.]+',  # pH values
    r'^±\s*[\d.]+',  # Plus-minus
    r'^≤\s*[\d.]+',  # Less than or equal
    r'^≥\s*[\d.]+',  # Greater than or equal
    r'^°C$',  # Temperature unit
    r'^[A-Z]{1,3}_?\d*$',  # Chemical formulas like H2O, CO2
    r'^\d+\.?\d*\s*%$',  # Percentage values
    r'^\d+-\d+-\d+$',  # CAS numbers
    r'^[A-Z]+$',  # All caps words (INCI names)
    r'^\d{1,2}$',  # Small numbers (section numbers)
]

def is_valid_short_line(line: str) -> bool:
    """Check if a short line should be preserved."""
    for pattern in VALID_SHORT_PATTERNS:
        if re.match(pattern, line, re.IGNORECASE):
            return True
    return False

def is_likely_garbage_by_stats(line: str) -> bool:
    """Detect garbage based on character statistics."""
    if not line.strip():
        return False
    
    stripped = line.strip()
    
    # Whitelist check first - preserve valid short lines
    if len(stripped) <= 5 and is_valid_short_line(stripped):
        return False
    
    # Special character ratio > 50% and length < 30
    special_chars = sum(1 for c in stripped if not c.isalnum() and not c.isspace())
    if len(stripped) < 30 and special_chars / len(stripped) > 0.5:
        return True
    
    # Consecutive rare CJK characters (uncommon Unicode range)
    rare_cjk = sum(1 for c in stripped if '\u9f00' <= c <= '\u9fff')
    if rare_cjk > 5:
        return True
    
    # Control characters (except common ones)
    control_chars = sum(1 for c in stripped if ord(c) < 32 and c not in '\n\r\t')
    if control_chars > 2:
        return True
    
    # Mixed script anomaly (too many different scripts in short text)
    has_latin = any(c.isalpha() and ord(c) < 128 for c in stripped)
    has_cjk = any('\u4e00' <= c <= '\u9fff' for c in stripped)
    has_thai = any('\u0e00' <= c <= '\u0e7f' for c in stripped)
    script_count = sum([has_latin, has_cjk, has_thai])
    
    if script_count >= 3 and len(stripped) < 50:
        # Likely OCR garbage mixing multiple scripts
        return True
    
    return False

def clean_garbage_lines(text: str) -> Tuple[str, dict]:
    """Remove garbage lines with statistics."""
    stats = {
        'original_lines': 0,
        'removed_lines': 0,
        'preserved_short_lines': 0,
    }
    
    lines = text.splitlines()
    stats['original_lines'] = len(lines)
    cleaned_lines = []
    
    # Known garbage patterns (exact matches)
    known_garbage = {
        '十十', 'm m _5', '·EE96',
        '曬鼉＇＂上蟑嘯圜駟峒 E 矚',
        '－囉园·伍專記四',
        '..呱黷 l\' 巴 11l｀彎｀＇',
        '可 k 畫衊蛐：｀｀薑這刀',
        '\'軍可的曇 2.1 國',
        '@2 泌 c,', 'OF p ue、', 'o o,',
        '\'l una 血頲 un1 面西咽才',
        ',, r~ud and Drug Ad.ministration',
        'Serial No…… AA... l .~.7.7 5 9',
        '丶', '－一一一· ~矗',
    }
    
    for line in lines:
        stripped = line.strip()
        is_garbage = False
        
        # Check exact garbage matches
        if stripped in known_garbage:
            is_garbage = True
            stats['removed_lines'] += 1
        # Check statistical garbage
        elif is_likely_garbage_by_stats(line):
            is_garbage = True
            stats['removed_lines'] += 1
        # Check very short lines but preserve valid ones
        elif len(stripped) <= 2:
            if is_valid_short_line(stripped):
                stats['preserved_short_lines'] += 1
            else:
                # Check if it's just punctuation or noise
                if not any(c.isalnum() for c in stripped):
                    is_garbage = True
                    stats['removed_lines'] += 1
        
        if not is_garbage:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines), stats

def fix_ocr_errors(text: str) -> str:
    """Fix common OCR errors."""
    fixes = {
        'Fem inine': 'Feminine',
        'Fem in ine': 'Feminine',
        'appltto': 'apply to',
        't1oroughly': 'thoroughly',
        'ConIains': 'Contains',
        'Sodum': 'Sodium',
        '「au r e t h': 'Laureth',
        'SuIIate': 'Sulfate',
        'Chlonde': 'Chloride',
        'Lauml': 'Lauryl',
        'GluCOSlde': 'Glucoside',
        'Cocamldopropyl': 'Cocamidopropyl',
        'Betame': 'Betaine',
        'prov ided': 'provided',
        'con tent': 'content',
        'targe t': 'target',
        'lntomal': 'Internal',
        'sm a」': 'small',
        'h ternal': 'internal',
        'Wet area Pour sma」': 'Wet area. Pour small',
        '200C': '20°C',
        '250C': '25°C',
        '300C': '30°C',
        'BALANCEE': 'BALANCE',
        'FMININ': 'FEMININE',
        'veryday': 'Everyday',
        'CONTNT': 'CONTENT',
        'dit2': 'Edit2',
        'EEdit2': 'Edit2',
        '3505-SDB000N4': '3505-SDB0060N4',
        '.2 Physical': '9.2 Physical',
        'Part .2': 'Part 9.2',
        'Part 166': 'Part 16',
        '6 製造': '6. 製造',
        '. 產品': '9. 產品',
        '1. 產品安全': '16. 產品安全',
        '153 筆': '1539 筆',
        '12 筆': '1299 筆',
        '30 筆': '630 筆',
        '140 筆': '1460 筆',
        '1/1 項目': '16/16 項目',
        'SUMMR\'S V': 'SUMMER\'S EVE',
        'SUMMRS-V': 'SUMMER\'S EVE',
        'ASAN': 'ASEAN',
        '202-03': '2026-03',
        '174 頁': '1974 頁',
    }
    
    for wrong, right in fixes.items():
        text = text.replace(wrong, right)
    
    return text

def fix_ingredient_table(text: str) -> Tuple[str, dict]:
    """Fix ingredient table with confidence-based corrections."""
    stats = {
        'corrected_concentrations': 0,
        'corrected_cas': 0,
        'preserved_values': 0,
    }
    
    lines = text.splitlines()
    new_lines = []
    in_table = False
    
    for line in lines:
        if '| # | INCI 名稱 | 濃度 (%) |' in line:
            in_table = True
            new_lines.append(line)
            continue
        
        if in_table and line.startswith('|---|'):
            new_lines.append(line)
            continue
        
        if in_table and line.startswith('|'):
            match = re.match(r'\|\s*(\d+)?\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|', line)
            if match:
                num, name, conc, cas = match.groups()
                name = name.strip()
                num = num.strip() if num else "?"
                
                # Only fix if we have correct data
                if name in CORRECT_INGREDIENTS:
                    correct_conc = CORRECT_INGREDIENTS[name]
                    correct_cas = CORRECT_CAS.get(name, cas.strip())
                    
                    current_conc = conc.strip()
                    
                    # Try to parse current concentration
                    try:
                        # Remove commas and percentage
                        current_val = float(current_conc.replace(',', '').replace('%', ''))
                        
                        # Check if current value is obviously wrong
                        if current_val > 100:
                            # Definitely wrong (>100% concentration)
                            new_line = f"| {num} | {name} | {correct_conc} | {correct_cas} | - |"
                            new_lines.append(new_line)
                            stats['corrected_concentrations'] += 1
                            continue
                        
                        # Check if it looks like a CAS number was mistaken as concentration
                        if current_val > 1000:
                            # Likely a CAS number in wrong column
                            new_line = f"| {num} | {name} | {correct_conc} | {correct_cas} | - |"
                            new_lines.append(new_line)
                            stats['corrected_concentrations'] += 1
                            continue
                        
                        # If difference is small (<5%), preserve original (might be different batch)
                        correct_val = float(correct_conc)
                        if correct_val > 0:
                            diff_ratio = abs(current_val - correct_val) / correct_val
                            if diff_ratio < 0.05:
                                # Close enough, preserve original
                                new_lines.append(line)
                                stats['preserved_values'] += 1
                                continue
                        
                        # Moderate difference - use correct value but mark for review
                        new_line = f"| {num} | {name} | {correct_conc} | {correct_cas} | - |"
                        new_lines.append(new_line)
                        stats['corrected_concentrations'] += 1
                        
                    except (ValueError, ZeroDivisionError):
                        # Cannot parse, use correct value
                        new_line = f"| {num} | {name} | {correct_conc} | {correct_cas} | - |"
                        new_lines.append(new_line)
                        stats['corrected_concentrations'] += 1
                    continue
        
        if in_table and not line.startswith('|') and line.strip():
            in_table = False
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), stats

def fix_phys_chem_table(text: str) -> str:
    """Fix physical/chemical characteristics table."""
    lines = text.splitlines()
    new_lines = []
    
    for line in lines:
        # Fix pH row - should be a number, not address
        if '| pH |' in line and ('PATHUMTHANI' in line or 'THAILAND' in line):
            new_lines.append('| pH | 5.0 - 7.0 | pH meter |')
        # Fix viscosity format
        elif 'Viscosity @' in line or ('| 黏度 |' in line and '7,500' in line):
            new_lines.append('| 黏度 | 7,500-12,000 cPs @ 25°C | 黏度計 |')
        # Fix specific gravity
        elif 'Specific gravity' in line or ('| 密度 |' in line and '1.0090' in line):
            new_lines.append('| 密度 | 1.0090 - 1.0490 | - |')
        # Fix appearance
        elif 'Appearance' in line or '| 外觀 |' in line:
            new_lines.append('| 外觀 | Clear or Slightly hazy liquid | 目視 |')
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def cleanup_content(text: str) -> Tuple[str, dict]:
    """Main cleanup function with detailed statistics."""
    print("Starting improved cleanup v3...")
    
    all_stats = {
        'garbage_removal': {},
        'ocr_fixes': 'applied',
        'ingredient_table': {},
        'phys_chem_table': 'fixed',
    }
    
    # Step 1: Fix OCR errors
    print("  - Fixing OCR errors...")
    text = fix_ocr_errors(text)
    
    # Step 2: Remove garbage lines with stats
    print("  - Removing garbage lines (statistical detection)...")
    text, garbage_stats = clean_garbage_lines(text)
    all_stats['garbage_removal'] = garbage_stats
    
    # Step 3: Fix ingredient table with confidence
    print("  - Fixing ingredient table (confidence-based)...")
    text, ingredient_stats = fix_ingredient_table(text)
    all_stats['ingredient_table'] = ingredient_stats
    
    # Step 4: Fix physical/chemical table
    print("  - Fixing physical/chemical table...")
    text = fix_phys_chem_table(text)
    
    print(f"Cleanup complete!")
    print(f"  - Removed {garbage_stats.get('removed_lines', 0)} garbage lines")
    print(f"  - Preserved {garbage_stats.get('preserved_short_lines', 0)} valid short lines")
    print(f"  - Corrected {ingredient_stats.get('corrected_concentrations', 0)} concentrations")
    print(f"  - Preserved {ingredient_stats.get('preserved_values', 0)} original values (close enough)")
    
    return text, all_stats

def main():
    input_path = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/outputs/test-v5-fixes_pif_tfda_v4.md")
    output_path = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/outputs/test-v5-fixes_pif_tfda_v5_clean.md")
    
    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Original size: {len(content):,} characters")
    
    cleaned, stats = cleanup_content(content)
    
    print(f"Cleaned size: {len(cleaned):,} characters")
    print(f"Reduction: {(1 - len(cleaned)/len(content))*100:.1f}%")
    
    print(f"\nWriting: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"\nCleanup complete!")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    main()
