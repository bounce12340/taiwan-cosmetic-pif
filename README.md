# 台灣化妝品 PIF 檔案製作 Skill

將泰國/ASEAN 格式 PIF 自動轉換為台灣 TFDA 格式的完整工具。

## 功能特色

- ✅ **自動轉換** - 泰國 PIF → 台灣 TFDA 16 項目
- ✅ **PDF OCR** - 支援大檔案（200MB+）處理
- ✅ **結構化輸出** - Markdown 表格格式
- ✅ **亂碼清理** - 自動移除 OCR 錯誤和中文亂碼
- ✅ **數據修正** - 自動修正成分濃度、CAS 號碼
- ✅ **檢查清單** - 16 項目的完成狀態追蹤

## 安裝

```bash
# 使用 clawhub 安裝
clawhub install taiwan-cosmetic-pif

# 或手動複製 skill 資料夾到 ~/.openclaw/workspace/skills/
```

## 快速開始

### 1. 準備 PDF 檔案

將泰國 PIF PDF 檔案放在同一個資料夾中：

```
inputs/
├── product1.pdf
├── product2.pdf
└── product3.pdf
```

### 2. 執行轉換

```bash
python scripts/pif_converter_v4.py "inputs/" product-name
```

### 3. 查看輸出

```
outputs/
└── product-name_pif_tfda_v4.md
```

## TFDA 16 項目

本 Skill 遵循台灣 TFDA PIF 格式，包含 16 個項目：

### 壹、產品敘述 (1-8)
1. 產品基本資料
2. 產品敘述
3. 全成分
4. 產品標籤、仿單
5. GMP 符合證明
6. 製造方法、流程
7. 使用方法、部位、用量、頻率及族群
8. 產品使用不良反應資料

### 貳、品質資料 (9-13)
9. 產品及各別成分之物理及化學特性
10. 毒理學終點數據
11. 安定性試驗報告
12. 微生物檢測報告
13. 防腐挑戰測試

### 肆、安全評估資料 (14-16)
14. 功能評估佐證資料
15. 包裝相容性資料
16. 產品安全資料（含簽署人員簽名）

## 輸出範例

### 成分表

```markdown
| # | INCI 名稱 | 濃度 (%) | CAS No. | 功能 |
|---|----------|---------|---------|------|
| 1 | Aqua (Water) | 85.7474 | 7732-18-5 | Solvent |
| 2 | Sodium Laureth Sulfate | 7.1775 | 9004-82-4 | Cleansing |
| 3 | Sodium Chloride | 3.5900 | 7647-14-5 | Viscosity |
```

### 微生物檢測

```markdown
| 檢測項目 | 結果 | 標準 |
|----------|------|------|
| 總菌數 | ≤100 CFU/g | ≤100 CFU/g |
| 黴菌/酵母菌 | ≤10 CFU/g | ≤10 CFU/g |
| 大腸桿菌 | 未檢出 | 未檢出 |
```

## 進階用法

### 清理亂碼

```bash
python scripts/cleanup_pif_v2.py outputs/product-name_pif_tfda_v4.md
```

### 使用 PaddleOCR（高品質）

```bash
# 安裝依賴
pip install paddlepaddle paddleocr pymupdf

# 執行 OCR
python scripts/pif_paddleocr.py
```

## 依賴

- Python 3.11+
- pypdf
- python-docx（可選）
- pymupdf（可選）
- paddlepaddle, paddleocr（可選）

## 注意事項

1. **PDF 品質**：建議先用 Adobe Acrobat 進行 OCR，設定 Thai + English
2. **成分濃度**：自動修正，但建議人工確認
3. **安全評估**：項目 16 需要合格人員簽署
4. **手動補充**：部分項目可能需要人工補充完整數據

## 相關資源

- [TFDA 法規](https://www.fda.gov.tw/)
- [CIR Safety Assessments](https://www.cir-safety.org/)
- [EU SCCS](https://health.ec.europa.eu/scientific-committees/sccs_en)
- [ISO 22716 (GMP)](https://www.iso.org/standard/36437.html)

## 授權

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！
