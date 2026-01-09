"""Compatibility helpers for loading pickled sklearn pipelines.

Provides a small shim to define sklearn.compose._RemainderColsList
when loading artifacts saved with older/newer sklearn versions that
used that internal symbol. Importing and calling
`ensure_sklearn_remainder()` is safe and idempotent.
"""
import importlib

def ensure_sklearn_remainder():
    # Ensure attribute exists in both the top-level sklearn.compose module
    # and the _column_transformer submodule where older pickles may look for it.
    try:
        mod = importlib.import_module('sklearn.compose')
    except Exception:
        mod = None

    try:
        submod = importlib.import_module('sklearn.compose._column_transformer')
    except Exception:
        submod = None

    if mod is None and submod is None:
        return

    if not (mod and hasattr(mod, '_RemainderColsList')) and not (submod and hasattr(submod, '_RemainderColsList')):
        class _RemainderColsList(list):
            """Small placeholder for sklearn.compose._RemainderColsList."""
            pass

        if mod is not None and not hasattr(mod, '_RemainderColsList'):
            setattr(mod, '_RemainderColsList', _RemainderColsList)
        if submod is not None and not hasattr(submod, '_RemainderColsList'):
            setattr(submod, '_RemainderColsList', _RemainderColsList)


__all__ = ["ensure_sklearn_remainder"]
