# pif_converter_v4.py - Thai PIF to Taiwan TFDA PIF Converter (v4 Complete with Tables)

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
import pypdf
from pypdf.errors import PdfReadError, PdfStreamError
from datetime import datetime

# TFDA 16 Sections with full names
TFDA_SECTIONS = {
    "1": "產品基本資料",
    "2": "產品敘述", 
    "3": "全成分",
    "4": "產品標籤、仿單",
    "5": "GMP 符合證明",
    "6": "製造方法、流程",
    "7": "使用方法、部位、用量、頻率及族群",
    "8": "產品使用不良反應資料",
    "9": "產品及各別成分之物理及化學特性",
    "10": "毒理學終點數據",
    "11": "安定性試驗報告",
    "12": "微生物檢測報告",
    "13": "防腐挑戰測試",
    "14": "功能評估佐證資料",
    "15": "包裝相容性資料",
    "16": "產品安全資料（含簽署人員簽名）",
}

# Keyword mapping with pre-compiled regex for performance
MAPPING = {
    "Product Information": {"tfda": ["1", "2"], "keywords": ["product name", "category", "dosage form", "purpose"]},
    "Composition & INCI": {"tfda": ["3"], "keywords": ["composition", "inci", "ingredients", "formula", "%", "cas"]},
    "Manufacturing": {"tfda": ["6"], "keywords": ["manufacturing", "manufacture", "production", "process", "gmp"]},
    "Quality Specifications": {"tfda": ["9", "10"], "keywords": ["quality", "specification", "physical", "chemical", "ph", "viscosity"]},
    "Stability Data": {"tfda": ["11"], "keywords": ["stability", "shelf life", "expiration", "expiry", "storage", "month"]},
    "Microbiology": {"tfda": ["12", "13"], "keywords": ["microbiology", "microbial", "cfu", "bacteria", "yeast", "mold", "challenge"]},
    "Safety Assessment": {"tfda": ["15", "16"], "keywords": ["safety", "toxicology", "dermatological", "patch test", "signed", "mos"]},
    "Labeling": {"tfda": ["4"], "keywords": ["label", "labeling", "warning", "caution", "direction"]},
    "GMP Certificate": {"tfda": ["5"], "keywords": ["gmp", "good manufacturing practice", "iso 22716", "certificate"]},
    "Usage Methods": {"tfda": ["7"], "keywords": ["usage", "apply", "frequency", "body part", "dosage", "adult", "children"]},
    "Adverse Effects": {"tfda": ["8"], "keywords": ["adverse", "side effect", "reaction", "irritation", "allergic", "complaint"]},
    "Functional Assessment": {"tfda": ["14"], "keywords": ["functional", "efficacy", "claim", "study", "assessment"]},
}

# Pre-compiled regex for O(1) classification instead of O(n*m)
ALL_KEYWORDS = set()
for info in MAPPING.values():
    ALL_KEYWORDS.update(info["keywords"])

KEYWORD_PATTERN = re.compile(
    '(' + '|'.join(re.escape(kw) for kw in sorted(ALL_KEYWORDS, key=len, reverse=True)) + ')',
    re.IGNORECASE
)

# Pre-build reverse mapping: keyword -> tfda sections
KEYWORD_TO_TFDA = {}
for chapter, info in MAPPING.items():
    for keyword in info["keywords"]:
        KEYWORD_TO_TFDA[keyword.lower()] = info["tfda"]

def clean_text(text: str) -> str:
    """Clean OCR artifacts and page elements."""
    lines = text.splitlines()
    cleaned = []
    
    for line in lines:
        line = line.strip()
        
        # Skip page numbers and headers/footers
        if re.match(r'^(page \d+ of \d+|\d+/\d+|uncontrolled|do not retain|destroy after|total quality)', line.lower()):
            continue
        if re.match(r'^(ref\.? no\.?|formula code|bulk code|finished product code)', line.lower()):
            continue
            
        # Remove obvious OCR garbage
        special_ratio = sum(1 for c in line if not c.isalnum() and not c.isspace()) / max(len(line), 1)
        if special_ratio > 0.4 and len(line) < 50:
            continue
        
        # Fix common OCR errors
        line = re.sub(r'Concen tration', 'Concentration', line)
        line = re.sub(r'Produc t', 'Product', line)
        line = re.sub(r'[\u4e00-\u9fff]{1,2}[0-9]{2,3}%', lambda m: m.group().replace(' ', ''), line)
            
        cleaned.append(line)
    
    return '\n'.join(cleaned)

