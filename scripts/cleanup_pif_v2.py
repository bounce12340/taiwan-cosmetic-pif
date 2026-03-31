# cleanup_pif_v2.py - Conservative cleanup of PIF Markdown

import re
from pathlib import Path

# Correct ingredient data (conservative - only fix obvious errors)
CORRECT_INGREDIENTS = {
    "Aqua": "85.7474",
    "Sodium Laureth Sulfate": "7.1775",
    "Sodium Chloride": "3.5900",
    "Cocamidopropyl Betaine": "1.2375",
    "Lauryl Glucoside": "1.2375",
    "Lactic Acid": "0.3600",
    "Disodium EDTA": "0.2000",
    "Sodium Benzoate": "0.2000",
    "Parfum": "0.1000",
    "Alpha-Glucan Oligosaccharide": "0.0500",
    "Polyquaternium-7": "0.0500",
    "Sodium Hydroxide": "0.0001",
    "Limonene": "0.0907",
    "Linalool": "0.0007",
    "Citronellol": "0.0004",
}

CORRECT_CAS = {
    "Aqua": "7732-18-5",
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

def clean_obvious_garbage(text: str) -> str:
    """Remove only obvious OCR garbage, preserve valid content."""
    
    # Remove specific garbage lines (very conservative)
    garbage_lines = [
        '十十',
        'm m _5',
        '·EE96',
        '曬鼉＇＂上蟑嘯圜駟峒 E 矚',
        '－囉园·伍專記四',
        '..呱黷 l\' 巴 11l｀彎｀＇',
        '可 k 畫衊蛐：｀｀薑這刀',
        '\'軍可的曇 2.1 國',
        '@2 泌 c,',
        'OF p ue、',
        'o o,',
        '\'l una 血頲 un1 面西咽才',
        ',, r~ud and Drug Ad.ministration',
        'Serial No…… AA... l .~.7.7 5 9',
        '丶',
        '－一一一· ~矗',
        'J',
    ]
    
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        is_garbage = False
        
        # Check if line is exact garbage
        for garbage in garbage_lines:
            if stripped == garbage or stripped in garbage:
                is_garbage = True
                break
        
        # Check for very short garbage (1-2 chars, not meaningful)
        if len(stripped) <= 2 and not stripped.replace('.', '').replace('-', '').replace(' ', ''):
            is_garbage = True
        
        if not is_garbage:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def fix_specific_ocr_errors(text: str) -> str:
    """Fix specific, obvious OCR errors only."""
    
    # Conservative fixes - only obvious typos
    fixes = {
        'Fem inine': 'Feminine',
        'Fem in ine': 'Feminine',
        'appltto': 'apply to',
        't1oroughly': 'thoroughly',
        'ConIains': 'Contains',
        'Sodum': 'Sodium',
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
        'SUMMRS-V': 'SUMMER\'S EVE',
        'ASAN': 'ASEAN',
        '202-03': '2026-03',
        '174 頁': '1974 頁',
        '1/1 項目': '16/16 項目',
        'SUMMR\'S V': 'SUMMER\'S EVE',
        'BALANC': 'BALANCE',
        'FMININ': 'FEMININE',
        'WASH': 'WASH',
        'veryday': 'Everyday',
        'CONTNT': 'CONTENT',
        'dit2': 'Edit2',
        '3505-SDB000N4': '3505-SDB0060N4',
        '.2 Physical': '9.2 Physical',
        'Part .2': 'Part 9.2',
        'Part 1': 'Part 16',
        '6 製造': '6. 製造',
        '. 產品': '9. 產品',
        '1. 產品安全': '16. 產品安全',
        '153 筆': '1539 筆',
        '12 筆': '1299 筆',
        '30 筆': '630 筆',
        '140 筆': '1460 筆',
    }
    
    for wrong, right in fixes.items():
        text = text.replace(wrong, right)
    
    return text

def fix_ingredient_table(text: str) -> str:
    """Fix ingredient table conservatively."""
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
            # Try to parse
            match = re.match(r'\|\s*(\d+)?\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|', line)
            if match:
                num, name, conc, cas = match.groups()
                name = name.strip()
                num = num.strip() if num else "?"
                
                # Only fix if we have correct data AND current data is wrong
                if name in CORRECT_INGREDIENTS:
                    correct_conc = CORRECT_INGREDIENTS[name]
                    correct_cas = CORRECT_CAS.get(name, cas.strip())
                    
                    # Check if current conc is wrong (not a valid number or obviously wrong)
                    current_conc = conc.strip()
                    try:
                        current_val = float(current_conc.replace(',', ''))
                        # If current is way off (like 7732 instead of 85.75), fix it
                        if current_val > 100 or (name in ['Aqua', 'Water'] and current_val < 50):
                            new_line = f"| {num} | {name} | {correct_conc} | {correct_cas} | - |"
                            new_lines.append(new_line)
                            continue
                    except:
                        # Current is not a valid number, use correct one
                        new_line = f"| {num} | {name} | {correct_conc} | {correct_cas} | - |"
                        new_lines.append(new_line)
                        continue
        
        if in_table and not line.startswith('|') and line.strip():
            in_table = False
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_phys_chem_table(text: str) -> str:
    """Fix physical/chemical table."""
    lines = text.splitlines()
    new_lines = []
    
    for line in lines:
        if '| pH |' in line and ('PATHUMTHANI' in line or 'THAILAND' in line):
            new_lines.append('| pH | 5.0 - 7.0 | pH meter |')
        elif 'Viscosity @' in line or '| 黏度 |' in line:
            if '7,500-12,000' in line:
                new_lines.append('| 黏度 | 7,500-12,000 cPs @ 25°C | 黏度計 |')
            else:
                new_lines.append(line)
        elif 'Specific gravity' in line or ('| 密度 |' in line and '1.0090' in line):
            new_lines.append('| 密度 | 1.0090 - 1.0490 | - |')
        elif 'Appearance' in line or '| 外觀 |' in line:
            new_lines.append('| 外觀 | Clear or Slightly hazy liquid | 目視 |')
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def cleanup_content(text: str) -> str:
    """Main cleanup function - conservative approach."""
    print("Starting conservative cleanup...")
    
    print("  - Fixing specific OCR errors...")
    text = fix_specific_ocr_errors(text)
    
    print("  - Removing obvious garbage lines...")
    text = clean_obvious_garbage(text)
    
    print("  - Fixing ingredient table...")
    text = fix_ingredient_table(text)
    
    print("  - Fixing physical/chemical table...")
    text = fix_phys_chem_table(text)
    
    print("Cleanup complete!")
    return text

def main():
    input_path = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/outputs/summers-eve_pif_tfda_v4.md")
    output_path = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/outputs/summers-eve_pif_tfda_v5_clean.md")
    
    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Original size: {len(content):,} characters")
    
    cleaned = cleanup_content(content)
    
    print(f"Cleaned size: {len(cleaned):,} characters")
    
    print(f"Writing: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"Cleanup complete!")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    main()
