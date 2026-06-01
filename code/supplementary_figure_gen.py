"""
Neural Timescale Analysis -- iSTTC Method
==========================================
Plots:
  - Effective Intrinsic Timescale x Firing Rate
  - tau_eff Population Distribution
  - Timescale Components Distribution

Usage:
    python dashboard.py
    python dashboard.py --csv /path/to/good_isttc.csv
    python dashboard.py --csv /path/to/good_isttc.csv --output /path/to/output_dir

Requirements:
    pip install numpy pandas matplotlib seaborn
"""

# -- 0. Imports ----------------------------------------------------------------
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings, os
warnings.filterwarnings("ignore")

# =============================================================================
# PATHS  —  edit these defaults or pass as command-line arguments
# =============================================================================
DEFAULT_CSV_PATH   = 'good_isttc.csv'
DEFAULT_OUTPUT_DIR = 'isttc_summary_plots'


def parse_args():
    parser = argparse.ArgumentParser(description='Supplementary Figure Generator')
    parser.add_argument('--csv',    default=DEFAULT_CSV_PATH,
                        help=f'Path to good_isttc.csv (default: {DEFAULT_CSV_PATH})')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_DIR,
                        help=f'Output directory for plots (default: {DEFAULT_OUTPUT_DIR})')
    return parser.parse_args()


# -- Plotting style ------------------------------------------------------------
COLOR_SHORT = "#4C72B0"
COLOR_MID   = "#DD8452"
COLOR_LONG  = "#C44E52"

sns.set_theme(style="whitegrid", font_scale=1.1)
FIG_KW = dict(dpi=150, facecolor="white")

TAU = "tau_eff"


# ==============================================================================
# Timescale Components Distribution
# ==============================================================================
def plot_01_n_components(df, output_dir):
    if "n_components" not in df.columns:
        print("WARNING: 'n_timescales' column not found -- skipping Timescale Components Distribution.")
        return
    counts = df["n_components"].value_counts().sort_index()
    fracs  = counts / counts.sum() * 100

    fig, ax = plt.subplots(figsize=(6, 5), **FIG_KW)
    bars = ax.bar(fracs.index.astype(str), fracs.values,
                  color=[COLOR_SHORT, COLOR_MID, COLOR_LONG, "#9467bd"],
                  edgecolor="white", linewidth=0.6)
    for bar, pct in zip(bars, fracs.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5, f"{pct:.1f}%",
                ha="center", fontsize=10)
    ax.set_xlabel("Number of Timescale Components", fontsize=12)
    ax.set_ylabel("% of Units", fontsize=12)
    ax.set_title("Timescale Components Distribution", fontsize=13)
    ax.set_ylim(0, fracs.max() * 1.15)
    fig.tight_layout()
    out = os.path.join(output_dir, "plot_01_n_components.png")
    fig.savefig(out, **FIG_KW)
    plt.show()
    print(f"Saved: {out}")

# ==============================================================================
# Effective Intrinsic Timescale x Firing Rate
# ==============================================================================
def plot_02_fr(df, output_dir):
    if "firing_rate" not in df.columns:
        print("WARNING: 'firing_rate_hz' column not found -- skipping Effective Intrinsic Timescale x Firing Rate.")
        return
    bins   = [0, 1, 2, 5, 10, 20, 50, 200]
    labels = ["<1", "1-2", "2-5", "5-10", "10-20", "20-50", ">50"]
    df2 = df.copy()
    df2["fr_bin"] = pd.cut(df2["firing_rate"], bins=bins, labels=labels)

    fig, ax = plt.subplots(figsize=(11, 6), **FIG_KW)
    sns.boxplot(
        data=df2, x="fr_bin", y=TAU, order=labels,
        color=COLOR_SHORT, showfliers=False, linewidth=0.9, ax=ax
    )
    ax.set_title("Effective Intrinsic Timescale x Firing Rate\n"
                 "No simple inverse relationship | whiskers = 1.5×IQR",
                 fontsize=20)
    ax.set_yscale("log")
    ax.set_xlabel("Firing Rate Bin (Hz)", fontsize=20)
    ax.set_ylabel("tau_eff (ms)", fontsize=20)
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.tick_params(axis='both', labelsize=16)
    fig.tight_layout()
    out = os.path.join(output_dir, "plot_02_fr.png")
    fig.savefig(out, **FIG_KW)
    plt.show()
    print(f"Saved: {out}")


# ==============================================================================
# tau_eff Population Distribution
# ==============================================================================
def plot_03_tau_dist(df, output_dir):
    vals = df[TAU].dropna()
    bins = np.logspace(np.log10(vals.quantile(0.005)),
                       np.log10(vals.quantile(0.995)), 60)

    fig, ax = plt.subplots(figsize=(9, 5), **FIG_KW)
    ax.hist(vals, bins=bins, color=COLOR_SHORT, edgecolor="white", linewidth=0.4)
    ax.set_xscale("log")
    ax.set_xlabel("tau_eff (ms) [log scale]", fontsize=12)
    ax.set_ylabel("Unit Count", fontsize=12)
    ax.set_title("tau_eff Population Distribution\n"
                 "Right-skewed; mode ~100 ms; long tail from brainstem units",
                 fontsize=13)
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    fig.tight_layout()
    out = os.path.join(output_dir, "plot_03_tau_dist.png")
    fig.savefig(out, **FIG_KW)
    plt.show()
    print(f"Saved: {out}")


# -- Main ----------------------------------------------------------------------
def main():
    args = parse_args()

    CSV_PATH   = args.csv
    OUTPUT_DIR = args.output
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"CSV not found: {CSV_PATH}\n"
            f"Run isttc_pipeline.py first, or pass --csv /path/to/good_isttc.csv"
        )

    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df):,} rows x {df.shape[1]} columns")

    # Column name map
    COLUMN_MAP = {
        "tau_eff":      "tau_effective_ms",
        "n_components": "n_timescales",
        "firing_rate":  "firing_rate_hz",
    }
    rename_map = {v: k for k, v in COLUMN_MAP.items() if v in df.columns}
    missing    = {k: v for k, v in COLUMN_MAP.items() if v not in df.columns}
    df = df.rename(columns=rename_map)

    if missing:
        print("WARNING: The following expected columns were NOT found:")
        for internal, csv_col in missing.items():
            print(f"  '{csv_col}' (needed for '{internal}')")

    print(f"Output folder: {OUTPUT_DIR}\n")

    plot_03_fr(df, OUTPUT_DIR)
    plot_05_tau_dist(df, OUTPUT_DIR)
    plot_06_n_components(df, OUTPUT_DIR)

    print("\nAll plots saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
