---
name: 台灣化妝品 PIF 檔案製作
slug: taiwan-cosmetic-pif
version: 1.0.0
homepage: https://github.com/yourusername/taiwan-cosmetic-pif
description: 將泰國/ASEAN 格式 PIF 自動轉換為台灣 TFDA 格式的 16 項目完整檔案。支援 PDF OCR 萃取、結構化分類、Markdown/Word 輸出。
metadata: {"clawdbot":{"emoji":"📋","os":["win32","darwin","linux"]}}
---

## 當使用

使用當：
1. 需要將泰國/ASEAN 格式 PIF 轉換為台灣 TFDA 格式
2. 需要從 PDF 萃取產品資訊並分類到 16 個 TFDA 項目
3. 需要生成結構化的 PIF Markdown 或 Word 文件
4. 需要清理 OCR 亂碼並修正成分濃度、CAS 號碼等數據

## 核心規則

### 1. TFDA 16 項目結構

本 Skill 嚴格遵循台灣 TFDA PIF 格式，包含 16 個項目：

**壹、產品敘述 (項目 1-8)**
1. 產品基本資料
2. 產品敘述
3. 全成分
4. 產品標籤、仿單
5. GMP 符合證明
6. 製造方法、流程
7. 使用方法、部位、用量、頻率及族群
8. 產品使用不良反應資料

**貳、品質資料 (項目 9-13)**
9. 產品及各別成分之物理及化學特性
10. 毒理學終點數據
11. 安定性試驗報告
12. 微生物檢測報告
13. 防腐挑戰測試

**肆、安全評估資料 (項目 14-16)**
14. 功能評估佐證資料
15. 包裝相容性資料
16. 產品安全資料（含簽署人員簽名）

### 2. PDF 處理流程

```
PDF 輸入 → OCR 文字萃取 → 清理亂碼 → 分類到 16 項目 → 結構化輸出
```

**OCR 選項：**
- 預設：pypdf（快速，適合已 OCR 的 PDF）
- 可選：PaddleOCR（更準確，支援泰文，但需要額外安裝）

### 3. 數據修正規則

**成分濃度修正：**
- Aqua (Water): 85.7474%
- Sodium Laureth Sulfate: 7.1775%
- Sodium Chloride: 3.5900%
- Cocamidopropyl Betaine: 1.2375%
- Lauryl Glucoside: 1.2375%
- Lactic Acid: 0.3600%
- Disodium EDTA: 0.2000%
- Sodium Benzoate: 0.2000%
- Parfum: 0.1000%
- Alpha-Glucan Oligosaccharide: 0.0500%
- Polyquaternium-7: 0.0500%
- Sodium Hydroxide: 0.0001%
- Limonene: 0.0907%
- Linalool: 0.0007%
- Citronellol: 0.0004%

**CAS 號碼修正：**
- Aqua: 7732-18-5
- Sodium Laureth Sulfate: 9004-82-4
- Sodium Chloride: 7647-14-5
- Cocamidopropyl Betaine: 97862-59-4
- Lauryl Glucoside: 110615-47-9
- Lactic Acid: 50-21-5
- Disodium EDTA: 139-33-3
- Sodium Benzoate: 532-32-1
- Polyquaternium-7: 26590-05-6
- Sodium Hydroxide: 1310-73-2
- Limonene: 138-86-3
- Linalool: 78-70-6
- Citronellol: 106-22-9

### 4. 亂碼清理規則

**移除項目：**
- 中文 OCR 亂碼（如：曬鼉、呱黷、衊蛐等）
- 頁碼和頁首尾（如：Page X of Y, UNCONTROLLED WHEN PRINTED）
- 重複內容（連續相同行）

**修正項目：**
- OCR 拼寫錯誤（Fem inine → Feminine, appltto → apply to）
- 數字格式（200C → 20°C, 250C → 25°C）
- 物理化學數據（pH 值、黏度、密度等）

## 使用方式

### 基本用法

```bash
python scripts/pif_converter_v4.py <輸入 PDF 資料夾> [產品名稱]
```

### 範例

```bash
# 處理 Summers Eve 產品
python scripts/pif_converter_v4.py "C:/PIF/summers-eve" summers-eve

# 輸出位置
outputs/summers-eve_pif_tfda_v4.md
```

### 清理亂碼

```bash
python scripts/cleanup_pif_v2.py <輸入 MD 檔>
```

### 使用 PaddleOCR（可選）

```bash
# 安裝依賴
pip install paddlepaddle paddleocr pymupdf

# 執行 OCR
python scripts/pif_paddleocr.py
```

## 輸出格式

### Markdown 輸出

- **檢查清單表格** - 16 項目的完成狀態
- **成分表** - INCI 名稱、濃度、CAS No.、功能
- **微生物檢測表** - 檢測項目、結果、標準
- **物理化學表** - pH、黏度、密度、外觀
- **參考文獻** - CIR、SCCS、ISO 等連結

### Word 輸出（可選）

使用 `word-docx` skill 轉換為 .docx 格式：

```bash
clawhub install word-docx
# 然後使用 word-docx skill 轉換
```

## 檔案結構

```
taiwan-cosmetic-pif/
├── SKILL.md                      # Skill 說明文件
├── README.md                     # 使用說明
├── scripts/
│   ├── pif_converter_v4.py       # 主要轉換腳本
│   ├── cleanup_pif_v2.py         # 亂碼清理腳本
│   └── pif_paddleocr.py          # PaddleOCR 腳本（可選）
└── outputs/
    └── <product>_pif_tfda_v4.md  # 輸出檔案
```

## 依賴

- Python 3.11+
- pypdf
- python-docx（可選，用於 Word 輸出）
- pymupdf（可選，用於 PDF 轉圖片）
- paddlepaddle, paddleocr（可選，用於高品質 OCR）

## 注意事項

1. **PDF 品質**：建議先使用 Adobe Acrobat 進行 OCR 處理，設定語言為 Thai + English
2. **成分濃度**：自動修正為正確值，但建議人工確認
3. **安全評估**：項目 16 需要合格安全評估人員簽署
4. **手動補充**：部分項目（如毒理學、安定性）可能需要人工補充完整數據

## 相關 Skill

- `word-docx` - 轉換為 Word (.docx) 格式
- `pdf-text-extractor` - PDF 文字萃取
- `documents` - 一般文件處理

## 反饋

- 問題回報：https://github.com/yourusername/taiwan-cosmetic-pif/issues
- 更新：`clawhub sync taiwan-cosmetic-pif`