def extract_pdf_text_chunked(pdf_path: str, progress_callback=None) -> Tuple[str, int]:
    """Extract text from PDF page by page with robust error handling."""
    text = ""
    page_count = 0
    
    # Validate file exists
    if not Path(pdf_path).exists():
        print(f"  [ERROR] File not found: {pdf_path}")
        return "", 0
    
    try:
        print(f"  Opening: {Path(pdf_path).name}")
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            
            # Check if PDF is encrypted
            if reader.is_encrypted:
                print(f"  [WARN] PDF is encrypted, attempting to decrypt with empty password...")
                try:
                    reader.decrypt('')
                except:
                    print(f"  [ERROR] PDF requires password, cannot process")
                    return "", 0
            
            page_count = len(reader.pages)
            print(f"  Pages: {page_count}")
            
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n\n"
                    
                    if progress_callback and (i + 1) % 20 == 0:
                        progress_callback(i + 1, page_count)
                except Exception as page_error:
                    print(f"  [WARN] Failed to extract page {i+1}: {page_error}")
                    continue
                    
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {pdf_path}")
        return "", 0
    except PdfReadError as e:
        print(f"  [ERROR] Invalid or corrupt PDF: {e}")
        return "", 0
    except PdfStreamError as e:
        print(f"  [ERROR] PDF stream error: {e}")
        return "", 0
    except Exception as e:
        print(f"  [ERROR] Unexpected error: {type(e).__name__} - {e}")
        return "", 0
    
    return text, page_count

def progress_handler(current, total):
    print(f"  Progress: {current}/{total} pages ({current/total*100:.1f}%)")

def extract_ingredient_table(text: str) -> List[Dict]:
    """Extract ingredient table with concentration and CAS."""
    ingredients = []
    
    # Known cosmetic ingredients to match
    known_ingredients = [
        'Aqua', 'Water', 'Sodium Laureth Sulfate', 'Sodium Chloride',
        'Cocamidopropyl Betaine', 'Lauryl Glucoside', 'Lactic Acid',
        'Disodium EDTA', 'Sodium Benzoate', 'Parfum', 'Fragrance',
        'Alpha-Glucan Oligosaccharide', 'Polyquaternium-7', 'Sodium Hydroxide',
        'Limonene', 'Linalool', 'Citronellol', 'Glycerin', 'Propylene Glycol'
    ]
    
    # Pattern: Ingredient name followed by concentration
    for ing_name in known_ingredients:
        pattern = rf'{re.escape(ing_name)}\s*(\d+\.?\d*)%?'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            concentration = match.group(1)
            # Try to find CAS nearby
            cas_match = re.search(rf'{re.escape(ing_name)}[^\n]*(\d+-\d+)', text, re.IGNORECASE)
            cas = cas_match.group(1) if cas_match else ""
            
            ingredients.append({
                "name": ing_name,
                "concentration": concentration,
                "cas": cas
            })
    
    # Sort by concentration (highest first)
    ingredients.sort(key=lambda x: float(x['concentration']) if x['concentration'].replace('.','').isdigit() else 0, reverse=True)
    
    return ingredients[:20]  # Top 20 ingredients

def extract_microbiology_data(text: str) -> Dict:
    """Extract microbiology test results."""
    data = {
        "total_aerobic": "",
        "yeast_mold": "",
        "e_coli": "",
        "pseudomonas": "",
        "staphylococcus": "",
        "candida": ""
    }
    
    # Total aerobic
    match = re.search(r'(?:total aerobic|total count)[^\n]*(\d+|conform|pass)[^\n]*', text, re.IGNORECASE)
    if match:
        data["total_aerobic"] = match.group(0).strip()
    
    # Yeast/mold
    match = re.search(r'(?:yeast|mould|mold)[^\n]*(\d+|conform|pass|absence)[^\n]*', text, re.IGNORECASE)
    if match:
        data["yeast_mold"] = match.group(0).strip()
    
    # E. coli
    match = re.search(r'(?:escherichia|e\.? coli)[^\n]*(conform|pass|absence|negative)[^\n]*', text, re.IGNORECASE)
    if match:
        data["e_coli"] = match.group(0).strip()
    
    # Pseudomonas
    match = re.search(r'pseudomonas[^\n]*(conform|pass|absence|negative)[^\n]*', text, re.IGNORECASE)
    if match:
        data["pseudomonas"] = match.group(0).strip()
    
    # Staphylococcus
    match = re.search(r'staphylococcus[^\n]*(conform|pass|absence|negative)[^\n]*', text, re.IGNORECASE)
    if match:
        data["staphylococcus"] = match.group(0).strip()
    
    # Candida
    match = re.search(r'candida[^\n]*(conform|pass|absence|negative)[^\n]*', text, re.IGNORECASE)
    if match:
        data["candida"] = match.group(0).strip()
    
    return data

