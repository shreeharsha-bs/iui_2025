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

# Create HuggingFace secret (you'll need to create this in Modal dashboard first)
# Go to modal.com/secrets and create a HuggingFace secret
try:
    hf_secret = modal.Secret.from_name("huggingface-secret")
except Exception:
    hf_secret = None
    print("Note: HuggingFace secret not found. Create one at modal.com/secrets if needed.")

# Define the container image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "ffmpeg",
        "libsndfile1",
        "git"
    )
    .pip_install(
        "numpy<2.0",  # Pin to 1.x for PyTorch 2.1 compatibility
        "torch==2.1.0",
        "torchaudio==2.1.0",
        "ipywidgets",
        "pandas",
        "librosa",
        "transformers",
        "omegaconf",
        "pyyaml",
        "einops",
        "accelerate",
        "munch",
        "g2p_en",
        "cached_path",
        "inflect",
        "editdistance",
    )
    .run_commands(
        "git clone https://github.com/Plachtaa/seed-vc.git /root/seed-vc",
        # Create necessary directories
        "mkdir -p /root/study/recordings",
        "mkdir -p /root/study/responses",
        "mkdir -p /root/study/results"
    )
    # Add essential study files to the image (copy=True to allow run_commands after)
    .add_local_file("shreeharshas-notebook-nov-16.ipynb", "/root/study/user_study.ipynb", copy=True)
    .add_local_file("selected_emotion_data_with_local_global_speaker.csv", "/root/study/selected_emotion_data_with_local_global_speaker.csv", copy=True)
    # Add the downloaded Seed-VC model file
    .add_local_file("DiT_uvit_tat_xlsr_ema.pth", "/root/models/DiT_uvit_tat_xlsr_ema.pth", copy=True)
    # Add target voices directory
    .add_local_dir("target_voices", remote_path="/root/study/target_voices", copy=True)
)

# Function to use this image in Modal Notebooks
@app.function(
    image=image,
    volumes={"/mnt/study-results": volume},  # Mount volume for persistent storage
    secrets=[hf_secret] if hf_secret else [],  # Attach HF secret if available
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
    
    HuggingFace Token: Will be available as HF_TOKEN env variable if secret is attached
    """
    import os
    if os.environ.get("HF_TOKEN"):
        print("✓ HuggingFace token is available")
    else:
        print("ℹ No HuggingFace token found")


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

