#!/usr/bin/env python3
"""
Quick setup verification script for IUI 2025 User Study
Run this before starting the study to check if everything is configured correctly.
"""

import sys
import os
from pathlib import Path

def check_item(name, condition, fix_hint=""):
    """Check a condition and print status"""
    if condition:
        print(f"✓ {name}")
        return True
    else:
        print(f"✗ {name}")
        if fix_hint:
            print(f"  → {fix_hint}")
        return False

def main():
    print("=" * 60)
    print("IUI 2025 User Study - Setup Verification")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Python version
    print("1. Checking Python version...")
    py_version = sys.version_info
    all_ok &= check_item(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 8),
        "Please use Python 3.8 or higher"
    )
    print()
    
    # Check required packages
    print("2. Checking required packages...")
    packages = ['torch', 'torchaudio', 'numpy', 'ipywidgets', 'voila', 'jupyter']
    for pkg in packages:
        try:
            __import__(pkg)
            check_item(f"{pkg}", True)
        except ImportError:
            all_ok &= check_item(
                f"{pkg}",
                False,
                f"Install with: pip install {pkg}"
            )
    print()
    
    # Check directories
    print("3. Checking directory structure...")
    base_dir = Path.cwd()
    
    dirs_to_check = {
        'seed-vc': 'Seed-VC directory (required for voice conversion)',
        'target_voices/emotion_samples': 'Target voice samples directory',
        'target_voices/emotion_samples/happy': 'Happy emotion samples',
        'target_voices/emotion_samples/sad': 'Sad emotion samples',
        'target_voices/emotion_samples/angry': 'Angry emotion samples',
    }
    
    for dir_name, description in dirs_to_check.items():
        dir_path = base_dir / dir_name
        all_ok &= check_item(
            description,
            dir_path.exists(),
            f"Missing: {dir_path}"
        )
    print()
    
    # Check for audio files in emotion samples
    print("4. Checking emotion sample audio files...")
    for emotion in ['happy', 'sad', 'angry']:
        emotion_dir = base_dir / 'target_voices' / 'emotion_samples' / emotion
        if emotion_dir.exists():
            wav_files = list(emotion_dir.glob('*.wav'))
            check_item(
                f"{emotion.capitalize()} samples ({len(wav_files)} files)",
                len(wav_files) > 0,
                f"Add at least one .wav file to {emotion_dir}"
            )
    print()
    
    # Check Seed-VC installation
    print("5. Checking Seed-VC setup...")
    seed_vc_dir = base_dir / 'seed-vc'
    if seed_vc_dir.exists():
        inference_py = seed_vc_dir / 'inference.py'
        check_item(
            "inference.py exists",
            inference_py.exists(),
            "Seed-VC may not be properly installed"
        )
        
        # Check if seed-vc dependencies are installed
        try:
            sys.path.insert(0, str(seed_vc_dir))
            import yaml
            check_item("PyYAML (Seed-VC dependency)", True)
        except ImportError:
            all_ok &= check_item(
                "PyYAML (Seed-VC dependency)",
                False,
                "Run: cd seed-vc && pip install -r requirements-mac.txt"
            )
    print()
    
    # Check model checkpoint
    print("6. Checking model checkpoint...")
    checkpoint_locations = [
        base_dir / 'DiT_uvit_tat_xlsr_ema.pth',
        base_dir / 'seed-vc' / 'DiT_uvit_tat_xlsr_ema.pth',
        Path.home() / '.cache' / 'huggingface' / 'hub',
    ]
    
    checkpoint_found = any(loc.exists() for loc in checkpoint_locations if loc.parent.exists())
    check_item(
        "Model checkpoint file",
        checkpoint_found,
        "Model will be downloaded automatically on first run"
    )
    print()
    
    # Summary
    print("=" * 60)
    if all_ok:
        print("✓ All checks passed! You're ready to run the study.")
        print()
        print("To start the study, run:")
        print("  ./run_study.sh")
        print()
        print("Or manually:")
        print("  voila user_study_iui_2025.ipynb --port=8866")
    else:
        print("⚠ Some issues were found. Please fix them before running the study.")
        print()
        print("See SETUP.txt for detailed installation instructions.")
    print("=" * 60)

if __name__ == '__main__':
    main()
