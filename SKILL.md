---
name: 台灣化妝品 PIF 檔案製作 / Taiwan Cosmetic PIF Maker
slug: taiwan-cosmetic-pif
version: 1.0.0
homepage: https://github.com/bounce12340/taiwan-cosmetic-pif
description: 將泰國/ASEAN 格式 PIF 自動轉換為台灣 TFDA 格式的 16 項目完整檔案 | Automatically convert Thai/ASEAN PIF to Taiwan TFDA 16-section format
metadata: {"clawdbot":{"emoji":"📋","os":["win32","darwin","linux"],"languages":["zh-TW","en"]}}
---

## 當使用 / When to Use

使用當：
1. 需要將泰國/ASEAN 格式 PIF 轉換為台灣 TFDA 格式
2. 需要從 PDF 萃取產品資訊並分類到 16 個 TFDA 項目
3. 需要生成結構化的 PIF Markdown 或 Word 文件
4. 需要清理 OCR 亂碼並修正成分濃度、CAS 號碼等數據

Use when:
1. Converting Thai/ASEAN PIF format to Taiwan TFDA format
2. Extracting product information from PDFs and classifying into 16 TFDA sections
3. Generating structured PIF Markdown or Word documents
4. Cleaning OCR errors and correcting ingredient concentrations, CAS numbers, etc.

---

## 核心規則 / Core Rules

### 1. TFDA 16 項目結構 / TFDA 16-Section Structure

本 Skill 嚴格遵循台灣 TFDA PIF 格式，包含 16 個項目：

This Skill strictly follows Taiwan TFDA PIF format with 16 sections:

**壹、產品敘述 (項目 1-8) / Part I: Product Description (Sections 1-8)**

| # | 中文 / Chinese | English |
|---|---------------|---------|
| 1 | 產品基本資料 | Basic Product Information |
| 2 | 產品敘述 | Product Description |
| 3 | 全成分 | Full Ingredient List |
| 4 | 產品標籤、仿單 | Product Labeling & Leaflets |
| 5 | GMP 符合證明 | GMP Compliance Certificate |
| 6 | 製造方法、流程 | Manufacturing Methods & Procedures |
| 7 | 使用方法、部位、用量、頻率及族群 | Usage Methods, Body Parts, Dosage, Frequencies, and Target Population |
| 8 | 產品使用不良反應資料 | Adverse Effects of Product Application |

**貳、品質資料 (項目 9-13) / Part II: Quality Data (Sections 9-13)**

| # | 中文 / Chinese | English |
|---|---------------|---------|
| 9 | 產品及各別成分之物理及化學特性 | Physical and Chemical Characteristics of Products and Individual Ingredients |
| 10 | 毒理學終點數據 | Toxicological Endpoint Data |
| 11 | 安定性試驗報告 | Stability Test Report |
| 12 | 微生物檢測報告 | Microbiological Test Report |
| 13 | 防腐挑戰測試 | Preservative Challenge Test |

**肆、安全評估資料 (項目 14-16) / Part IV: Safety Assessment Data (Sections 14-16)**

