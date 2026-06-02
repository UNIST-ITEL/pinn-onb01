"""fig:ablation — test-accuracy progression v3→v11 (RMSE bars + R2 line).

Values are the committed test-split metrics from PROGRESS_LOG.md § 훈련 실험 결과.
Edit the arrays below if the experiment table changes.
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
from figlib import set_style, save_fig

# Reader-facing sequential stages S1–S8 (internal config/checkpoint versions in
# parentheses, see PROGRESS_LOG.md § 훈련 실험 결과): S1=v3, S2=v5, S3=v6, S4=v7,
# S5=v8, S6=v9, S7=v10, S8=v11 (v4 produced no gain and is omitted).
STAGES = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
RMSE = [7.56, 5.56, 4.02, 1.85, 2.03, 1.91, 2.00, 1.84]   # test RMSE_dT [K]
R2   = [0.377, 0.545, 0.623, 0.769, 0.706, 0.740, 0.717, 0.768]
CHG  = ["transfer\nbaseline", "+4 papers", "clean\n(−pool/P)", "−Basu 2002\n(all pool)",
        "+microchannel\n(Qu)", "one-sided\nHsu", "reduced\npressure", "+high-P\n(Wang)"]


def main() -> None:
    set_style()
    x = np.arange(len(STAGES))
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.bar(x, RMSE, color="#5C6BC0", alpha=0.85, edgecolor="k", lw=0.5)
    ax1.set_ylabel("Test RMSE$_{\\Delta T_{ONB}}$ [K]", color="#3949AB"); ax1.set_ylim(0, 8.5)
    ax1.set_xticks(x); ax1.set_xticklabels(STAGES)
    for xi, r, ch in zip(x, RMSE, CHG):
        ax1.annotate(ch, (xi, r + 0.15), ha="center", fontsize=6.8, color="#444")
    ax2 = ax1.twinx(); ax2.plot(x, R2, "o-", color="#E65100", lw=2, ms=6)
    ax2.set_ylabel("$R^2_{\\Delta T_{ONB}}$", color="#E65100"); ax2.set_ylim(0, 1)
    ax2.spines["top"].set_visible(False)
    ax1.annotate("", xy=(7, 1.84), xytext=(0, 7.56),
                 arrowprops=dict(arrowstyle="->", color="#388E3C", lw=1.5, alpha=0.5))
    ax1.text(3.2, 6.3, "−76% RMSE", color="#388E3C", fontsize=10, rotation=-20)
    save_fig(fig, "fig_ablation_progression")


if __name__ == "__main__":
    main()
