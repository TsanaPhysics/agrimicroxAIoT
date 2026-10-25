#!/bin/bash
# ==========================================================
# QUICK BUILD — Run this from Terminal.app (NOT from AI)
# ==========================================================
# Usage:
#   cd /Applications/XAMPP/xamppfiles/htdocs/11_Biology_Microbiology/microbioexam/agri_book
#   chmod +x quick_build.sh
#   ./quick_build.sh
# ==========================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌾 MicroBio Series — Book 2 Builder: Agricultural Microbiology"
echo "=========================================================="

# Create assets and build directories if they don't exist
mkdir -p assets
mkdir -p build

# 3-pass compile
for PASS in 1 2 3; do
    echo ""
    echo "Pass $PASS/3..."
    xelatex -interaction=nonstopmode \
            -file-line-error \
            main.tex
done

# Rename output
if [ -f "main.pdf" ]; then
    mv main.pdf "จุลชีววิทยาการเกษตร_ชีวะทัศนา.pdf"
    echo ""
    echo "✅ Build complete!"
    echo "📚 Output: จุลชีววิทยาการเกษตร_ชีวะทัศนา.pdf"
    open "จุลชีววิทยาการเกษตร_ชีวะทัศนา.pdf" 2>/dev/null || true
else
    echo "❌ Build failed. Check main.log for errors."
    exit 1
fi
