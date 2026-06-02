"""fig:trends — physical-trend consistency (v11).

(a) model ΔT_ONB increases with subcooling (synthetic sweep);
(b) measured ΔT_ONB increases with heat flux (in-source data, Hsu coupling).
The pressure trend is shown separately in fig_pressure_trend (the synthetic P
sweep is non-monotone at a single base condition, so it is omitted here).
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np, torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from figlib import set_style, save_fig, load_v11, load_dataframe, SOURCE_LABELS
from data.dataset import collate_fn

# flow_numeric channel indices: 4 = ΔT_sub/T_sat
CH_SUB = 4
T_SAT_APPROX = 380.0   # K, for converting subcooling ratio back to ~K on the axis


def main() -> None:
    set_style()
    model, device, _ = load_v11()
    ds, df = load_dataframe("all")
    b = next(iter(DataLoader(ds, batch_size=1, shuffle=False, collate_fn=collate_fn)))
    bsn = b["surface_features"]["numeric"][0]
    bsc = b["surface_features"]["category_id"][0]
    bfn = b["flow_numeric"][0].clone()

    def sweep(idx, rng, n=30):
        fb = bfn.unsqueeze(0).expand(n, -1).clone()
        fb[:, idx] = torch.linspace(rng[0], rng[1], n)
        sf = {"numeric": bsn.unsqueeze(0).expand(n, -1).to(device),
              "category_id": bsc.unsqueeze(0).expand(n).to(device)}
        with torch.no_grad():
            o = model(torch.full((n, 1), 0.5, device=device), sf, fb.to(device))
        return (o.delta_T_onb_star.squeeze(-1) * 20).cpu().numpy()

    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    xs = np.linspace(0, 0.25, 30)
    ya = sweep(CH_SUB, (0, 0.25))
    dT_axis = xs * T_SAT_APPROX
    axs[0].plot(dT_axis, ya, "-", color="#2E7D32", lw=2.4)
    axs[0].set_xlabel("$\\Delta T_{sub}$ [K]"); axs[0].set_ylabel("predicted $\\Delta T_{ONB}$ [K]")
    axs[0].set_title("(a)", loc="left", fontweight="bold", fontsize=12)
    # The sign is correct but the magnitude is small — state it so the zoomed
    # y-axis is not read as a strong dependence.
    axs[0].annotate(f"monotonic, but weak:\n$\\Delta(\\Delta T_{{ONB}})\\approx{ya[-1]-ya[0]:+.2f}$ K "
                    f"over 0–{dT_axis[-1]:.0f} K",
                    xy=(0.05, 0.93), xycoords="axes fraction", fontsize=8.5, va="top", color="#2E7D32")

    for pid, c in [("cheng2022", "#6A1B9A"), ("qu2002", "#00838F"),
                   ("kuang2025", "#EF6C00"), ("liu2005", "#1565C0")]:
        d = df[(df.paper_id == pid) & (df.delta_T_onb_K > 0) & (df.q_onb_W_m2 > 0)]
        if len(d):
            axs[1].scatter(d.q_onb_W_m2 / 1e3, d.delta_T_onb_K, s=20, color=c, alpha=0.65,
                           label=SOURCE_LABELS.get(pid, pid))
    axs[1].set_xscale("log"); axs[1].set_xlabel("$q''_{ONB}$ [kW m$^{-2}$]")
    axs[1].set_ylabel("$\\Delta T_{ONB}$ [K]")
    axs[1].set_title("(b)", loc="left", fontweight="bold", fontsize=12)
    axs[1].legend(fontsize=8)
    fig.tight_layout()
    save_fig(fig, "fig_physics_trends")


if __name__ == "__main__":
    main()
