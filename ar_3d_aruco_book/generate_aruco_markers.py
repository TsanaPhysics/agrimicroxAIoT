#!/usr/bin/env python3
"""
Generate ArUco markers (DICT_6X6_250) for all 8 Agricultural Microbiology Labs.
Outputs:
1. High-resolution PNG markers (600x600 px) in aruco_markers/
2. Formatted target cards with Thai labels and borders
3. JSON metadata file aruco_mapping.json
4. Precomputed JavaScript dictionary aruco_dictionary_6x6.js
"""

import os
import json
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MARKERS_DIR = os.path.join(BASE_DIR, "aruco_markers")
CARDS_DIR = os.path.join(BASE_DIR, "aruco_cards")

os.makedirs(MARKERS_DIR, exist_ok=True)
os.makedirs(CARDS_DIR, exist_ok=True)

# 8 Labs Mapping
LAB_TARGETS = [
    {
        "lab_id": 1,
        "aruco_id": 0,
        "code": "lab01_winogradsky",
        "title": "ปฏิบัติการที่ 1: การสร้างและศึกษานิเวศวิทยา Winogradsky Column",
        "title_en": "Lab 1: Winogradsky Column & Soil Microbial Ecology",
        "short": "1. คอลัมน์วิโนกราดสกี",
        "biomolecule": "Photosynthetic Reaction Center & Bacteriochlorophyll",
        "pdb_id": "1PCR",
        "color": "#10b981"
    },
    {
        "lab_id": 2,
        "aruco_id": 1,
        "code": "lab02_rhizobium",
        "title": "ปฏิบัติการที่ 2: การแยกและทดสอบประสิทธิภาพ Rhizobium จากปมรากถั่ว",
        "title_en": "Lab 2: Rhizobium Isolation & Leghemoglobin Activity",
        "short": "2. ปมรากถั่วและเลกเฮโมโกลบิน",
        "biomolecule": "Leghemoglobin (Oxygen Buffer Protein)",
        "pdb_id": "1GDJ",
        "color": "#ec4899"
    },
    {
        "lab_id": 3,
        "aruco_id": 2,
        "code": "lab03_phosphate",
        "title": "ปฏิบัติการที่ 3: การคัดเลือกจุลินทรีย์ละลายฟอสเฟต (PSI)",
        "title_en": "Lab 3: Phosphate Solubilizing Microorganisms & PSI",
        "short": "3. จุลินทรีย์ละลายฟอสเฟต",
        "biomolecule": "Acid Phosphatase / Phytase",
        "pdb_id": "1DKL",
        "color": "#f59e0b"
    },
    {
        "lab_id": 4,
        "aruco_id": 3,
        "code": "lab04_trichoderma",
        "title": "ปฏิบัติการที่ 4: การทดสอบกิจกรรมปฏิปักษ์ของ Trichoderma (PIRG)",
        "title_en": "Lab 4: Trichoderma Antagonistic Assay & PIRG",
        "short": "4. ราปฏิปักษ์ไตรโคเดอร์มา",
        "biomolecule": "Endochitinase Chi18a & Bt Toxin",
        "pdb_id": "1CTN",
        "color": "#06b6d4"
    },
    {
        "lab_id": 5,
        "aruco_id": 4,
        "code": "lab05_mycorrhiza",
        "title": "ปฏิบัติการที่ 5: การย้อมสีและตรวจหาเชื้อราไมคอร์ไรซาในรากพืช",
        "title_en": "Lab 5: Arbuscular Mycorrhizal Fungi (AMF) Root Colonization",
        "short": "5. ราไมคอร์ไรซาในรากพืช",
        "biomolecule": "Plant Phosphate Transporter (Pht1)",
        "pdb_id": "7EI8",
        "color": "#8b5cf6"
    },
    {
        "lab_id": 6,
        "aruco_id": 5,
        "code": "lab06_biofertilizer",
        "title": "ปฏิบัติการที่ 6: การวิเคราะห์คุณภาพปุ๋ยชีวภาพและการตรวจหาเชื้อปนเปื้อน",
        "title_en": "Lab 6: Biofertilizer Quality Control & Serial Dilution",
        "short": "6. ตรวจสอบคุณภาพปุ๋ยชีวภาพ",
        "biomolecule": "Bacterial Cell Wall Peptidoglycan Complex",
        "pdb_id": "1VQQ",
        "color": "#3b82f6"
    },
    {
        "lab_id": 7,
        "aruco_id": 6,
        "code": "lab07_soil_dna",
        "title": "ปฏิบัติการที่ 7: การสกัด Soil DNA และการตรวจสอบคุณภาพ",
        "title_en": "Lab 7: Soil Metagenomic DNA Extraction & Purity",
        "short": "7. การสกัด Soil DNA",
        "biomolecule": "B-DNA Double Helix",
        "pdb_id": "1BNA",
        "color": "#eab308"
    },
    {
        "lab_id": 8,
        "aruco_id": 7,
        "code": "lab08_pcr_diagnosis",
        "title": "ปฏิบัติการที่ 8: การตรวจวินิจฉัยโรคพืชด้วย PCR และการประเมินภาพด้วย OpenCV",
        "title_en": "Lab 8: Plant Pathogen PCR Diagnosis & Vision AI",
        "short": "8. PCR วินิจฉัยโรคพืช & AI",
        "biomolecule": "Taq DNA Polymerase Polymerization Complex",
        "pdb_id": "1TAU",
        "color": "#ef4444"
    }
]

