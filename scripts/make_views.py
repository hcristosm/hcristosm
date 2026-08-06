"""Gera views.svg: contador cumulativo de visitas à página do repositório
no GitHub, no mesmo estilo cassete-vintage do stats.svg.

A API de tráfego do GitHub (`/traffic/views`) só expõe os últimos 14 dias
por dia. Para manter um total acumulado sem depender de terceiros, os
valores diários são mesclados num estado local (views_state.json, versão
por dia) — dias já vistos são sobrescritos com o valor mais recente da API
(ainda dentro da janela de 14 dias), e dias que já saíram da janela ficam
congelados no total.
"""

import json
import os

import requests

from palette import DARK, LIGHT, rainbow_stripe

USERNAME = "hcristosm"
REPO = "hcristosm"
TOKEN = os.getenv("GITHUB_TOKEN")
STATE_PATH = "views_state.json"


def fetch_daily_views():
    if not TOKEN:
        print("⚠️ GITHUB_TOKEN não encontrado. Pulando atualização de views.")
        return None

    url = f"https://api.github.com/repos/{USERNAME}/{REPO}/traffic/views"
    headers = {"Authorization": f"bearer {TOKEN}", "Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro na API de tráfego: {response.status_code}")
        return None

    data = response.json()
    return {day["timestamp"][:10]: day["count"] for day in data.get("views", [])}


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def generate_views_svg(total_views, output_path="views.svg"):
    width = 620
    height = 85

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .panel {{ fill: {LIGHT['panel_bg']}; }}
    .frame {{ fill: none; stroke: {LIGHT['panel_border']}; stroke-width: 1.5; }}
    .label {{
      font-family: 'JetBrains Mono', 'Courier New', monospace;
      font-size: 11px;
      letter-spacing: 1px;
      fill: {LIGHT['text_secondary']};
    }}
    .stat-number {{
      font-family: 'JetBrains Mono', 'Courier New', monospace;
      font-size: 20px;
      font-weight: bold;
      fill: {LIGHT['accent']};
    }}
    @media (prefers-color-scheme: dark) {{
      .panel {{ fill: {DARK['panel_bg']}; }}
      .frame {{ stroke: {DARK['panel_border']}; }}
      .label {{ fill: {DARK['text_secondary']}; }}
      .stat-number {{ fill: {DARK['accent']}; }}
    }}
  </style>
  <rect class="panel" x="0" y="0" width="{width}" height="{height}" rx="10"/>
{rainbow_stripe(20, 4, width - 40, 3)}
  <rect class="frame" x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="9.5"/>

  <text x="20" y="42" class="label">PROFILE VIEWS</text>
  <text x="20" y="68" class="stat-number">{total_views:,}</text>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ {output_path} gerado com sucesso! Total de views: {total_views}")


if __name__ == "__main__":
    state = load_state()
    daily = fetch_daily_views()
    if daily is not None:
        state.update(daily)
        save_state(state)
    generate_views_svg(sum(state.values()))
