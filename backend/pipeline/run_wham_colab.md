# WHAM Batch Lifting Notes

Phase 1 uses WHAM manually on Google Colab's free T4 GPU while validating accuracy.

```python
!git clone https://github.com/yohanshin/WHAM.git
%cd WHAM
# Follow the official inference script.
# Input: extracted 2D keypoints from backend.pipeline.pose_pipeline.extract_2d_pose
# Output: world-grounded 3D joint positions plus foot-contact labels per frame
```

Keep WHAM as a batch step until Phase 4. The local `lift_to_3d` function currently
contains a z=0 fallback only to keep the pipeline contract runnable.
