"""fig:designmap — predicted ΔT_ONB over the (G, P) plane (v11).

Fixed representative surface (reused from a stainless_steel dataset row),
water, D_h=3 mm, ΔT_sub=20 K, q unknown (Bo channel = 0). The surface tensor is
borrowed from a dataset sample to avoid importing the Phase-1 surface encoder.
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np, torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Subset
from figlib import set_style, save_fig, load_v11, load_dataframe
from data.dataset import collate_fn
from model.flow_encoder import encode_flow_to_tensor, FlowFeatures

SURF_CAT = "stainless_steel"
D_H_MM = 3.0
SUBCOOL_K = 20.0
N = 36


def main() -> None:
    set_style()
    model, device, _ = load_v11()
    ds, df = load_dataframe("all")

    # borrow a stainless_steel sample's surface tensor
    pos = int(np.where(df.surface_cat.values == SURF_CAT)[0][0])
    b0 = next(iter(DataLoader(Subset(ds, [pos]), batch_size=1, collate_fn=collate_fn)))
    snum = b0["surface_features"]["numeric"].to(device)
    scat = b0["surface_features"]["category_id"].to(device)

    Gs = np.linspace(200, 2000, N)
    Ps = np.logspace(np.log10(150), np.log10(16000), N)   # kPa
    Z = np.zeros((len(Ps), len(Gs)))
    with torch.no_grad():
        for i, P in enumerate(Ps):
            for j, G in enumerate(Gs):
                ff = FlowFeatures.from_dataset_row(
                    G_kg_m2s=float(G), D_h_mm=D_H_MM, channel_type="narrow_rectangular",
                    delta_T_sub_K=SUBCOOL_K, fluid="water", P_kPa=float(P), q_onb_W_m2=None)
                ft = encode_flow_to_tensor(ff).unsqueeze(0).to(device)
                o = model(torch.tensor([[0.5]], device=device),
                          {"numeric": snum, "category_id": scat}, ft)
                Z[i, j] = float(o.delta_T_onb_star.squeeze() * 20.0)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    cf = ax.contourf(Gs, Ps / 1000, Z, levels=18, cmap="viridis")
    cs = ax.contour(Gs, Ps / 1000, Z, levels=8, colors="white", linewidths=0.6, alpha=0.65)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")
    ax.set_yscale("log")
    ax.set_xlabel("Mass flux $G$ [kg m$^{-2}$s$^{-1}$]"); ax.set_ylabel("Pressure $P$ [MPa]")
    plt.colorbar(cf, ax=ax, label="predicted $\\Delta T_{ONB}$ [K]")
    save_fig(fig, "fig_design_map")


if __name__ == "__main__":
    main()
