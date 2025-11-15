# Modal deployment for IUI 2025 User Study
# This creates a custom image that can be used with Modal Notebooks
# To use: 
# 1. Deploy this: modal deploy modal_app.py
# 2. Go to modal.com/notebooks and create a new notebook
# 3. Select the custom image from "iui-2025-voice-study" app
# 4. Upload your notebook file or copy the cells

import modal

# Create Modal app
app = modal.App("iui-2025-voice-study")

# Create a volume for persistent storage of results
volume = modal.Volume.from_name("iui-study-results", create_if_missing=True)

# Define the container image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "ffmpeg",
        "libsndfile1",
        "git"
    )
    .pip_install(
        "torch==2.1.0",
        "torchaudio==2.1.0",
        "numpy",
        "ipywidgets",
        "pandas",
        "librosa",
        "transformers",
        "omegaconf",
        "pyyaml",
        "einops",
        "accelerate",
    )
    .run_commands(
        "git clone https://github.com/Plachtaa/seed-vc.git /root/seed-vc"
    )
    # Add local files to the image (use copy=True for notebooks)
    .add_local_dir(
        ".",
        remote_path="/root/study",
        copy=True,
        # Exclude large directories
        condition=lambda pth: not any(
            excluded in pth for excluded in [
                ".git", "__pycache__", ".ipynb_checkpoints", 
                "emotion_balanced", "Emotion_Balanced.zip", "__MACOSX",
                "Test", "emotion_balanced_test", "recordings", "responses"
            ]
        )
    )
)

# Function to use this image in Modal Notebooks
@app.function(
    image=image,
    volumes={"/mnt/study-results": volume},  # Mount volume for persistent storage
    gpu="T4",  # Use GPU for faster voice conversion
    timeout=7200,  # 2 hour timeout
)
def notebook_image():
    """
    This function references the custom image for use in Modal Notebooks.
    
    After deploying with: modal deploy modal_app.py
    
    Go to modal.com/notebooks and:
    1. Create a new notebook
    2. In the sidebar, search for "iui-2025-voice-study" app
    3. Select this function to use the custom image
    4. Upload your notebook or paste the code
    5. Files will be in /root/study/
    6. Save results to /mnt/study-results/ for persistence
    """
    pass


# Alternative: Test function to verify setup
@app.function(image=image, gpu="T4")
def test_setup():
    """Test that everything is set up correctly"""
    import torch
    import sys
    import os
    
    print("✓ Python version:", sys.version)
    print("✓ PyTorch version:", torch.__version__)
    print("✓ CUDA available:", torch.cuda.is_available())
    
    # Test seed-vc import
    sys.path.insert(0, "/root/seed-vc")
    print("✓ Seed-VC path added")
    
    # List study files
    print("\n✓ Study files:")
    for f in os.listdir("/root/study"):
        print(f"  - {f}")
    
    return "Setup test passed!"

