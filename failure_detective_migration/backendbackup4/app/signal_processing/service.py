"""Signal ingestion and reference-comparison services."""
from __future__ import annotations

import io
from typing import Mapping

import numpy as np
import pandas as pd
import requests
from scipy.io import loadmat

from app.diagnostics.engine import window_features, build_baseline, assess_against_baseline, symptoms_from_sensor_assessment


def read_sensor_bytes(filename: str, content: bytes) -> dict[str, np.ndarray]:
    """Read CSV/TXT/MAT uploads. Channel units remain caller-supplied metadata."""
    if not content:
        raise ValueError("The uploaded file is empty.")
    name = filename.lower()
    try:
        if name.endswith((".csv", ".txt")):
            frame = pd.read_csv(io.BytesIO(content), sep=None, engine="python")
            channels = {}
            for col in frame.columns:
                values = pd.to_numeric(frame[col], errors="coerce").dropna().to_numpy(dtype=float)
                values = values[np.isfinite(values)]
                if values.size >= 128:
                    channels[str(col)] = values
            if not channels:
                raise ValueError("No numeric sensor channel with at least 128 samples was found.")
            return channels
        if name.endswith(".mat"):
            mat = loadmat(io.BytesIO(content))
            channels = {}
            for key, value in mat.items():
                if key.startswith("__"):
                    continue
                arr = np.asarray(value)
                if arr.dtype.kind in "iuf" and arr.size >= 128:
                    arr = np.squeeze(arr).astype(float).ravel()
                    arr = arr[np.isfinite(arr)]
                    if arr.size >= 128:
                        canonical = str(key)
                        for suffix in ("DE_time", "FE_time", "BA_time"):
                            if canonical.endswith(suffix):
                                canonical = suffix
                                break
                        channels[canonical] = arr
            if not channels:
                raise ValueError("No numeric MATLAB channel with at least 128 samples was found.")
            return channels
    except Exception as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Could not read {filename}: {exc}") from exc
    raise ValueError("Upload a CSV, TXT, or MATLAB .mat file.")


def load_builtin_cwru_recordings() -> dict[str, dict[str, np.ndarray]]:
    """Fetch selected CWRU recordings; these are lab recordings, not live data."""
    root = "https://raw.githubusercontent.com/s-whynot/CWRU-dataset/main/"
    source_files = {
        "healthy": root + "Normal/97_Normal_0.mat",
        "inner_race_fault": root + "12k_Drive_End_Bearing_Fault_Data/IR/007/105_0.mat",
        "ball_fault": root + "12k_Drive_End_Bearing_Fault_Data/B/007/118_0.mat",
        "outer_race_fault": root + "12k_Drive_End_Bearing_Fault_Data/OR/007/130_0.mat",
    }
    output = {}
    for label, url in source_files.items():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        mat = loadmat(io.BytesIO(response.content))
        signal = None
        for key, value in mat.items():
            if key.startswith("__") or not key.endswith("DE_time"):
                continue
            arr = np.asarray(value).squeeze().astype(float).ravel()
            arr = arr[np.isfinite(arr)]
            if arr.size >= 128:
                signal = arr
                break
        if signal is None:
            raise ValueError(f"No drive-end vibration channel found in {label} recording.")
        output[label] = {"DE_time": signal}
    return output


def analyse_against_healthy(test_channels: Mapping[str, np.ndarray], healthy_channels: Mapping[str, np.ndarray]) -> dict:
    baseline = build_baseline(healthy_channels)
    assessment = assess_against_baseline(test_channels, baseline)
    symptoms, evidence = symptoms_from_sensor_assessment(assessment)
    return {
        "features": assessment.replace({np.nan: None}).to_dict(orient="records"),
        "inferred_symptoms": symptoms,
        "evidence_notes": evidence,
        "method_note": "Empirical comparison against the selected healthy reference; not a universal machine threshold or standalone fault classifier.",
    }
