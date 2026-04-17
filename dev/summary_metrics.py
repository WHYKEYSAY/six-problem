"""
summary_metrics.py

Compute summary metrics for different window and overlap configurations
in pseudo real-time EEG analysis.
"""

import numpy as np


def compute_summary_metrics(results_df, window_sec, overlap_ratio):
    """
    Compute summary metrics for a given results_df.

    Parameters
    ----------
    results_df : pandas.DataFrame
        DataFrame containing computed EEG states and metadata.
    window_sec : float
        Window size in seconds.
    overlap_ratio : float
        Overlap ratio (0 ~ 1).

    Returns
    -------
    dict
        Dictionary of summary metrics.
    """

    # -------------------------
    # Basic parameters
    # -------------------------
    step_sec = window_sec * (1 - overlap_ratio)
    n_updates = len(results_df)

    # -------------------------
    # 1. Delay
    # -------------------------
    mean_processing_delay_ms = results_df["processing_delay_ms"].mean()
    decision_latency_sec = window_sec + mean_processing_delay_ms / 1000.0

    # -------------------------
    # 2. Valid window ratio
    # -------------------------
    artifact_windows = results_df["artifact_flag"].sum()
    valid_window_ratio = 1 - artifact_windows / n_updates if n_updates > 0 else np.nan

    # -------------------------
    # 3. Stability (mean abs diff)
    # -------------------------
    def mean_abs_diff(series):
        series = series.dropna()
        if len(series) < 2:
            return np.nan
        return np.mean(np.abs(np.diff(series)))

    mean_abs_diff_workload = mean_abs_diff(results_df["workload_z"])
    mean_abs_diff_engagement = mean_abs_diff(results_df["engagement_z"])
    mean_abs_diff_stress = mean_abs_diff(results_df["stress_z"])

    # -------------------------
    # 4. Label switch rate
    # -------------------------
    def label_switch_rate(labels):
        labels = labels.dropna().values
        if len(labels) < 2:
            return np.nan
        switches = np.sum(labels[:-1] != labels[1:])
        return switches / (len(labels) - 1)

    label_switch_rate_workload = label_switch_rate(results_df["workload_label"])
    label_switch_rate_engagement = label_switch_rate(results_df["engagement_label"])
    label_switch_rate_stress = label_switch_rate(results_df["stress_label"])

    # -------------------------
    # 5. Separation (mean abs z)
    # -------------------------
    def mean_abs(series):
        series = series.dropna()
        if len(series) == 0:
            return np.nan
        return np.mean(np.abs(series))

    mean_abs_workload_z = mean_abs(results_df["workload_z"])
    mean_abs_engagement_z = mean_abs(results_df["engagement_z"])
    mean_abs_stress_z = mean_abs(results_df["stress_z"])

    # -------------------------
    # Summary
    # -------------------------
    summary = {
        "window_sec": window_sec,
        "overlap_ratio": overlap_ratio,
        "step_sec": step_sec,

        "mean_processing_delay_ms": mean_processing_delay_ms,
        "decision_latency_sec": decision_latency_sec,

        "valid_window_ratio": valid_window_ratio,

        "mean_abs_diff_workload": mean_abs_diff_workload,
        "mean_abs_diff_engagement": mean_abs_diff_engagement,
        "mean_abs_diff_stress": mean_abs_diff_stress,

        "label_switch_rate_workload": label_switch_rate_workload,
        "label_switch_rate_engagement": label_switch_rate_engagement,
        "label_switch_rate_stress": label_switch_rate_stress,

        "mean_abs_workload_z": mean_abs_workload_z,
        "mean_abs_engagement_z": mean_abs_engagement_z,
        "mean_abs_stress_z": mean_abs_stress_z,
    }

    return summary
