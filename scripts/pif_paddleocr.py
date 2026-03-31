# pif_paddleocr.py - Extract text from Thai PIF PDFs using PaddleOCR

import sys
from pathlib import Path
from paddleocr import PaddleOCR
import cv2
import fitz  # PyMuPDF

def pdf_to_images(pdf_path, output_dir, dpi=200):
    """Convert PDF pages to images."""
    print(f"  Converting {Path(pdf_path).name} to images...")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    image_paths = []
    
    for i, page in enumerate(doc):
        if (i + 1) % 50 == 0:
            print(f"    Page {i+1}/{len(doc)}")
        
        # Render page to image
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat)
        
        img_path = output_dir / f"page_{i+1:04d}.png"
        pix.save(str(img_path))
        image_paths.append(img_path)
    
    doc.close()
    print(f"    Extracted {len(image_paths)} images")
    return image_paths

def ocr_images(image_paths, ocr, output_file):
    """Run OCR on images and save results."""
    print(f"  Running OCR on {len(image_paths)} images...")
    
    results = []
    
    for i, img_path in enumerate(image_paths):
        if (i + 1) % 50 == 0:
            print(f"    OCR Page {i+1}/{len(image_paths)}")
        
        # Run OCR (using new API)
        result = ocr.predict(str(img_path))
        
        # Extract text from result format
        page_text = []
        if result:
            # New API returns dict with 'text_results' key
            if isinstance(result, dict):
                if 'text_results' in result:
                    for item in result['text_results']:
                        if isinstance(item, dict) and 'text' in item:
                            page_text.append(item['text'])
            elif isinstance(result, list) and len(result) > 0:
                # Old API format: list of lists
                if isinstance(result[0], list):
                    for line in result[0]:
                        if isinstance(line, (list, tuple)) and len(line) >= 2:
                            text = line[1][0] if isinstance(line[1], (list, tuple)) else str(line[1])
                            page_text.append(text)
        
        results.append({
            'page': i + 1,
            'text': '\n'.join(page_text),
            'image': str(img_path)
        })
    
    # Save results
    print(f"  Saving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# PaddleOCR Extraction Results\n\n")
        for r in results:
            f.write(f"## Page {r['page']}\n\n")
            f.write(r['text'] + "\n\n")
            f.write("---\n\n")
    
    print(f"  Done! Total pages: {len(results)}")
    return results

def main():
    print("=" * 60)
    print("PIF PaddleOCR Extraction")
    print("=" * 60)
    
    # Disable oneDNN to avoid compatibility issues
    import os
    os.environ['FLAGS_use_mkldnn'] = '0'
    
    # Input PDFs
    input_dir = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/inputs/summers-eve")
    output_dir = Path("C:/Users/BDAIPC/.openclaw/workspace/temp-repo/outputs/paddleocr")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(input_dir.glob("*.pdf"))
    print(f"\n[INPUT] Found {len(pdf_files)} PDF files")
    
    # Initialize PaddleOCR with Thai + English + Multi-language support
    print("\n[INIT] Loading PaddleOCR (Thai + English + Multi-language)...")
    ocr = PaddleOCR(
        use_textline_orientation=False,
        lang='multi',  # ✅ Fixed: Multi-language support (80+ languages including Thai)
        det=True,
        rec=True,
        cls=False
    )
    
    all_results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        print(f"    Size: {pdf_file.stat().st_size / (1024*1024):.1f} MB")
        
        # Convert to images
        img_dir = output_dir / pdf_file.stem
        image_paths = pdf_to_images(str(pdf_file), img_dir)
        
        # Run OCR
        output_file = output_dir / f"{pdf_file.stem}_ocr.md"
        results = ocr_images(image_paths, ocr, output_file)
        all_results.extend(results)
        
        print(f"    Output: {output_file}")
    
    # Combine all results
    combined_output = output_dir / "summers-eve_combined_ocr.md"
    print(f"\n[COMBINE] Creating combined file: {combined_output}")
    
    with open(combined_output, 'w', encoding='utf-8') as f:
        f.write("# SUMMER'S EVE PIF - PaddleOCR Extraction\n\n")
        f.write(f"**Total Pages:** {len(all_results)}\n\n")
        f.write("---\n\n")
        
        for r in all_results:
            f.write(f"## Page {r['page']}\n\n")
            f.write(r['text'] + "\n\n")
            f.write("---\n\n")
    
    print(f"\n[OK] Combined OCR results: {combined_output}")
    print(f"    Total pages: {len(all_results)}")
    print(f"    Output directory: {output_dir}")
    
    print("\n" + "=" * 60)
    print("PaddleOCR Extraction Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
