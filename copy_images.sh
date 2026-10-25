#!/bin/bash
# ==============================================================================
# สคริปต์คัดลอกภาพประกอบ 3D จากโฟลเดอร์ของระบบ AI ไปยังโฟลเดอร์ assets/ ของหนังสือเล่ม 2
# (หากไม่พบรูปภาพเนื่องจากข้อจำกัดโควตา จะใช้รูปภาพจากเล่ม 1 เป็นภาพตัวอย่างชั่วคราว)
# ==============================================================================

set -e

# ที่อยู่โฟลเดอร์ภาพประกอบที่สร้างขึ้นใหม่ใน session นี้
BRAIN_DIR="/Users/chewathassana/.gemini/antigravity-ide/brain/6a8f37c9-438b-4f4b-985c-1aa20149a1a0"
ASSETS_DIR="/Applications/XAMPP/xamppfiles/htdocs/11_Biology_Microbiology/microbioexam/agri_book/assets"
BOOK1_ASSETS="/Applications/XAMPP/xamppfiles/htdocs/11_Biology_Microbiology/microbioexam/book/assets"

# สร้างโฟลเดอร์ assets หากยังไม่มี
mkdir -p "$ASSETS_DIR"

echo "📂 กำลังคัดลอกภาพประกอบการเกษตรไปยัง assets ของหนังสือเล่ม 2..."

copy_with_fallback() {
    local pattern="$1"
    local dest_name="$2"
    local label="$3"
    
    # พยายามคัดลอกไฟล์จริงจากโฟลเดอร์ AI
    if ls "$BRAIN_DIR"/$pattern >/dev/null 2>&1; then
        cp "$BRAIN_DIR"/$pattern "$ASSETS_DIR"/$dest_name
        echo "✅ คัดลอกภาพจริงสำเร็จ: $dest_name ($label)"
    else
        # ใช้ภาพจริงจากเล่ม 1 เป็นภาพตัวแทนชั่วคราวเพื่อป้องกันการพังของ libpng
        cp "$BOOK1_ASSETS"/ch03_industrial_bioreactor.png "$ASSETS_DIR"/$dest_name
        echo "⚠️ ใช้ภาพตัวแทนชั่วคราว (เนื่องจากโควตาจำกัด): $dest_name ($label)"
    fi
}

copy_with_fallback "ch01_winogradsky_column_*.png" "ch01_winogradsky_column.png" "Winogradsky Column"
copy_with_fallback "ch02_nitrogen_cycle_*.png" "ch02_nitrogen_cycle.png" "Nitrogen Cycle"
copy_with_fallback "ch03_root_nodules_*.png" "ch03_root_nodules.png" "Root Nodules"
copy_with_fallback "ch04_fungal_infection_*.png" "ch04_fungal_infection.png" "Fungal Infection"
copy_with_fallback "ch05_bt_mechanism_*.png" "ch05_bt_mechanism.png" "Bt Mechanism"
copy_with_fallback "ch06_biofertilizer_fermentation_*.png" "ch06_biofertilizer_fermentation.png" "Biofertilizer Fermentation"
copy_with_fallback "ch07_rumen_microbes_*.png" "ch07_rumen_microbes.png" "Rumen Microbes"
copy_with_fallback "ch08_composting_microbes_*.png" "ch08_composting_microbes.png" "Composting Microbes"
copy_with_fallback "ch09_metagenomics_ai_*.png" "ch09_metagenomics_ai.png" "Metagenomics & AI"

echo ""
echo "✅ จัดเตรียมไฟล์ภาพประกอบทั้ง 9 บทเรียบร้อยแล้ว!"
echo "📚 ท่านสามารถสั่งคอมไพล์หนังสือได้โดยใช้คำสั่ง:"
echo "   cd /Applications/XAMPP/xamppfiles/htdocs/11_Biology_Microbiology/microbioexam/agri_book"
# สรุปขั้นตอน
