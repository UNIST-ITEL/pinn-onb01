"""
WebPlotDigitizer raw CSV → SCHEMA.md 표준 CSV 변환기.

입력: 02_data/raw/literature/{paper_id}/{paper_id}_fig{N}_{label}_wpd.csv (header 없음, x,y)
출력: 같은 폴더의 표준 CSV (SCHEMA.md 헤더) + sidecar .meta.yaml

사용:
  python3 02_data/scripts/standardize_wpd.py BETZ_2013
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIT_ROOT = PROJECT_ROOT / "02_data" / "raw" / "literature"


@dataclass
class FigureSpec:
    """Figure별 단위·축 정의.

    지원 축 조합:
      (x=delta_T_wall, y=q_flux)   — 표준 비등 곡선
      (x=delta_T_wall, y=HTC)      — HTC 곡선; q_flux = HTC * delta_T
      (x=q_flux, y=HTC)            — Phan 12a 형태; delta_T = q_flux / HTC
    """
    figure: str                       # 예: "4", "6b", "7b", "12a"
    y_kind: str                       # "HTC" | "q_flux"
    y_unit_raw: str                   # 원 논문 표기
    y_to_si: Callable[[float], float] # y_raw → W/m²K (HTC) 또는 W/m² (q_flux)
    x_kind: str = "delta_T_wall"      # "delta_T_wall" | "q_flux"
    x_unit_raw: str = "K"
    x_to_si: Callable[[float], float] = lambda x: x  # default: K → K (no-op)
    fluid_override: str | None = None  # PaperSpec.fluid를 figure 단위로 덮어쓰기
    is_onb_diagram: bool = False       # x=theta, y=ΔT_ONB 형태 (Bourdon 2015 Fig.3)
    q_flux_onb_fixed: float = 0.0      # ONB diagram 모드에서 사용할 고정 q_flux [W/m²]
    pages: str = ""
    notes: str = ""


@dataclass
class PaperSpec:
    """논문별 메타데이터 + Figure 사양."""
    paper_id: str
    doi: str
    fluid: str
    pressure_atm: float
    subcooling_K: float
    figures: dict[str, FigureSpec]
    surface_card_map: dict[str, str] = field(default_factory=dict)
    onb_hint_K: dict[str, tuple[float, float]] = field(default_factory=dict)
    digitizer_user: str = "leejs92"
    digitized_date: str = "2026-05-09"


# ============================================================================
# 논문별 사양 (필요한 만큼 추가)
# ============================================================================

BETZ_2013 = PaperSpec(
    paper_id="BETZ_2013",
    doi="10.1016/j.ijheatmasstransfer.2012.10.080",
    fluid="water",
    pressure_atm=1.0,
    subcooling_K=0.0,
    figures={
        "4": FigureSpec(
            figure="4",
            y_kind="q_flux",
            y_unit_raw="W/cm2",
            y_to_si=lambda y: y * 10000.0,  # W/cm² → W/m²
            pages="10-11",
            notes="Boiling curve q'' vs delta_T (linear axes). Unit reinterpreted from initial HTC assumption to W/cm2 heat flux based on physical range check.",
        ),
        "6b": FigureSpec(
            figure="6b",
            y_kind="q_flux",
            y_unit_raw="W/cm2",
            y_to_si=lambda y: y * 10000.0,  # W/cm² → W/m²
            pages="13-14",
            notes="Heat flux vs delta_T (linear axes).",
        ),
        "7b": FigureSpec(
            figure="7b",
            y_kind="q_flux",
            y_unit_raw="W/cm2",
            y_to_si=lambda y: y * 10000.0,  # W/cm² → W/m²
            pages="14-15",
            notes="Boiling-curve comparison with literature (Jones, Chen, Li). y in W/cm2.",
        ),
    },
    surface_card_map={  # 미정인 표면은 UNASSIGNED
        "Hydrophilic": "UNASSIGNED",
        "Hydrophobic": "UNASSIGNED",
        "SHPi": "UNASSIGNED",
        "SHPo": "UNASSIGNED",
        "Superhydrophilic": "UNASSIGNED",
        "Biphilic": "UNASSIGNED",
        "Superbiphilic": "UNASSIGNED",
        "Superbiphiliccircle": "UNASSIGNED",
        "Superbiphilichexagon": "UNASSIGNED",
        "hydrophilic": "UNASSIGNED",
        "Chen2009": "EXTERNAL_REF",      # 외부 reference 데이터
        "Li2008": "EXTERNAL_REF",
        "Jones10um": "EXTERNAL_REF",
        "JonesPolished": "EXTERNAL_REF",
    },
    onb_hint_K={
        # 시리즈명 → (lo, hi) ΔT_ONB 추정 범위
        "Hydrophilic": (10.0, 15.0),
        "hydrophilic": (10.0, 15.0),
        "Hydrophobic": (2.0, 5.0),
        "SHPi": (2.0, 5.0),
        "Superhydrophilic": (2.0, 5.0),
        "SHPo": (0.0, 2.0),
        "Biphilic": (0.0, 5.0),
        "Superbiphilic": (0.0, 5.0),
        "Superbiphiliccircle": (0.0, 5.0),
        "Superbiphilichexagon": (0.0, 5.0),
    },
)

JO_2011 = PaperSpec(
    paper_id="JO_2011",
    doi="10.1016/j.ijheatmasstransfer.2011.06.001",
    fluid="water",
    pressure_atm=1.0,
    subcooling_K=0.0,
    figures={
        "3": FigureSpec(
            figure="3",
            y_kind="q_flux",
            y_unit_raw="kW/m2",
            y_to_si=lambda y: y * 1000.0,  # kW/m² → W/m²
            pages="5-6",
            notes="Boiling curve q'' [kW/m2] vs delta_T_wall [K], linear axes.",
        ),
        # Fig.4, Fig.5는 HTC vs q'' (역방향 축) — 보조, 우선순위 낮음
    },
    surface_card_map={
        "Hydrophilic": "UNASSIGNED",
        "Hydrophobic": "UNASSIGNED",
        # Fig.4/Fig.5 추출 시 추가 가능: 100A150, 100B150, 100B600, 50A150, 300A150, 500A150
    },
    onb_hint_K={
        "Hydrophilic": (8.0, 12.0),    # 저자 명시 ~10K
        "Hydrophobic": (1.0, 4.0),     # 저자 명시 1-3K
    },
)


PHAN_2009 = PaperSpec(
    paper_id="PHAN_2009",
    doi="10.1016/j.ijheatmasstransfer.2009.06.032",
    fluid="water",
    pressure_atm=1.0,
    subcooling_K=15.0,             # 과냉! T_bulk = 85°C, T_sat = 100°C
    figures={
        "12a": FigureSpec(
            figure="12a",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,    # kW/m² → W/m²
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,             # W/m²K → W/m²K (no-op)
            pages="8-9",
            notes="HTC vs q_flux (axes reversed). delta_T = q_flux / HTC. Subcooled (ΔT_sub=15K).",
        ),
    },
    surface_card_map={
        # 시리즈 라벨: theta{XX} = 접촉각 (Figure 12a 5종 표면)
        "theta22": "UNASSIGNED",     # SiOx PECVD (친수)
        "theta31": "UNASSIGNED",     # TiO₂ NNBD (친수)
        "theta67": "UNASSIGNED",     # Pt MOCVD (약친수)
        "theta80": "UNASSIGNED",     # Fe₂O₃ MOCVD (중성)
        "theta85": "UNASSIGNED",     # 무코팅 ref (중성)
    },
    onb_hint_K={
        # 저자 명시: Figure 12a에 "ONB" 레이블이 각 커브 굴곡점에 표시됨
        # 과냉 조건(ΔT_sub=15K)에서 친수 표면은 ONB 늦게, 소수 표면은 일찍 발생
        "theta22": (12.0, 25.0),    # 친수 SiOx — ONB 늦음
        "theta31": (10.0, 22.0),    # 친수 TiO₂
        "theta67": (5.0, 18.0),     # 약친수 Pt
        "theta80": (5.0, 15.0),     # 중성 Fe₂O₃
        "theta85": (5.0, 15.0),     # 무코팅 ref
    },
)


JONES_2009 = PaperSpec(
    paper_id="JONES_2009",
    doi="10.1115/1.3220144",
    fluid="water",                  # default; Fig.4a는 fluid_override로 FC-77
    pressure_atm=1.0,
    subcooling_K=0.0,
    figures={
        "3a": FigureSpec(
            figure="3a",
            y_kind="q_flux",
            y_unit_raw="kW/m2",
            y_to_si=lambda y: y * 1000.0,
            x_kind="delta_T_wall",
            x_unit_raw="K",
            fluid_override="water",
            pages="4-5",
            notes="Boiling curve (water) q'' [kW/m2] vs delta_T [K]. 5 surfaces (Polished + 4 EDM).",
        ),
        "4a": FigureSpec(
            figure="4a",
            y_kind="q_flux",
            y_unit_raw="kW/m2",
            y_to_si=lambda y: y * 1000.0,
            x_kind="delta_T_wall",
            x_unit_raw="K",
            fluid_override="FC-77",
            pages="5-6",
            notes="Boiling curve (FC-77) q'' [kW/m2] vs delta_T [K]. 5 surfaces.",
        ),
    },
    surface_card_map={
        "Polished": "UNASSIGNED",   # Ra=0.027 (FC-77) / 0.038 (water)
        "EDM1p08": "UNASSIGNED",    # Ra=1.08 μm
        "EDM2p22": "UNASSIGNED",    # Ra=2.22 μm
        "EDM5p89": "UNASSIGNED",    # Ra=5.89 μm
        "EDM10p0": "UNASSIGNED",    # Ra=10.0 μm
    },
    onb_hint_K={
        # 저자 명시: Polished water q_ONB≈15 kW/m², ΔT_ONB≈10.8K
        # FC-77은 더 낮은 ΔT에서 비등 (잘 젖음), q_ONB≈20 kW/m²
        # EDM 거칠수록 ΔT_ONB 감소 (거칠기 효과)
        "Polished": (8.0, 14.0),    # 저자 명시 ~10.8K (water 기준)
        "EDM1p08": (4.0, 10.0),     # 거칠어질수록 ΔT_ONB 감소
        "EDM2p22": (3.0, 9.0),
        "EDM5p89": (2.0, 8.0),
        "EDM10p0": (2.0, 7.0),
    },
)


BOURDON_2012 = PaperSpec(
    paper_id="BOURDON_2012",
    doi="10.1021/la203636a",
    fluid="water",
    pressure_atm=1.0,
    subcooling_K=0.0,
    figures={
        "4": FigureSpec(
            figure="4",
            y_kind="q_flux",
            y_unit_raw="kW/m2",
            y_to_si=lambda y: y * 1000.0,
            x_kind="delta_T_wall",
            x_unit_raw="K",
            pages="5",
            notes="Roughness effect on boiling onset — 3 ungrafted surfaces (S1 rougher → S3 smoother), all theta=0°.",
        ),
        "6": FigureSpec(
            figure="6",
            y_kind="q_flux",
            y_unit_raw="kW/m2",
            y_to_si=lambda y: y * 1000.0,
            x_kind="delta_T_wall",
            x_unit_raw="K",
            pages="6",
            notes="Wettability effect on boiling onset — S1 surface with 3 graftings (ungrafted/whole/center).",
        ),
    },
    surface_card_map={
        # Fig.4: 거칠기 비교 (모두 ungrafted, theta=0°)
        "S1": "UNASSIGNED",          # 가장 거침 (Sa~9.7nm)
        "S2": "UNASSIGNED",          # 중간
        "S3": "UNASSIGNED",          # 가장 매끈 (Sa~7.6nm)
        # Fig.6: 젖음성 비교 (모두 S1 거칠기, 처리만 다름)
        "ungrafted": "UNASSIGNED",   # theta=0°, 동일 S1 (Fig.4 S1과 동일 표면)
        "grafted_whole": "UNASSIGNED",  # theta=108° 전체 알칸티올 그라프팅
        "grafted_center": "UNASSIGNED", # theta=108° 중앙 15mm만 그라프팅
    },
    onb_hint_K={
        # 저자 명시:
        # Fig.4: S1=8.8K (rougher), S3=12.3K (smoother)
        # Fig.6: ungrafted=8.8K, grafted=5.1K
        "S1": (7.0, 11.0),           # 8.8K ± 0.4
        "S2": (8.0, 12.0),           # 중간 추정
        "S3": (10.0, 14.0),          # 12.3K ± 1.4
        "ungrafted": (7.0, 11.0),    # 8.8K (S1과 동일 표면)
        "grafted_whole": (3.5, 7.0), # 5.1K ± 0.8
        "grafted_center": (3.5, 7.0),# grafted와 유사 추정
    },
)


BOURDON_2015 = PaperSpec(
    paper_id="BOURDON_2015",
    doi="10.1016/j.cis.2015.04.004",
    fluid="water",
    pressure_atm=1.0,
    subcooling_K=0.0,
    figures={
        "3": FigureSpec(
            figure="3",
            x_kind="theta_contact",
            x_unit_raw="deg",
            x_to_si=lambda x: x,           # degree 그대로
            y_kind="delta_T_onb",
            y_unit_raw="K",
            y_to_si=lambda y: y,           # K 그대로
            is_onb_diagram=True,
            q_flux_onb_fixed=15000.0,      # 추정값 (BOURDON_2012 ungrafted ONB q ~1.6kW/m² 기준 — 측정 q 차이 가능)
            pages="5",
            notes="ONB diagram: ΔT_ONB vs theta. Each point is ONB. q_flux is sentinel (real measurement q not specified in text).",
        ),
        "7": FigureSpec(
            figure="7",
            x_kind="delta_T_wall",
            x_unit_raw="K",
            y_kind="q_flux",
            y_unit_raw="kW/m2",
            y_to_si=lambda y: y * 1000.0,
            pages="Appendix A",
            notes="Complete boiling curves. Per author: only OTS shows clear slope change (ONB).",
        ),
    },
    surface_card_map={
        # Fig.3 (ONB diagram): 4개 표면 (각 점이 곧 표면)
        "ONB_vs_theta": "UNASSIGNED",
        # Fig.7 (boiling curves): 4종 시리즈
        "NotGrafted": "UNASSIGNED",   # super-hydrophilic
        "MPEGPTMS": "UNASSIGNED",     # θ~35°
        "AcOUTES": "UNASSIGNED",      # θ~75°
        "OTS": "UNASSIGNED",          # θ~105°
    },
    onb_hint_K={
        # Fig.7 — only OTS shows clear ONB
        "OTS": (3.0, 8.0),            # author cross-reference: OTS ΔT_ONB ≈ 5.1K
        # 나머지 3종은 ONB 굴곡점 불분명 → 자동 식별이 noise 가능성
        "NotGrafted": (15.0, 25.0),
        "MPEGPTMS": (10.0, 20.0),
        "AcOUTES": (5.0, 15.0),
    },
)


JABARDO_2009 = PaperSpec(
    paper_id="JABARDO_2009",
    doi="10.1016/j.expthermflusci.2008.12.004",
    fluid="R-134a",                     # default; figure_override로 R-123도 처리
    pressure_atm=3.0,                   # 대표값 (각 fig에서 p_r 다름 — meta에 기록)
    subcooling_K=0.0,
    figures={
        # Fig.9 — 거칠기 효과 (구리, 4 서브플롯)
        "9a": FigureSpec(
            figure="9a",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,  # kW/m²K → W/m²K
            fluid_override="R-123",
            pages="8-9",
            notes="HTC vs q'' (axes reversed, log-log). Cu, R-123, p_r=0.011. delta_T = q/HTC. y in kW/m2K.",
        ),
        "9b": FigureSpec(
            figure="9b",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-123",
            pages="8-9",
            notes="HTC vs q'' (axes reversed, log-log). Cu, R-123, p_r=0.092.",
        ),
        "9c": FigureSpec(
            figure="9c",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-134a",
            pages="8-9",
            notes="HTC vs q'' (axes reversed, log-log). Cu, R-134a, p_r=0.063.",
        ),
        "9d": FigureSpec(
            figure="9d",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-134a",
            pages="8-9",
            notes="HTC vs q'' (axes reversed, log-log). Cu, R-134a, p_r=0.260.",
        ),
        # Fig.10 — 재질 효과 (Brass, Stainless Steel)
        "10a": FigureSpec(
            figure="10a",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-134a",
            pages="10",
            notes="HTC vs q'' (log-log). Brass, R-134a, p_r=0.063. 5 roughness levels.",
        ),
        "10b": FigureSpec(
            figure="10b",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-134a",
            pages="10",
            notes="HTC vs q'' (log-log). Brass, R-134a, p_r=0.260. 5 roughness levels.",
        ),
        "10c": FigureSpec(
            figure="10c",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-134a",
            pages="10",
            notes="HTC vs q'' (log-log). SS (stainless steel), R-134a, p_r=0.063. 7 roughness levels. Roughness effect weaker than Cu/Brass.",
        ),
        "10d": FigureSpec(
            figure="10d",
            x_kind="q_flux",
            x_unit_raw="kW/m2",
            x_to_si=lambda x: x * 1000.0,
            y_kind="HTC",
            y_unit_raw="kW/m2K",
            y_to_si=lambda y: y * 1000.0,
            fluid_override="R-134a",
            pages="10",
            notes="HTC vs q'' (log-log). SS (stainless steel), R-134a, p_r=0.260. 7 roughness levels.",
        ),
    },
    surface_card_map={
        # 재질_표면처리_Ra 형식 (논문 Table 1 기준)
        # Cu (구리) — Polished/Sandpaper/Shot-Peening
        "Cu_Ra0p07P": "UNASSIGNED",          # Polished
        "Cu_Ra0p16SP": "UNASSIGNED",         # Sandpaper Ra=0.16
        "Cu_Ra0p47SP": "UNASSIGNED",         # Sandpaper Ra=0.47
        "Cu_Ra0p5SP": "UNASSIGNED",          # Sandpaper Ra=0.50
        "Cu_Ra2p5SPI": "UNASSIGNED",         # Shot-Peening Ra=2.5
        "Cu_Ra3p3SPI": "UNASSIGNED",         # Shot-Peening Ra=3.3
        "Cu_Ra4p6SPI": "UNASSIGNED",         # Shot-Peening Ra=4.6
        "Cu_Ra10p5SPI": "UNASSIGNED",        # Shot-Peening Ra=10.5
        # Brass (황동) — Fig.10a/10b
        "Br_Ra0p08P": "UNASSIGNED",          # Polished Ra=0.08
        "Br_Ra0p90SP": "UNASSIGNED",         # Sandpaper Ra=0.90
        "Br_Ra1p2SPI": "UNASSIGNED",         # Shot-Peening Ra=1.2
        "Br_Ra1p8SPI": "UNASSIGNED",         # Shot-Peening Ra=1.8
        "Br_Ra3p5SPI": "UNASSIGNED",         # Shot-Peening Ra=3.5
        # Stainless Steel (SS) — Fig.10c/10d
        "SS_Ra0p03P": "UNASSIGNED",          # Polished Ra=0.03
        "SS_Ra0p07SP": "UNASSIGNED",         # Sandpaper Ra=0.07
        "SS_Ra0p45SP": "UNASSIGNED",         # Sandpaper Ra=0.45
        "SS_Ra0p90SPI": "UNASSIGNED",        # Shot-Peening Ra=0.90
        "SS_Ra1p45SPI": "UNASSIGNED",        # Shot-Peening Ra=1.45
        "SS_Ra2p50SPI": "UNASSIGNED",        # Shot-Peening Ra=2.50
        "SS_Ra3p20SPI": "UNASSIGNED",        # Shot-Peening Ra=3.20
    },
    onb_hint_K={
        # 저자 명시: Ra=10.5 μm는 q≈15 kW/m² 부근 슬로프 변화점
        # 거칠기↑ → ΔT_ONB↓ 경향
        "Cu_Ra0p07P": (8.0, 18.0),       # Polished — ONB 늦음
        "Cu_Ra0p16SP": (5.0, 15.0),
        "Cu_Ra0p47SP": (3.0, 12.0),
        "Cu_Ra0p5SP": (3.0, 12.0),       # 0.47과 유사
        "Cu_Ra2p5SPI": (2.0, 10.0),
        "Cu_Ra3p3SPI": (2.0, 9.0),
        "Cu_Ra4p6SPI": (2.0, 9.0),
        "Cu_Ra10p5SPI": (2.0, 8.0),      # Roughest — ONB 가장 빠름
        # Brass
        "Br_Ra0p08P": (5.0, 18.0),
        "Br_Ra0p90SP": (3.0, 12.0),
        "Br_Ra1p2SPI": (2.0, 10.0),
        "Br_Ra1p8SPI": (2.0, 10.0),
        "Br_Ra3p5SPI": (2.0, 8.0),
        # Stainless Steel — 거칠기 효과 약함 (저자 명시)
        "SS_Ra0p03P": (6.0, 20.0),
        "SS_Ra0p07SP": (5.0, 18.0),
        "SS_Ra0p45SP": (4.0, 14.0),
        "SS_Ra0p90SPI": (3.0, 12.0),
        "SS_Ra1p45SPI": (3.0, 12.0),
        "SS_Ra2p50SPI": (2.0, 10.0),
        "SS_Ra3p20SPI": (2.0, 10.0),
    },
)


PAPER_REGISTRY: dict[str, PaperSpec] = {
    "BETZ_2013": BETZ_2013,
    "JO_2011": JO_2011,
    "PHAN_2009": PHAN_2009,
    "JONES_2009": JONES_2009,
    "BOURDON_2012": BOURDON_2012,
    "BOURDON_2015": BOURDON_2015,
    "JABARDO_2009": JABARDO_2009,
}


# ============================================================================
# 파일명 파싱 — {paper_id}_fig{N}_{series}_wpd.csv
# ============================================================================

WPD_NAME = re.compile(
    r"^(?P<paper>[A-Z]+_\d{4})_fig(?P<fig>[\w]+?)_(?P<series>[\w\-]+?)_wpd\.csv$"
)


def parse_wpd_filename(path: Path) -> tuple[str, str, str] | None:
    """파일명에서 (paper_id, figure, series) 추출. fig는 raw 형식 그대로 반환."""
    m = WPD_NAME.match(path.name)
    if not m:
        return None
    paper = m.group("paper")
    fig = m.group("fig").lstrip("0")  # "06b" → "6b"
    return paper, fig, m.group("series")


def lookup_figure_spec(paper: PaperSpec, fig_id: str) -> FigureSpec | None:
    """fig_id를 paper.figures에서 lookup. 정확 매칭 실패 시 끝 'a' 제거 시도."""
    if fig_id in paper.figures:
        return paper.figures[fig_id]
    # "4a" → "4" 시도 (BETZ_2013의 "Fig 4" sub-panel)
    if fig_id.endswith("a") and len(fig_id) > 1:
        stripped = fig_id[:-1]
        if stripped in paper.figures:
            return paper.figures[stripped]
    return None


# ============================================================================
# ONB 자동 식별 (단순 휴리스틱)
# ============================================================================

def identify_onb_index(
    delta_T: list[float],
    q_flux: list[float],
    hint_range: tuple[float, float] | None = None,
) -> tuple[int | None, list[int]]:
    """
    ONB 후보 행 식별.
    1순위: hint_range가 주어지면 해당 범위 내 첫 포인트
    2순위: 기울기 d(q)/d(ΔT) 가 직전 대비 1.5배 이상 점프하는 첫 인덱스
    return: (onb_idx, candidates)
    """
    n = len(delta_T)
    if n < 3:
        return None, []

    # 인덱스 정렬
    order = sorted(range(n), key=lambda i: delta_T[i])
    candidates: list[int] = []

    # 1순위: hint_range 사용
    if hint_range is not None:
        lo, hi = hint_range
        for i in order:
            if lo <= delta_T[i] <= hi:
                candidates.append(i)
        if candidates:
            return candidates[0], candidates

    # 2순위: 슬로프 점프
    prev_slope = None
    for k in range(1, n):
        i_prev = order[k - 1]
        i_curr = order[k]
        dT = delta_T[i_curr] - delta_T[i_prev]
        if dT <= 0:
            continue
        slope = (q_flux[i_curr] - q_flux[i_prev]) / dT
        if prev_slope is not None and prev_slope > 0:
            ratio = slope / prev_slope
            if ratio > 1.5:
                candidates.append(i_curr)
                return i_curr, candidates
        prev_slope = slope

    return None, candidates


# ============================================================================
# 변환 메인 로직
# ============================================================================

@dataclass
class StandardRow:
    q_flux: float
    delta_T_wall: float
    delta_T_sub: float
    surface_id: str
    fluid: str
    source_paper: str
    figure_ref: str
    ONB_flag: bool
    notes: str

    def as_csv_row(self) -> list[str]:
        return [
            f"{self.q_flux:.2f}",
            f"{self.delta_T_wall:.4f}",
            f"{self.delta_T_sub:.4f}",
            self.surface_id,
            self.fluid,
            self.source_paper,
            self.figure_ref,
            "True" if self.ONB_flag else "False",
            self.notes,
        ]


HEADER = [
    "q_flux", "delta_T_wall", "delta_T_sub",
    "surface_id", "fluid", "source_paper",
    "figure_ref", "ONB_flag", "notes",
]


def load_wpd_csv(path: Path) -> tuple[list[float], list[float]]:
    xs: list[float] = []
    ys: list[float] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue
            try:
                x = float(parts[0])
                y = float(parts[1])
            except ValueError:
                continue
            xs.append(x)
            ys.append(y)
    return xs, ys


def make_rows(
    xs: list[float],
    ys: list[float],
    paper: PaperSpec,
    fig: FigureSpec,
    series: str,
) -> tuple[list[StandardRow], int | None, list[int]]:
    """축 조합별 ΔT/q 변환 + ONB 식별. delta_T_wall 오름차순 정렬."""
    # 1) SI 변환
    xs_si = [fig.x_to_si(x) for x in xs]
    ys_si = [fig.y_to_si(y) for y in ys]

    surface_id = paper.surface_card_map.get(series, "UNASSIGNED")
    fig_ref = f"Fig{fig.figure}_{series}"
    fluid = fig.fluid_override if fig.fluid_override else paper.fluid

    # 특수 케이스: ONB(θ) 다이어그램 — 각 점이 곧 ONB
    if fig.is_onb_diagram:
        pairs = sorted(zip(ys_si, xs_si), key=lambda p: p[0])  # sort by ΔT_ONB
        deltas = [p[0] for p in pairs]
        thetas = [p[1] for p in pairs]
        q_si = [fig.q_flux_onb_fixed] * len(deltas)

        rows: list[StandardRow] = []
        for i, (dT, theta) in enumerate(zip(deltas, thetas)):
            notes_parts: list[str] = [f"theta_contact={theta:.1f}deg", "ONB_diagram_point"]
            if not (2.0 <= dT <= 30.0):
                notes_parts.append(f"WARN: delta_T={dT:.2f} out of [2,30] K range")
            rows.append(StandardRow(
                q_flux=fig.q_flux_onb_fixed,
                delta_T_wall=dT,
                delta_T_sub=paper.subcooling_K,
                surface_id=surface_id,
                fluid=fluid,
                source_paper=paper.paper_id,
                figure_ref=fig_ref,
                ONB_flag=True,    # 모든 점이 ONB
                notes="; ".join(notes_parts),
            ))
        return rows, None, list(range(len(rows)))

    # 일반 boiling curve 처리
    if fig.x_kind == "delta_T_wall" and fig.y_kind == "q_flux":
        deltas_unsorted = xs_si
        q_unsorted = ys_si
    elif fig.x_kind == "delta_T_wall" and fig.y_kind == "HTC":
        deltas_unsorted = xs_si
        q_unsorted = [htc * dT for htc, dT in zip(ys_si, xs_si)]
    elif fig.x_kind == "q_flux" and fig.y_kind == "HTC":
        # delta_T = q_flux / HTC
        deltas_unsorted = [q / htc if htc > 0 else 0.0 for q, htc in zip(xs_si, ys_si)]
        q_unsorted = xs_si
    else:
        raise ValueError(f"unsupported axis combo: x={fig.x_kind}, y={fig.y_kind}")

    # delta_T 오름차순 정렬
    pairs = sorted(zip(deltas_unsorted, q_unsorted), key=lambda p: p[0])
    deltas = [p[0] for p in pairs]
    q_si = [p[1] for p in pairs]

    onb_idx, candidates = identify_onb_index(
        deltas, q_si, paper.onb_hint_K.get(series)
    )

    rows: list[StandardRow] = []
    for i, (dT, q) in enumerate(zip(deltas, q_si)):
        notes_parts: list[str] = []
        # 물리 범위 검사
        if not (2.0 <= dT <= 30.0) and surface_id != "EXTERNAL_REF":
            notes_parts.append(f"WARN: delta_T={dT:.2f} out of [2,30] K range")
        if not (1_000.0 <= q <= 5_000_000.0):
            notes_parts.append(f"FLAG: q_flux={q:.0f} out of [1e3, 5e6] W/m2 range")
        # 단조성 검사
        if i > 0 and q < rows[-1].q_flux:
            notes_parts.append(f"FLAG: non-monotonic at idx {i}")
        is_onb = (onb_idx is not None and i == onb_idx)
        if is_onb:
            hint = paper.onb_hint_K.get(series)
            hint_str = f"hint=[{hint[0]:.1f},{hint[1]:.1f}]K" if hint else "slope-jump"
            notes_parts.append(f"ONB_auto ({hint_str})")
        rows.append(StandardRow(
            q_flux=q,
            delta_T_wall=dT,
            delta_T_sub=paper.subcooling_K,
            surface_id=surface_id,
            fluid=fluid,
            source_paper=paper.paper_id,
            figure_ref=fig_ref,
            ONB_flag=is_onb,
            notes="; ".join(notes_parts),
        ))

    return rows, onb_idx, candidates


def write_csv(path: Path, rows: list[StandardRow]) -> None:
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for r in rows:
            w.writerow(r.as_csv_row())


def write_meta_yaml(
    path: Path,
    paper: PaperSpec,
    fig: FigureSpec,
    series: str,
    onb_idx: int | None,
    candidates: list[int],
    n_rows: int,
) -> None:
    surface_id = paper.surface_card_map.get(series, "UNASSIGNED")
    yaml = f"""paper_id: {paper.paper_id}