def extract_physical_chemical(text: str) -> Dict:
    """Extract physical/chemical characteristics."""
    data = {
        "ph": "",
        "viscosity": "",
        "density": "",
        "appearance": "",
        "color": "",
        "odor": ""
    }
    
    # pH
    match = re.search(r'p[^\n]*(\d+\.?\d*)[^\n]*', text, re.IGNORECASE)
    if match:
        data["ph"] = match.group(0).strip()[:100]
    
    # Viscosity
    match = re.search(r'viscosity[^\n]*(\d+\.?\d*)[^\n]*(?:cps|mpa\.s|pa\.s)?[^\n]*', text, re.IGNORECASE)
    if match:
        data["viscosity"] = match.group(0).strip()[:100]
    
    # Density/Specific gravity
    match = re.search(r'(?:density|specific gravity)[^\n]*(\d+\.?\d*)[^\n]*', text, re.IGNORECASE)
    if match:
        data["density"] = match.group(0).strip()[:100]
    
    # Appearance
    match = re.search(r'(?:appearance|color|colour|odor|odour)[^\n]*(?:clear|liquid|white|transparent|fragrant)[^\n]*', text, re.IGNORECASE)
    if match:
        data["appearance"] = match.group(0).strip()[:100]
    
    return data

def extract_stability_data(text: str) -> List[str]:
    """Extract stability test data."""
    stability = []
    
    # Look for stability-related content
    pattern = r'(?:stability|shelf.?life|accelerated|long term|month|year|temperature|storage)[^\n]*(?:\d+|stable|conform|pass)[^\n]*'
    
    for match in re.finditer(pattern, text, re.IGNORECASE):
        line = match.group(0).strip()
        if len(line) > 20 and line not in stability:
            stability.append(line)
    
    return stability[:15]

def classify_content(text: str) -> Dict[str, List[str]]:
    """Classify content to TFDA sections using optimized O(n) algorithm."""
    tfda_content = {num: [] for num in TFDA_SECTIONS.keys()}
    
    lines = text.splitlines()
    current_sections = []
    buffer = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # O(1) classification using pre-compiled regex
        detected = []
        matches = KEYWORD_PATTERN.finditer(line_stripped.lower())
        for match in matches:
            keyword = match.group(1).lower()
            if keyword in KEYWORD_TO_TFDA:
                detected.extend(KEYWORD_TO_TFDA[keyword])
        
        if detected and detected != current_sections:
            if buffer and current_sections:
                content = '\n'.join(buffer[-30:])  # Last 30 lines
                for sec in set(current_sections):
                    if sec in tfda_content and content not in tfda_content[sec]:
                        tfda_content[sec].append(clean_text(content))
            buffer = []
            current_sections = list(set(detected))
        
        buffer.append(line)
    
    # Save remaining
    if buffer and current_sections:
        content = '\n'.join(buffer[-30:])
        for sec in set(current_sections):
            if sec in tfda_content and content not in tfda_content[sec]:
                tfda_content[sec].append(clean_text(content))
    
    return tfda_content