| # | 中文 / Chinese | English |
|---|---------------|---------|
| 14 | 功能評估佐證資料 | Supporting Information for Functional Assessments |
| 15 | 包裝相容性資料 | Packaging Compatibility Data |
| 16 | 產品安全資料（含簽署人員簽名） | Product Safety Information (with Assessor's Signature) |

---

### 2. PDF 處理流程 / PDF Processing Workflow

```
PDF 輸入 → OCR 文字萃取 → 清理亂碼 → 分類到 16 項目 → 結構化輸出
PDF Input → OCR Text Extraction → Clean Garbage → Classify to 16 Sections → Structured Output
```

**OCR 選項 / OCR Options:**
- 預設 / Default: `pypdf` (快速，適合已 OCR 的 PDF | Fast, suitable for pre-OCR'd PDFs)
- 可選 / Optional: `PaddleOCR` (更準確，支援泰文，但需要額外安裝 | More accurate, supports Thai, but requires additional installation)

---

### 3. 數據修正規則 / Data Correction Rules

**成分濃度修正 / Ingredient Concentration Corrections:**

| INCI 名稱 | 濃度 (%) | Function / 功能 |
|-----------|---------|----------------|
| Aqua (Water) | 85.7474 | Solvent / 溶劑 |
| Sodium Laureth Sulfate | 7.1775 | Cleansing, Foaming / 清潔、發泡 |
| Sodium Chloride | 3.5900 | Viscosity Controlling / 黏度控制 |
| Cocamidopropyl Betaine | 1.2375 | Cleansing, Foaming Boosting / 清潔、發泡促進 |
| Lauryl Glucoside | 1.2375 | Cleansing, Surfactant / 清潔、界面活性劑 |
| Lactic Acid | 0.3600 | Buffering, Humectant / 緩衝、保濕 |
| Disodium EDTA | 0.2000 | Chelating / 螯合 |
| Sodium Benzoate | 0.2000 | Preservative / 防腐 |
| Parfum (Fragrance) | 0.1000 | Perfuming / 香精 |
| Alpha-Glucan Oligosaccharide | 0.0500 | Skin Conditioning / 皮膚調理 |
| Polyquaternium-7 | 0.0500 | Antistatic, Film Forming / 抗靜電、成膜 |
| Sodium Hydroxide | 0.0001 | Buffering / 緩衝 |
| Limonene | 0.0907 | Perfuming (EU Allergen) / 香精 (歐盟過敏原) |
| Linalool | 0.0007 | Perfuming (EU Allergen) / 香精 (歐盟過敏原) |
| Citronellol | 0.0004 | Perfuming (EU Allergen) / 香精 (歐盟過敏原) |

**CAS 號碼修正 / CAS Number Corrections:**

| Ingredient | CAS No. |
|------------|---------|
| Aqua | 7732-18-5 |
| Sodium Laureth Sulfate | 9004-82-4 |
| Sodium Chloride | 7647-14-5 |
| Cocamidopropyl Betaine | 97862-59-4 |
| Lauryl Glucoside | 110615-47-9 |
| Lactic Acid | 50-21-5 |
| Disodium EDTA | 139-33-3 |
| Sodium Benzoate | 532-32-1 |
| Polyquaternium-7 | 26590-05-6 |
| Sodium Hydroxide | 1310-73-2 |
| Limonene | 138-86-3 |
| Linalool | 78-70-6 |
| Citronellol | 106-22-9 |

---

### 4. 亂碼清理規則 / Garbage Cleanup Rules

**移除項目 / Remove:**
- 中文 OCR 亂碼（如：曬鼉、呱黷、衊蛐等）| Chinese OCR garbage characters
- 頁碼和頁首尾（如：Page X of Y, UNCONTROLLED WHEN PRINTED）| Page numbers and headers/footers
- 重複內容（連續相同行）| Duplicate content (consecutive identical lines)

**修正項目 / Correct:**
- OCR 拼寫錯誤（Fem inine → Feminine, appltto → apply to）
- 數字格式（200C → 20°C, 250C → 25°C）
- 物理化學數據（pH 值、黏度、密度等）| Physical/chemical data (pH, viscosity, density, etc.)

---

## 使用方式 / Usage

### 基本用法 / Basic Usage

```bash
python scripts/pif_converter_v4.py <輸入 PDF 資料夾 / Input PDF Folder> [產品名稱 / Product Name]
```

### 範例 / Examples

```bash
# 處理 Summers Eve 產品 / Process Summers Eve products
python scripts/pif_converter_v4.py "C:/PIF/summers-eve" summers-eve

# 輸出位置 / Output location
outputs/summers-eve_pif_tfda_v4.md
```

### 清理亂碼 / Clean Garbage

```bash
python scripts/cleanup_pif_v2.py <輸入 MD 檔 / Input MD File>
```

### 使用 PaddleOCR（可選） / Using PaddleOCR (Optional)

```bash
# 安裝依賴 / Install dependencies
pip install paddlepaddle paddleocr pymupdf

# 執行 OCR / Run OCR
python scripts/pif_paddleocr.py
```

---

## 輸出格式 / Output Format

### Markdown 輸出 / Markdown Output

- **檢查清單表格** - 16 項目的完成狀態 / Checklist table - Completion status of 16 sections
- **成分表** - INCI 名稱、濃度、CAS No.、功能 / Ingredient table - INCI name, concentration, CAS No., function
- **微生物檢測表** - 檢測項目、結果、標準 / Microbiology table - Test items, results, standards
- **物理化學表** - pH、黏度、密度、外觀 / Physicochemical table - pH, viscosity, density, appearance
- **參考文獻** - CIR、SCCS、ISO 等連結 / References - Links to CIR, SCCS, ISO, etc.

### Word 輸出（可選） / Word Output (Optional)

使用 `word-docx` skill 轉換為 .docx 格式：

Use `word-docx` skill to convert to .docx format:

```bash
clawhub install word-docx
# 然後使用 word-docx skill 轉換 / Then use word-docx skill to convert
```

---

## 檔案結構 / File Structure

```
taiwan-cosmetic-pif/
├── SKILL.md                      # Skill 說明文件 / Skill documentation
├── README.md                     # 使用說明 / User guide
├── requirements.txt              # Python 依賴 / Python dependencies
├── scripts/
│   ├── pif_converter_v4.py       # 主要轉換腳本 / Main converter script
│   ├── cleanup_pif_v2.py         # 亂碼清理腳本 / Garbage cleanup script
│   └── pif_paddleocr.py          # PaddleOCR 腳本 / PaddleOCR script (optional)
└── outputs/
    └── <product>_pif_tfda_v4.md  # 輸出檔案 / Output file
```

---

## 依賴 / Dependencies

- Python 3.11+
- pypdf
- python-docx（可選，用於 Word 輸出 / Optional, for Word output）
- pymupdf（可選，用於 PDF 轉圖片 / Optional, for PDF to image conversion）
- paddlepaddle, paddleocr（可選，用於高品質 OCR / Optional, for high-quality OCR）

---

## 注意事項 / Notes

1. **PDF 品質 / PDF Quality**: 建議先使用 Adobe Acrobat 進行 OCR 處理，設定語言為 Thai + English  
   Recommended to use Adobe Acrobat for OCR first, set language to Thai + English

2. **成分濃度 / Ingredient Concentrations**: 自動修正為正確值，但建議人工確認  
   Automatically corrected, but manual verification is recommended

3. **安全評估 / Safety Assessment**: 項目 16 需要合格安全評估人員簽署  
   Section 16 requires signature by qualified safety assessor

4. **手動補充 / Manual Completion**: 部分項目（如毒理學、安定性）可能需要人工補充完整數據  
   Some sections (e.g., toxicology, stability) may require manual data completion

---

## 相關 Skill / Related Skills

- `word-docx` - 轉換為 Word (.docx) 格式 / Convert to Word (.docx) format
- `pdf-text-extractor` - PDF 文字萃取 / PDF text extraction
- `documents` - 一般文件處理 / General document handling

---

## 反饋 / Feedback

- 問題回報 / Issue Report: https://github.com/bounce12340/taiwan-cosmetic-pif/issues
- 更新 / Updates: `clawhub sync taiwan-cosmetic-pif`

---

## 授權 / License

MIT License

## 版本歷史 / Version History

- **v1.0.0** (2026-03-31): Initial release with bilingual support (Chinese/English)
