import os
import requests
from datetime import datetime

from palette import DARK, LIGHT, rainbow_stripe

USERNAME = "hcristosm"
TOKEN = os.getenv("GITHUB_TOKEN")

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

def fetch_github_data():
    if not TOKEN:
        print("⚠️ GITHUB_TOKEN não encontrado. Gerando com dados padrão.")
        return []
    
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {TOKEN}"}
    response = requests.post(url, json={'query': GRAPHQL_QUERY, 'variables': {'username': USERNAME}}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        days = []
        for week in weeks:
            for day in week['contributionDays']:
                days.append(day)
        return days
    else:
        print(f"Erro na API GraphQL: {response.status_code}")
        return []

def calculate_streaks(days):
    if not days:
        return 0, 0

    # Ordena os dias cronologicamente
    days.sort(key=lambda x: x['date'])
    
    longest_streak = 0
    temp_streak = 0
    
    # Cálculo da Longest Streak
    for d in days:
        if d['contributionCount'] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Cálculo da Current Streak (do dia mais recente para trás)
    reversed_days = list(reversed(days))
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    
    current_streak = 0
    idx = 0
    
    # Se hoje ainda não teve commit, começa a contar a partir de ontem sem zerar a streak
    if reversed_days and reversed_days[0]['date'] == today_str and reversed_days[0]['contributionCount'] == 0:
        idx = 1

    for d in reversed_days[idx:]:
        if d['contributionCount'] > 0:
            current_streak += 1
        else:
            break

    return current_streak, longest_streak

def generate_streak_svg(current_streak, longest_streak, output_path="streak.svg"):
    width = 620
    height = 85

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .panel {{ fill: {LIGHT['panel_bg']}; }}
    .frame {{ fill: none; stroke: {LIGHT['panel_border']}; stroke-width: 1.5; }}
    .divider {{ stroke: {LIGHT['panel_border']}; stroke-width: 1; }}
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
      .divider {{ stroke: {DARK['panel_border']}; }}
      .label {{ fill: {DARK['text_secondary']}; }}
      .stat-number {{ fill: {DARK['accent']}; }}
    }}
  </style>
  <rect class="panel" x="0" y="0" width="{width}" height="{height}" rx="10"/>
{rainbow_stripe(20, 4, width - 40, 3)}
  <rect class="frame" x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="9.5"/>
  <line x1="300" y1="24" x2="300" y2="{height - 20}" class="divider" opacity="0.5"/>

  <text x="20" y="42" class="label">CURRENT STREAK</text>
  <text x="20" y="68" class="stat-number">{current_streak} days</text>

  <text x="320" y="42" class="label">LONGEST STREAK</text>
  <text x="320" y="68" class="stat-number">{longest_streak} days</text>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✅ {output_path} gerado com sucesso! (Current: {current_streak}d, Longest: {longest_streak}d)")

if __name__ == "__main__":
    days_data = fetch_github_data()
    curr, long_s = calculate_streaks(days_data)
    generate_streak_svg(curr, long_s)