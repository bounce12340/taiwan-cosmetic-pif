# Taiwan Cosmetic PIF Maker 🇹🇼

<p align="center">
  <b>台灣化妝品 PIF 轉換器 | Taiwan Cosmetic PIF Converter</b>
</p>

<p align="center">
  <a href="#中文">🇹🇼 繁體中文</a> • 
  <a href="#english">🇺🇸 English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PDF-OCR-orange.svg" alt="PDF OCR">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/TFDA-Compliant-blue" alt="TFDA">
</p>

---

<a name="中文"></a>

## 🇹🇼 繁體中文

> 將泰國/ASEAN 格式 PIF **自動轉換**為台灣 TFDA 格式的完整工具

### ✨ 功能特色

- ✅ **自動轉換** - 泰國 PIF → 台灣 TFDA 16 項目
- ✅ **PDF OCR** - 支援大檔案（200MB+）處理
- ✅ **結構化輸出** - Markdown 表格格式
- ✅ **亂碼清理** - 自動移除 OCR 錯誤和亂碼
- ✅ **數據修正** - 自動修正成分濃度、CAS 號碼
- ✅ **檢查清單** - 16 項目的完成狀態追蹤

### 📋 TFDA 16 項目

**壹、產品敘述 (1-8)**
1. 產品基本資料
2. 產品敘述
3. 全成分
4. 產品標籤、仿單
5. GMP 符合證明
6. 製造方法、流程
7. 使用方法、部位、用量、頻率及族群
8. 產品使用不良反應資料

**貳、品質資料 (9-13)**
9. 物理及化學特性
10. 毒理學終點數據
11. 安定性試驗報告
12. 微生物檢測報告
13. 防腐挑戰測試

**肆、安全評估資料 (14-16)**
14. 功能評估佐證資料
15. 包裝相容性資料
16. 產品安全資料

### 🚀 快速開始

```bash
# 安裝
clawhub install bounce12340/taiwan-cosmetic-pif

# 或使用 Git
git clone https://github.com/bounce12340/taiwan-cosmetic-pif.git

# 準備 PDF 檔案
mkdir inputs/
# 放入 Thai PIF PDF

# 執行轉換
python scripts/pif_converter_v4.py "inputs/" product-name

# 查看輸出
cat outputs/product-name_pif_tfda_v4.md
```

---

<a name="english"></a>

## 🇺🇸 English

> Automatically convert Thai/ASEAN PIF to **Taiwan TFDA format** with complete 16-section structure

### ✨ Features

- ✅ **Auto Conversion** - Thai PIF → Taiwan TFDA 16 sections
- ✅ **PDF OCR** - Large files (200MB+) support
- ✅ **Structured Output** - Markdown table format
- ✅ **Data Cleaning** - Remove OCR errors and garbage
- ✅ **Auto Correction** - Fix ingredient concentrations, CAS numbers
- ✅ **Completion Tracker** - Track 16 sections status

### 📋 TFDA 16 Sections

**Part I: Product Description (1-8)**
1. Basic Product Information
2. Product Description
3. Full Ingredient List
4. Product Labeling & Leaflets
5. GMP Compliance Certificate
6. Manufacturing Methods
7. Usage, Body Parts, Dosage, Frequencies
8. Adverse Effects Data

**Part II: Quality Data (9-13)**
9. Physical and Chemical Characteristics
10. Toxicological Endpoint Data
11. Stability Test Report
12. Microbiological Test Report
13. Preservative Challenge Test

**Part III: Safety Assessment (14-16)**
14. Functional Assessment Support
15. Packaging Compatibility Data
16. Product Safety Information

### 🚀 Quick Start

```bash
# Install
clawhub install bounce12340/taiwan-cosmetic-pif

# Or use Git
git clone https://github.com/bounce12340/taiwan-cosmetic-pif.git

# Prepare PDF files
mkdir inputs/
# Put Thai PIF PDFs here

# Run conversion
python scripts/pif_converter_v4.py "inputs/" product-name

# View output
cat outputs/product-name_pif_tfda_v4.md
```

---

## 📊 Output Example / 輸出範例

### Ingredient Table / 成分表

```markdown
| # | INCI Name | Concentration (%) | CAS No. | Function |
|---|-----------|-------------------|---------|----------|
| 1 | Aqua (Water) | 85.7474 | 7732-18-5 | Solvent |
| 2 | Sodium Laureth Sulfate | 7.1775 | 9004-82-4 | Cleansing |
| 3 | Sodium Chloride | 3.5900 | 7647-14-5 | Viscosity |
```

### Microbiology Test / 微生物檢測

```markdown
| Test Item | Result | Standard |
|-----------|--------|----------|
| Total Bacteria | ≤100 CFU/g | ≤100 CFU/g |
| Yeast & Mold | ≤10 CFU/g | ≤10 CFU/g |
| E. coli | ND | ND |
```

---

## 🔧 Advanced Usage / 進階用法

### Clean OCR Garbage / 清理亂碼

```bash
python scripts/cleanup_pif_v2.py outputs/product-name_pif_tfda_v4.md
```

### High-Quality OCR (PaddleOCR) / 高品質 OCR

```bash
pip install paddlepaddle paddleocr pymupdf
python scripts/pif_paddleocr.py
```

---

## 📝 License / 授權

MIT License — See [LICENSE](LICENSE)

---

## 👤 Author / 作者

**Josh** — [@bounce12340](https://github.com/bounce12340)

---

## 🔗 Resources / 相關資源

- [TFDA 法規](https://www.fda.gov.tw/)
- [CIR Safety Assessments](https://www.cir-safety.org/)
- [EU SCCS](https://health.ec.europa.eu/scientific-committees/sccs_en)

---

<p align="center">
  Made with ❤️ for Taiwan Cosmetic Regulatory Compliance<br>
  為台灣化妝品法規合規用心打造
</p>
