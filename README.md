# Taiwan Cosmetic PIF Maker 🇹🇼

<p align="center">
  <b>台灣化妝品 PIF 轉換器 | Taiwan Cosmetic PIF Converter | 台湾化妆品 PIF 转换器</b>
</p>

<p align="center">
  <a href="#english">🇺🇸 English</a> • 
  <a href="#繁體中文">🇹🇼 繁體中文</a> • 
  <a href="#简体中文">🇨🇳 简体中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PDF-OCR-orange.svg" alt="PDF OCR">
  <img src="https://img.shields.io/badge/TFDA-Compliant-blue" alt="TFDA">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

<a name="english"></a>
## 🇺🇸 English

> Automatically convert Thai/ASEAN PIF to **Taiwan TFDA 16-section format** with complete regulatory compliance.

### ✨ Features

- ✅ **Auto Conversion** — Thai PIF → Taiwan TFDA 16 sections
- ✅ **PDF OCR** — Large files (200MB+) support
- ✅ **Structured Output** — Markdown table format
- ✅ **Data Cleaning** — Remove OCR errors
- ✅ **Auto Correction** — Fix ingredient concentrations, CAS numbers
- ✅ **Completion Tracker** — Track 16 sections status

### 📋 TFDA 16 Sections

**Part I: Product Description (1-8)**
1. Basic Product Information
2. Product Description
3. Full Ingredient List
4. Product Labeling & Leaflets
5. GMP Compliance Certificate
6. Manufacturing Methods
7. Usage Methods & Target Population
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

# Prepare PDF files
mkdir inputs/
# Put Thai PIF PDFs here

# Run conversion
python scripts/pif_converter_v4.py "inputs/" product-name

# View output
cat outputs/product-name_pif_tfda_v4.md
```

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

> 將泰國/ASEAN 格式 PIF **自動轉換**為台灣 TFDA 格式的完整工具

### ✨ 功能特色

- ✅ **自動轉換** — 泰國 PIF → 台灣 TFDA 16 項目
- ✅ **PDF OCR** — 支援大檔案（200MB+）處理
- ✅ **結構化輸出** — Markdown 表格格式
- ✅ **亂碼清理** — 自動移除 OCR 錯誤和亂碼
- ✅ **數據修正** — 自動修正成分濃度、CAS 號碼
- ✅ **檢查清單** — 16 項目的完成狀態追蹤

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
9. 產品及各別成分之物理及化學特性
10. 毒理學終點數據
11. 安定性試驗報告
12. 微生物檢測報告
13. 防腐挑戰測試

**參、安全評估資料 (14-16)**
14. 功能評估佐證資料
15. 包裝相容性資料
16. 產品安全資料（含簽署人員簽名）

### 🚀 快速開始

```bash
# 安裝
clawhub install bounce12340/taiwan-cosmetic-pif

# 準備 PDF 檔案
mkdir inputs/
# 放入 Thai PIF PDF

# 執行轉換
python scripts/pif_converter_v4.py "inputs/" product-name

# 查看輸出
cat outputs/product-name_pif_tfda_v4.md
```

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

> 将泰国/ASEAN 格式 PIF **自动转换**为台湾 TFDA 格式的完整工具

### ✨ 功能特性

- ✅ **自动转换** — 泰国 PIF → 台湾 TFDA 16 项目
- ✅ **PDF OCR** — 支持大文件（200MB+）处理
- ✅ **结构化输出** — Markdown 表格格式
- ✅ **乱码清理** — 自动移除 OCR 错误和乱码
- ✅ **数据修正** — 自动修正成分浓度、CAS 号码
- ✅ **检查清单** — 16 项目的完成状态追踪

### 📋 TFDA 16 项目

**一、产品叙述 (1-8)**
1. 产品基本资料
2. 产品叙述
3. 全成分
4. 产品标签、仿单
5. GMP 符合证明
6. 制造方法、流程
7. 使用方法、部位、用量、频率及族群
8. 产品使用不良反应资料

**二、品质资料 (9-13)**
9. 产品及各别成分之物理及化学特性
10. 毒理学终点数据
11. 稳定性试验报告
12. 微生物检测报告
13. 防腐挑战测试

**三、安全评估资料 (14-16)**
14. 功能评估佐证资料
15. 包装相容性资料
16. 产品安全资料（含签署人员签名）

### 🚀 快速开始

```bash
# 安装
clawhub install bounce12340/taiwan-cosmetic-pif

# 准备 PDF 文件
mkdir inputs/
# 放入 Thai PIF PDF

# 执行转换
python scripts/pif_converter_v4.py "inputs/" product-name

# 查看输出
cat outputs/product-name_pif_tfda_v4.md
```

### 📊 输出示例

### 成分表

```markdown
| # | INCI 名称 | 浓度 (%) | CAS No. | 功能 |
|---|----------|---------|---------|------|
| 1 | Aqua (Water) | 85.7474 | 7732-18-5 | 溶剂 |
| 2 | Sodium Laureth Sulfate | 7.1775 | 9004-82-4 | 清洁 |
| 3 | Sodium Chloride | 3.5900 | 7647-14-5 | 增稠 |
```

### 微生物检测

```markdown
| 检测项目 | 结果 | 标准 |
|----------|------|------|
| 总菌数 | ≤100 CFU/g | ≤100 CFU/g |
| 霉菌/酵母菌 | ≤10 CFU/g | ≤10 CFU/g |
| 大肠杆菌 | 未检出 | 未检出 |
```

### 🔧 高级用法

#### 清理乱码

```bash
python scripts/cleanup_pif_v2.py outputs/product-name_pif_tfda_v4.md
```

#### 使用 PaddleOCR（高质量）

```bash
# 安装依赖
pip install paddlepaddle paddleocr pymupdf

# 执行 OCR
python scripts/pif_paddleocr.py
```

### 📦 依赖

- Python 3.11+
- pypdf
- python-docx（可选）
- pymupdf（可选）
- paddlepaddle, paddleocr（可选）

### ⚠️ 注意事项

1. **PDF 质量**: 建议先用 Adobe Acrobat 进行 OCR，设置 Thai + English
2. **成分浓度**: 自动修正，但建议人工确认
3. **安全评估**: 项目 16 需要合格人员签署
4. **手动补充**: 部分项目可能需要人工补充完整数据

### 🔗 相关资源

- [TFDA 法规](https://www.fda.gov.tw/)
- [CIR Safety Assessments](https://www.cir-safety.org/)
- [EU SCCS](https://health.ec.europa.eu/scientific-committees/sccs_en)
- [ISO 22716 (GMP)](https://www.iso.org/standard/36437.html)

### 📝 授权

MIT License

### 👤 作者

**Josh** — [@bounce12340](https://github.com/bounce12340)

---

<p align="center">
  Made with ❤️ for Taiwan Cosmetic Regulatory Compliance<br>
  為台灣化妝品法規合規用心打造 | 为台湾化妆品法规合规用心打造
</p>
