# 台灣化妝品 PIF 檔案製作 Skill
# Taiwan Cosmetic PIF Maker Skill

將泰國/ASEAN 格式 PIF 自動轉換為台灣 TFDA 格式的完整工具

Automatically convert Thai/ASEAN PIF to Taiwan TFDA format

[![GitHub](https://img.shields.io/github/v/release/bounce12340/taiwan-cosmetic-pif)](https://github.com/bounce12340/taiwan-cosmetic-pif)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Languages](https://img.shields.io/badge/languages-中文%2CEnglish-green)](README.md)

---

## 功能特色 / Features

- ✅ **自動轉換** - 泰國 PIF → 台灣 TFDA 16 項目  
  **Auto Conversion** - Thai PIF → Taiwan TFDA 16 sections

- ✅ **PDF OCR** - 支援大檔案（200MB+）處理  
  **PDF OCR** - Supports large files (200MB+)

- ✅ **結構化輸出** - Markdown 表格格式  
  **Structured Output** - Markdown table format

- ✅ **亂碼清理** - 自動移除 OCR 錯誤和中文亂碼  
  **Garbage Cleanup** - Auto-remove OCR errors and Chinese garbage

- ✅ **數據修正** - 自動修正成分濃度、CAS 號碼  
  **Data Correction** - Auto-correct ingredient concentrations, CAS numbers

- ✅ **檢查清單** - 16 項目的完成狀態追蹤  
  **Checklist** - Track completion status of 16 sections

---

## 安裝 / Installation

```bash
# 使用 clawhub 安裝 / Install with clawhub
clawhub install bounce12340/taiwan-cosmetic-pif

# 或手動複製 skill 資料夾 / Or manually copy skill folder
# 到 / to ~/.openclaw/workspace/skills/
```

---

## 快速開始 / Quick Start

### 1. 準備 PDF 檔案 / Prepare PDF Files

將泰國 PIF PDF 檔案放在同一個資料夾中：

Place Thai PIF PDF files in the same folder:

```
inputs/
├── product1.pdf
├── product2.pdf
└── product3.pdf
```

### 2. 執行轉換 / Run Conversion

```bash
python scripts/pif_converter_v4.py "inputs/" product-name
```

### 3. 查看輸出 / View Output

```
outputs/
└── product-name_pif_tfda_v4.md
```

---

## TFDA 16 項目 / TFDA 16 Sections

本 Skill 遵循台灣 TFDA PIF 格式，包含 16 個項目：

This Skill follows Taiwan TFDA PIF format with 16 sections:

### 壹、產品敘述 (1-8) / Part I: Product Description (1-8)

| # | 中文 / Chinese | English |
|---|---------------|---------|
| 1 | 產品基本資料 | Basic Product Information |
| 2 | 產品敘述 | Product Description |
| 3 | 全成分 | Full Ingredient List |
| 4 | 產品標籤、仿單 | Product Labeling & Leaflets |
| 5 | GMP 符合證明 | GMP Compliance Certificate |
| 6 | 製造方法、流程 | Manufacturing Methods & Procedures |
| 7 | 使用方法、部位、用量、頻率及族群 | Usage Methods, Body Parts, Dosage, Frequencies, Target Population |
| 8 | 產品使用不良反應資料 | Adverse Effects of Product Application |

### 貳、品質資料 (9-13) / Part II: Quality Data (9-13)

| # | 中文 / Chinese | English |
|---|---------------|---------|
| 9 | 產品及各別成分之物理及化學特性 | Physical and Chemical Characteristics |
| 10 | 毒理學終點數據 | Toxicological Endpoint Data |
| 11 | 安定性試驗報告 | Stability Test Report |
| 12 | 微生物檢測報告 | Microbiological Test Report |
| 13 | 防腐挑戰測試 | Preservative Challenge Test |

### 肆、安全評估資料 (14-16) / Part IV: Safety Assessment (14-16)

| # | 中文 / Chinese | English |
|---|---------------|---------|
| 14 | 功能評估佐證資料 | Supporting Information for Functional Assessments |
| 15 | 包裝相容性資料 | Packaging Compatibility Data |
| 16 | 產品安全資料（含簽署人員簽名） | Product Safety Information (with Assessor's Signature) |

---

## 輸出範例 / Output Examples

### 成分表 / Ingredient Table

```markdown
| # | INCI 名稱 | 濃度 (%) | CAS No. | 功能 |
|---|----------|---------|---------|------|
| 1 | Aqua (Water) | 85.7474 | 7732-18-5 | Solvent |
| 2 | Sodium Laureth Sulfate | 7.1775 | 9004-82-4 | Cleansing |
| 3 | Sodium Chloride | 3.5900 | 7647-14-5 | Viscosity |
```

### 微生物檢測 / Microbiology Test

```markdown
| 檢測項目 / Test Item | 結果 / Result | 標準 / Standard |
|----------|------|------|
| 總菌數 / Total Bacteria | ≤100 CFU/g | ≤100 CFU/g |
| 黴菌/酵母菌 / Yeast & Mold | ≤10 CFU/g | ≤10 CFU/g |
| 大腸桿菌 / E. coli | 未檢出 / ND | 未檢出 / ND |
```

---

## 進階用法 / Advanced Usage

### 清理亂碼 / Clean Garbage

```bash
python scripts/cleanup_pif_v2.py outputs/product-name_pif_tfda_v4.md
```

### 使用 PaddleOCR（高品質） / Using PaddleOCR (High Quality)

```bash
# 安裝依賴 / Install dependencies
pip install paddlepaddle paddleocr pymupdf

# 執行 OCR / Run OCR
python scripts/pif_paddleocr.py
```

---

## 依賴 / Dependencies

- Python 3.11+
- pypdf
- python-docx（可選 / Optional）
- pymupdf（可選 / Optional）
- paddlepaddle, paddleocr（可選 / Optional）

---

## 注意事項 / Notes

1. **PDF 品質 / PDF Quality**: 建議先用 Adobe Acrobat 進行 OCR，設定 Thai + English  
   Recommended to use Adobe Acrobat for OCR first, set Thai + English

2. **成分濃度 / Ingredient Concentrations**: 自動修正，但建議人工確認  
   Auto-corrected, but manual verification recommended

3. **安全評估 / Safety Assessment**: 項目 16 需要合格人員簽署  
   Section 16 requires signature by qualified personnel

4. **手動補充 / Manual Completion**: 部分項目可能需要人工補充完整數據  
   Some sections may require manual data completion

---

## 相關資源 / Related Resources

- [TFDA 法規 / TFDA Regulations](https://www.fda.gov.tw/)
- [CIR Safety Assessments](https://www.cir-safety.org/)
- [EU SCCS](https://health.ec.europa.eu/scientific-committees/sccs_en)
- [ISO 22716 (GMP)](https://www.iso.org/standard/36437.html)

---

## 授權 / License

MIT License

---

## 貢獻 / Contributing

歡迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

---

## 版本歷史 / Version History

- **v1.0.0** (2026-03-31): Initial release with bilingual support (中文/English)

---

## 開發者 / Developer

- **GitHub**: [@bounce12340](https://github.com/bounce12340)
- **Repository**: https://github.com/bounce12340/taiwan-cosmetic-pif