doi: {paper.doi}
figure: "{fig.figure}"
curve_label: "{series}"
surface_card_id: {surface_id}
fluid: {paper.fluid}
pressure_atm: {paper.pressure_atm}
subcooling_K: {paper.subcooling_K}
onb_index: {onb_idx if onb_idx is not None else 'null'}
onb_candidates: {candidates if candidates else '[]'}
n_rows: {n_rows}
original_units:
  q_flux_or_HTC: "{fig.y_unit_raw}"
  y_kind: "{fig.y_kind}"
  delta_T_wall: "{fig.x_unit_raw}"
digitizer_user: {paper.digitizer_user}
digitized_date: "{paper.digitized_date}"
notes: "{fig.notes}"
"""
    path.write_text(yaml)


# ============================================================================
# CLI
# ============================================================================

def read_existing_onb_index(meta_path: Path) -> int | None | str:
    """meta.yaml에서 onb_index 읽기. 없으면 None, 명시적 null이면 'null' 반환."""
    if not meta_path.is_file():
        return None
    for line in meta_path.read_text().splitlines():
        if line.startswith("onb_index:"):
            v = line.split(":", 1)[1].strip()
            if v == "null":
                return "null"
            try:
                return int(v)
            except ValueError:
                return None
    return None


def process_paper(paper_id: str, preserve_manual: bool = True) -> dict[str, dict]:
    paper = PAPER_REGISTRY.get(paper_id)
    if paper is None:
        raise SystemExit(f"unknown paper_id: {paper_id} (registered: {list(PAPER_REGISTRY)})")

    paper_dir = LIT_ROOT / paper_id
    if not paper_dir.is_dir():
        raise SystemExit(f"missing dir: {paper_dir}")

    summary: dict[str, dict] = {}

    for csv_path in sorted(paper_dir.glob("*_wpd.csv")):
        parsed = parse_wpd_filename(csv_path)
        if parsed is None:
            print(f"  [skip] unparseable filename: {csv_path.name}")
            continue
        _, fig_id, series = parsed
        fig = lookup_figure_spec(paper, fig_id)
        if fig is None:
            print(f"  [skip] no spec for fig{fig_id}: {csv_path.name}")
            continue

        xs, ys = load_wpd_csv(csv_path)
        rows, onb_idx, candidates = make_rows(xs, ys, paper, fig, series)

        # 출력 파일명 — spec.figure가 표준 이름 (예: BETZ raw "fig4a" → output "figure_4_*.csv")
        std_csv = paper_dir / f"figure_{fig.figure}_{series}.csv"
        meta_yaml = paper_dir / f"figure_{fig.figure}_{series}.meta.yaml"

        # 기존 수동 보정 보존
        existing = read_existing_onb_index(meta_yaml) if preserve_manual else None
        manual_override = False
        if existing == "null":
            # 사용자가 명시적으로 ONB를 보류 처리한 경우
            for r in rows:
                r.ONB_flag = False
                r.notes = "; ".join(p for p in r.notes.split("; ") if not p.startswith("ONB_"))
            onb_idx = None
            manual_override = True
        elif isinstance(existing, int) and 0 <= existing < len(rows):
            # 사용자가 수동 idx를 지정한 경우
            for i, r in enumerate(rows):
                was_auto = r.ONB_flag
                r.ONB_flag = (i == existing)
                # ONB_auto 노트 정리, ONB_manual 표기
                parts = [p for p in r.notes.split("; ") if p and not p.startswith("ONB_")]
                if r.ONB_flag:
                    parts.append("ONB_manual (preserved)")
                r.notes = "; ".join(parts)
            onb_idx = existing
            manual_override = True

        write_csv(std_csv, rows)
        write_meta_yaml(meta_yaml, paper, fig, series, onb_idx, candidates, len(rows))

        summary[std_csv.name] = {
            "n_rows": len(rows),
            "onb_idx": onb_idx,
            "manual_preserved": manual_override,
            "delta_T_range": (
                f"{min(r.delta_T_wall for r in rows):.2f}",
                f"{max(r.delta_T_wall for r in rows):.2f}",
            ),
            "q_range": (
                f"{min(r.q_flux for r in rows):.0f}",
                f"{max(r.q_flux for r in rows):.0f}",
            ),
            "warnings": sum(1 for r in rows if "WARN" in r.notes or "FLAG" in r.notes),
        }
        tag = "[manual]" if manual_override else "[auto]  "
        print(f"  [ok] {tag} {csv_path.name} → {std_csv.name} (n={len(rows)}, ONB idx={onb_idx})")

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="WPD CSV → SCHEMA standard CSV converter")
    parser.add_argument("paper_id", help="예: BETZ_2013")
    parser.add_argument(
        "--reset-onb",
        action="store_true",
        help="기존 meta.yaml의 onb_index를 무시하고 자동 식별로 재설정 (수동 보정 덮어씀)",
    )
    args = parser.parse_args()

    print(f"[standardize_wpd] paper={args.paper_id} (preserve_manual={not args.reset_onb})")
    summary = process_paper(args.paper_id, preserve_manual=not args.reset_onb)

    n_files = len(summary)
    n_onb = sum(1 for v in summary.values() if v["onb_idx"] is not None)
    n_manual = sum(1 for v in summary.values() if v.get("manual_preserved"))
    n_warn = sum(v["warnings"] for v in summary.values())
    print()
    print(f"=== summary ===")
    print(f"  files processed: {n_files}")
    print(f"  ONB flagged: {n_onb} ({n_manual} manual preserved + {n_onb - n_manual} auto)")
    print(f"  warning rows total: {n_warn}")


if __name__ == "__main__":
    main()
