import os
import requests

from palette import DARK, LIGHT, rainbow_stripe

USERNAME = "hcristosm"
TOKEN = os.getenv("GITHUB_TOKEN")

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
    }
  }
}
"""

def fetch_github_data():
    if not TOKEN:
        print("⚠️ GITHUB_TOKEN não encontrado. Usando dados locais de fallback.")
        return 0, []
    
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {TOKEN}"}
    response = requests.post(url, json={'query': GRAPHQL_QUERY, 'variables': {'username': USERNAME}}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        user_data = data['data']['user']
        total_contribs = user_data['contributionsCollection']['contributionCalendar']['totalContributions']
        weeks = user_data['contributionsCollection']['contributionCalendar']['weeks']
        return total_contribs, weeks
    else:
        print(f"Erro na API GraphQL: {response.status_code}")
        return 0, []

def generate_stats_svg(total_contribs, weeks, output_path="stats.svg"):
    width = 620
    height = 85

    svg_header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
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

  <text x="20" y="42" class="label">CONTRIBUTIONS IN THE LAST YEAR</text>
  <text x="20" y="68" class="stat-number">{total_contribs:,}</text>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_header)
    print(f"✅ {output_path} gerado com sucesso! Total de contribuições: {total_contribs}")

if __name__ == "__main__":
    total, weeks = fetch_github_data()
    generate_stats_svg(total, weeks)