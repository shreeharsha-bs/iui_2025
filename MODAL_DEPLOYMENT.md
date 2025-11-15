# Modal Deployment for IUI 2025 User Study

This guide explains how to deploy the user study environment to Modal's cloud notebooks.

## Overview

Modal Notebooks provide a hosted Jupyter environment in the cloud with GPU access. This eliminates the need for participants to install dependencies locally.

## Deployment Steps

### 1. Install Modal CLI

```bash
pip install modal
modal setup  # Authenticate with your Modal account
```

### 2. Deploy the Custom Image

```bash
cd /path/to/iui_2025
modal deploy modal_app.py
```

This will:
- Build a custom Docker image with all dependencies (PyTorch, seed-vc, etc.)
- Clone the seed-vc repository
- Copy your study files into the image
- Create a persistent volume for storing results

### 3. Access the Notebook

1. Go to **[modal.com/notebooks](https://modal.com/notebooks)**
2. Click "New Notebook"
3. In the right sidebar, under "Compute Profile":
   - Click on "Image" dropdown
   - Search for **"iui-2025-voice-study"**
   - Select the `notebook_image` function
4. Under "Storage":
   - Click "Attach Volume"
   - Select **"iui-study-results"**
   - It will be mounted at `/mnt/study-results/`

### 4. Upload or Create Your Notebook

Option A: Upload existing notebook
- Click the upload button and select `user_study_iui_2025.ipynb`

Option B: Copy cells manually
- Copy and paste cells from your local notebook into the Modal notebook

### 5. Adjust File Paths

In your notebook, update paths:
- Study files are in: `/root/study/`
- Seed-VC is in: `/root/seed-vc/`
- Save results to: `/mnt/study-results/` (this persists across sessions)

Example:
```python
import sys
sys.path.insert(0, "/root/seed-vc")

# Load data from study files
import pandas as pd
df = pd.read_csv("/root/study/selected_emotion_data_with_local_global_speaker.csv")

# Save results to persistent volume
df.to_csv("/mnt/study-results/my_results.csv", index=False)
```

## Sharing with Participants

1. In your Modal notebook, click **"Share"** in the top-right corner
2. Enable "Share by link"
3. Choose permissions:
   - **"Can view and run"** - Participants can execute cells
   - **"Can view"** - Read-only access
4. Copy the link and send to participants

Participants don't need a Modal account to access shared notebooks!

## Resource Management

### GPU Settings
- Default: T4 GPU (good for most tasks)
- To change: Sidebar → Compute Profile → GPU
- Options: T4, A10G, A100, H100

### Costs
- You're only charged when the kernel is running
- Idle notebooks (after 10 min by default) don't incur costs
- See [Modal Pricing](https://modal.com/pricing) for rates

### Timeouts
- Default idle timeout: 10 minutes
- Max execution time: 2 hours (configurable in `modal_app.py`)
- Adjust in: Sidebar → Compute Profile → Idle Timeout

## File Management

### Ephemeral Files
Files outside `/mnt/` are deleted when the kernel stops. This includes:
- `/root/study/recordings/` 
- `/root/study/responses/`

### Persistent Storage
Save important data to the mounted volume:
```python
# In your notebook
import shutil
shutil.copy("/root/study/recordings/audio.wav", "/mnt/study-results/audio.wav")
```

### Downloading Results
1. In Modal notebook, open the Files panel (left sidebar)
2. Navigate to `/mnt/study-results/`
3. Click the download icon next to any file

## Testing the Setup

Run the test function to verify everything works:

```bash
modal run modal_app.py::test_setup
```

Expected output:
```
✓ Python version: 3.11.x
✓ PyTorch version: 2.1.0
✓ CUDA available: True
✓ Seed-VC path added
✓ Study files:
  - user_study_iui_2025.ipynb
  - selected_emotion_data_with_local_global_speaker.csv
  - ...
Setup test passed!
```

## Troubleshooting

### "Image not found"
- Make sure you ran `modal deploy modal_app.py`
- Check deployment status: `modal app list`

### "Out of memory"
- Increase memory in Compute Profile settings
- Or switch to a GPU with more VRAM (A100 has 40GB)

### "Files not found"
- Remember files are in `/root/study/`, not current directory
- Check file list in the Files panel

### "Results disappeared"
- Only files in `/mnt/study-results/` persist
- Other directories are ephemeral

## Support

- Modal Docs: https://modal.com/docs/guide/notebooks
- Modal Slack: https://modal.com/slack
- Check your deployment: https://modal.com/apps
