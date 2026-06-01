"""fig:persource — per-source ΔT_ONB RMSE bar chart (v11, all data)."""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from figlib import set_style, save_fig, load_v11, load_dataframe, predict_dT


def main() -> None:
    set_style()
    model, device, _ = load_v11()
    ds, df = load_dataframe("all")
    df = df.copy(); df["pred"] = predict_dT(model, device, ds)
    d = df[df.delta_T_onb_K > 0].copy(); d["ae"] = np.abs(d.pred - d.delta_T_onb_K)
    g = (d.groupby("paper_id")
           .apply(lambda x: pd.Series({"rmse": np.sqrt((x.ae ** 2).mean()), "n": len(x)}))
           .sort_values("rmse"))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(range(len(g)), g.rmse, color="#26A69A", edgecolor="k", lw=0.4)
    ax.set_yticks(range(len(g)))
    ax.set_yticklabels([f"{i} (n={int(n)})" for i, n in zip(g.index, g.n)])
    ax.set_xlabel("$\\Delta T_{ONB}$ RMSE [K]")
    ax.set_title("Per-source wall-superheat error (PINN v11, all data)")
    ax.axvline(1.84, ls="--", color="#C62828", lw=1.2)
    ax.text(1.9, 0.1, "overall test 1.84 K", color="#C62828", fontsize=8.5)
    for i, r in enumerate(g.rmse):
        ax.text(r + 0.05, i, f"{r:.2f}", va="center", fontsize=8)
    fig.tight_layout()
    save_fig(fig, "fig_per_source_rmse")


if __name__ == "__main__":
    main()