def generate_markdown_v4(tfda_content: Dict[str, List[str]], ingredients: List[Dict], 
                         micro_data: Dict, phys_chem: Dict, stability: List[str],
                         output_path: str, project_name: str, total_pages: int, total_chars: int):
    """Generate TFDA PIF Markdown v4 with tables and checklist."""
    
    md = f"""# TFDA PIF 文件 - {project_name.upper()}

**生成時間：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**來源：** 泰國 PIF (ASEAN Format) → 台灣 TFDA 格式轉換 (v4 完整版)  
**統計：** 共 {total_pages} 頁 / {total_chars:,} 字元  
**檔案：** {Path(output_path).name}

---

## 📋 PIF 完成狀態檢查清單

| 項目 | 狀態 | 內容筆數 | 說明 |
|------|------|----------|------|
"""
    
    filled_count = 0
    for num in sorted(TFDA_SECTIONS.keys(), key=int):
        section_name = TFDA_SECTIONS[num]
        contents = tfda_content.get(num, [])
        
        # Check if we have specific extracted data
        has_data = len(contents) > 0
        if num == "3" and ingredients:
            has_data = True
        if num == "12" and any(v for v in micro_data.values()):
            has_data = True
        if num == "9" and any(v for v in phys_chem.values()):
            has_data = True
        if num == "11" and stability:
            has_data = True
        
        status = "✅" if has_data else "⏳"
        if has_data:
            filled_count += 1
        
        md += f"| {num}. {section_name[:15]}{'...' if len(section_name) > 15 else ''} | {status} | {len(contents)} 筆 | {'已填充' if has_data else '待補充'} |\n"
    
    md += f"""
**總計：** {filled_count}/16 項目 ({filled_count/16*100:.0f}%)

---

"""
    
    # Generate each section
    for num in sorted(TFDA_SECTIONS.keys(), key=int):
        section_name = TFDA_SECTIONS[num]
        md += f"## {num}. {section_name}\n\n"
        
        contents = tfda_content.get(num, [])
        
        # Special handling for specific sections
        if num == "3" and ingredients:
            md += "### 成分表\n\n"
            md += "| # | INCI 名稱 | 濃度 (%) | CAS No. | 功能 |\n"
            md += "|---|----------|---------|---------|------|\n"
            for i, ing in enumerate(ingredients, 1):
                md += f"| {i} | {ing['name']} | {ing['concentration']} | {ing['cas']} | - |\n"
            md += "\n"
        
        if num == "9" and any(v for v in phys_chem.values()):
            md += "### 物理化學特性\n\n"
            md += "| 項目 | 結果 | 測試方法 |\n"
            md += "|------|------|----------|\n"
            if phys_chem.get("ph"):
                md += f"| pH | {phys_chem['ph'][:50]} | pH meter |\n"
            if phys_chem.get("viscosity"):
                md += f"| 黏度 | {phys_chem['viscosity'][:50]} | 黏度計 |\n"
            if phys_chem.get("density"):
                md += f"| 密度 | {phys_chem['density'][:50]} | - |\n"
            if phys_chem.get("appearance"):
                md += f"| 外觀 | {phys_chem['appearance'][:50]} | 目視 |\n"
            md += "\n"
        
        if num == "12" and any(v for v in micro_data.values()):
            md += "### 微生物檢測結果\n\n"
            md += "| 檢測項目 | 結果 | 標準 |\n"
            md += "|----------|------|------|\n"
            if micro_data.get("total_aerobic"):
                md += f"| 總菌數 | {micro_data['total_aerobic'][:60]} | ≤100 CFU/g |\n"
            if micro_data.get("yeast_mold"):
                md += f"| 黴菌/酵母菌 | {micro_data['yeast_mold'][:60]} | ≤10 CFU/g |\n"
            if micro_data.get("e_coli"):
                md += f"| 大腸桿菌 | {micro_data['e_coli'][:60]} | 未檢出 |\n"
            if micro_data.get("pseudomonas"):
                md += f"| 綠膿桿菌 | {micro_data['pseudomonas'][:60]} | 未檢出 |\n"
            if micro_data.get("staphylococcus"):
                md += f"| 金黃色葡萄球菌 | {micro_data['staphylococcus'][:60]} | 未檢出 |\n"
            if micro_data.get("candida"):
                md += f"| 白色念珠菌 | {micro_data['candida'][:60]} | 未檢出 |\n"
            md += "\n"
        
        if num == "11" and stability:
            md += "### 安定性測試結果\n\n"
            for i, item in enumerate(stability, 1):
                md += f"{i}. {item}\n"
            md += "\n"
        
        # General content
        if contents:
            for i, content in enumerate(contents[:5], 1):
                if len(content) > 50:
                    md += f"### {num}.{i}\n{content[:2000]}\n\n"
        elif not (num in ["3"] and ingredients or num in ["12"] and any(v for v in micro_data.values())):
            md += "*(待補充 / To be added)*\n\n"
        
        md += "---\n\n"
    
    # References
    md += f"""## 📚 參考文獻

| 來源 | 連結 |
|------|------|
| PubChem | https://pubchem.ncbi.nlm.nih.gov/ |
| US CIR | https://www.cir-safety.org/ |
| EU SCCS | https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en |
| ISO 22716 (GMP) | https://www.iso.org/standard/36437.html |
| ISO 11930 | https://www.iso.org/standard/46838.html |

---

## 📝 備註

- 本文件由自動化工具從泰國 PIF 轉換生成
- 部分項目可能需要人工補充完整
- 建議由合格安全評估人員審查後簽署
- 最後更新：{datetime.now().strftime('%Y-%m-%d')}

"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"\n[OK] Markdown generated: {output_path}")
    print(f"    File size: {Path(output_path).stat().st_size / 1024:.1f} KB")
    print(f"    Filled sections: {filled_count}/16 ({filled_count/16*100:.0f}%)")

def main(input_dir: str, project_name: str = "summers-eve", output_dir: str = None):
    print("=" * 60)
    print("PIF Converter v4: Thailand -> Taiwan TFDA (Complete with Tables)")
    print("=" * 60)
    
    # Validate input directory
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"[ERROR] Input directory not found: {input_path}")
        return
    
    # Parameterized output directory
    if output_dir is None:
        output_dir = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/outputs")
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for PDF files
    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        print(f"[ERROR] No PDF files found in: {input_path}")
        return
    
    print(f"\n[INPUT] Found {len(pdf_files)} PDF files")
    
    all_text = ""
    total_pages = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        print(f"    Size: {pdf_file.stat().st_size / (1024*1024):.1f} MB")
        text, pages = extract_pdf_text_chunked(str(pdf_file), progress_handler)
        all_text += text + "\n\n"
        total_pages += pages
        print(f"    Extracted: {len(text):,} characters")
    
    print(f"\n[TOTAL] Pages: {total_pages} | Characters: {len(all_text):,}")
    
    print("\n[EXTRACT] Extracting structured data...")
    
    # Extract ingredients
    print("  - Ingredients table...")
    ingredients = extract_ingredient_table(all_text)
    print(f"    Found {len(ingredients)} ingredients")
    
    # Extract microbiology
    print("  - Microbiology data...")
    micro_data = extract_microbiology_data(all_text)
    print(f"    Found {sum(1 for v in micro_data.values() if v)} test results")
    
    # Extract physical/chemical
    print("  - Physical/chemical data...")
    phys_chem = extract_physical_chemical(all_text)
    print(f"    Found {sum(1 for v in phys_chem.values() if v)} characteristics")
    
    # Extract stability
    print("  - Stability data...")
    stability = extract_stability_data(all_text)
    print(f"    Found {len(stability)} stability records")
    
    print("\n[CLASSIFY] Classifying content to TFDA sections...")
    tfda_content = classify_content(all_text)
    
    output_path = output_dir / f"{project_name}_pif_tfda_v4.md"
    
    print("\n[MD] Generating Markdown v4...")
    generate_markdown_v4(tfda_content, ingredients, micro_data, phys_chem, stability, 
                         str(output_path), project_name, total_pages, len(all_text))
    
    # Optional: Run cleanup if cleanup script exists
    cleanup_script = Path(__file__).parent / "cleanup_pif_v3.py"
    if cleanup_script.exists():
        print("\n[CLEARUP] Running cleanup_pif_v3.py...")
        import subprocess
        result = subprocess.run(
            ["python", str(cleanup_script), str(output_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  Cleanup output: {result.stdout[:200]}")
        else:
            print(f"  Cleanup error: {result.stderr[:200]}")
    
    print("\n" + "=" * 60)
    print("Conversion Complete!")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pif_converter_v4.py <input_dir> [project_name]")
        sys.exit(1)
    
    project = sys.argv[2] if len(sys.argv) > 2 else "summers-eve"
    main(sys.argv[1], project)
