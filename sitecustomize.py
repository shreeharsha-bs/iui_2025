# Auto-loaded by Python if present on sys.path. Used here to avoid modifying
# third-party code (seed-vc) while applying a compatibility patch for PyTorch 2.6.
# This sets torch.load default weights_only=False to match pre-2.6 behavior.

try:
    import torch
    _orig_load = torch.load

    def _patched_torch_load(f, map_location=None, pickle_module=None, weights_only=None, *args, **kwargs):
        if weights_only is None:
            weights_only = False
        return _orig_load(f, map_location=map_location, pickle_module=pickle_module, weights_only=weights_only, *args, **kwargs)

    torch.load = _patched_torch_load  # type: ignore[attr-defined]
except Exception:
    # If torch isn't available yet, do nothing.
    pass