# Load ArUco Dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

dict_bits_map = {}

print("==================================================================")
print("Generating ArUco 6x6 Markers for 8 Microbiology Labs")
print("==================================================================")

for lab in LAB_TARGETS:
    aruco_id = lab["aruco_id"]
    code = lab["code"]
    
    # 1. Generate Raw Marker (600x600 px, high contrast)
    marker_raw = cv2.aruco.generateImageMarker(aruco_dict, aruco_id, 600)
    marker_path = os.path.join(MARKERS_DIR, f"aruco_id_{aruco_id}_{code}.png")
    cv2.imwrite(marker_path, marker_raw)
    
    # Also save with standard simple name
    cv2.imwrite(os.path.join(MARKERS_DIR, f"aruco_id_{aruco_id}.png"), marker_raw)
    
    # 2. Extract 6x6 inner bits for JavaScript real-time decoder
    # A standard 6x6 marker in OpenCV has an 8x8 grid (6x6 inner data + 1-cell black border)
    grid_img = cv2.aruco.generateImageMarker(aruco_dict, aruco_id, 8)
    # Extract inner 6x6 (rows 1 to 6, cols 1 to 6)
    inner_bits = []
    for r in range(1, 7):
        row = []
        for c in range(1, 7):
            val = 1 if grid_img[r, c] > 127 else 0
            row.append(val)
        inner_bits.append(row)
    dict_bits_map[str(aruco_id)] = inner_bits

    # 3. Create Styled Target Card with Border, Labels and Academic Frame
    card_w, card_h = 800, 960
    card = np.ones((card_h, card_w, 3), dtype=np.uint8) * 255 # White background
    
    # Draw Outer Dark Border
    cv2.rectangle(card, (16, 16), (card_w - 16, card_h - 16), (20, 35, 13), 3)
    cv2.rectangle(card, (24, 24), (card_w - 24, card_h - 24), (165, 225, 197), 1)

    # Header Bar
    cv2.rectangle(card, (30, 30), (card_w - 30, 95), (46, 125, 50), -1) # Dark green
    cv2.putText(card, f"AR 3D ARUCO BOOK - LAB {lab['lab_id']}", (50, 72), 
                cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

    # Paste Marker in Center
    marker_resized = cv2.resize(marker_raw, (540, 540), interpolation=cv2.INTER_NEAREST)
    marker_bgr = cv2.cvtColor(marker_resized, cv2.COLOR_GRAY2BGR)
    
    # Marker drop shadow & white box
    y_start = 125
    x_start = (card_w - 540) // 2
    cv2.rectangle(card, (x_start - 10, y_start - 10), (x_start + 550, y_start + 550), (220, 220, 220), -1)
    card[y_start:y_start+540, x_start:x_start+540] = marker_bgr

    # Footer Card Info
    cv2.rectangle(card, (30, 690), (card_w - 30, 930), (245, 248, 245), -1)
    cv2.rectangle(card, (30, 690), (card_w - 30, 930), (165, 225, 197), 1)

    cv2.putText(card, f"ArUco ID: {aruco_id} (DICT_6X6_250)", (50, 730),
                cv2.FONT_HERSHEY_DUPLEX, 0.75, (46, 125, 50), 2, cv2.LINE_AA)
    cv2.putText(card, lab["title_en"], (50, 770),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (30, 40, 30), 1, cv2.LINE_AA)
    cv2.putText(card, f"Biomolecule: {lab['biomolecule']}", (50, 810),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (100, 70, 20), 1, cv2.LINE_AA)
    cv2.putText(card, f"Target PDB Code: {lab['pdb_id']}", (50, 850),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (46, 125, 50), 2, cv2.LINE_AA)
    cv2.putText(card, "Agricultural Microbiology & AIoT - RBRU 2026", (50, 900),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (120, 120, 120), 1, cv2.LINE_AA)

    card_path = os.path.join(CARDS_DIR, f"card_lab{lab['lab_id']}_aruco_{aruco_id}.png")
    cv2.imwrite(card_path, card)
    print(f"Generated: Lab {lab['lab_id']} -> ArUco ID {aruco_id} ({marker_path})")

# Export JSON Mapping
json_path = os.path.join(BASE_DIR, "aruco_mapping.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({
        "book_title": "Agricultural Microbiology and AIoT Technology",
        "book_isbn": "978-616-94520-2-7",
        "dictionary": "DICT_6X6_250",
        "total_labs": len(LAB_TARGETS),
        "targets": LAB_TARGETS
    }, f, ensure_ascii=False, indent=2)
print(f"Saved metadata: {json_path}")

# Export JS Bit Patterns Lookup
js_dict_path = os.path.join(BASE_DIR, "aruco_dictionary_6x6.js")
with open(js_dict_path, "w", encoding="utf-8") as f:
    f.write("// ArUco DICT_6X6_250 Precomputed Bits for Agricultural Microbiology WebAR\n")
    f.write("// Auto-generated from OpenCV DICT_6X6_250\n")
    f.write("const ARUCO_DICT_6X6_MAP = ")
    json.dump(dict_bits_map, f, indent=2)
    f.write(";\n\n")
    f.write("if (typeof module !== 'undefined' && module.exports) {\n")
    f.write("  module.exports = { ARUCO_DICT_6X6_MAP };\n")
    f.write("}\n")
print(f"Saved JS dictionary: {js_dict_path}")
print("All 8 ArUco markers and target cards generated successfully!")
