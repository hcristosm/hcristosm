import os
import requests

USERNAME = "hcristosm"
TOKEN = os.getenv("GITHUB_TOKEN")

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        name
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""

def fetch_languages_data():
    if not TOKEN:
        print("⚠️ GITHUB_TOKEN não encontrado. Gerando dados de demonstração.")
        return {"python": 120000, "jupyter notebook": 30000, "html": 15000, "shell": 5000}, {"python": 3, "jupyter notebook": 1, "html": 1, "shell": 1}

    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {TOKEN}"}
    response = requests.post(url, json={'query': GRAPHQL_QUERY, 'variables': {'username': USERNAME}}, headers=headers)

    bytes_by_lang = {}
    repos_by_lang = {}

    if response.status_code == 200:
        data = response.json()
        repos = data.get('data', {}).get('user', {}).get('repositories', {}).get('nodes', [])
        
        for repo in repos:
            edges = repo.get('languages', {}).get('edges', [])
            repo_langs = set()
            for edge in edges:
                lang_name = edge['node']['name'].lower()
                size = edge['size']
                
                bytes_by_lang[lang_name] = bytes_by_lang.get(lang_name, 0) + size
                repo_langs.add(lang_name)
            
            for lang in repo_langs:
                repos_by_lang[lang] = repos_by_lang.get(lang, 0) + 1

    return bytes_by_lang, repos_by_lang

def generate_langs_svg(bytes_data, repos_data, output_path="langs.svg"):
    # Ordena top 5 por bytes
    sorted_bytes = sorted(bytes_data.items(), key=lambda x: x[1], reverse=True)[:5]
    total_bytes = sum(bytes_data.values()) if bytes_data else 1

    # Ordena top 5 por repositórios
    sorted_repos = sorted(repos_data.items(), key=lambda x: x[1], reverse=True)[:5]
    max_repos = max(repos_data.values()) if repos_data else 1

    width = 620
    row_height = 22
    max_rows = max(len(sorted_bytes), len(sorted_repos))
    height = 45 + max_rows * row_height

    # Margens e Posições recalculadas para acomodar nomes longos sem sobreposição
    col1_label_x = 20
    col1_bar_x = 160        # Empurrado para a direita para dar espaço ao "jupyter notebook"
    col1_bar_max_w = 80
    col1_val_x = 250

    col2_header_x = 310
    col2_label_x = 310
    col2_bar_x = 450        # Empurrado para a direita na segunda coluna
    col2_bar_max_w = 80
    col2_val_x = 540

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .header {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: 11px;
      font-weight: 600;
      fill: #57606a;
      letter-spacing: 1.5px;
    }}
    .label {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: 11px;
      fill: #1f2328;
    }}
    .value {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: 11px;
      fill: #57606a;
    }}
    .bar-bg {{
      fill: #e1e4e8;
      opacity: 0.3;
      rx: 3px;
    }}
    .bar-fill {{
      fill: #8b949e;
      rx: 3px;
    }}
    @media (prefers-color-scheme: dark) {{
      .header {{ fill: #8b949e; }}
      .label {{ fill: #c9d1d9; }}
      .value {{ fill: #8b949e; }}
      .bar-bg {{ fill: #30363d; opacity: 0.5; }}
      .bar-fill {{ fill: #c9d1d9; }}
    }}
  </style>

  <!-- COLUNA 1: BY BYTES -->
  <text x="{col1_label_x}" y="20" class="header">BY BYTES</text>
"""

    # Renderiza linhas da Coluna 1 (BY BYTES)
    for i, (lang, size) in enumerate(sorted_bytes):
        y = 42 + i * row_height
        pct = int(round((size / total_bytes) * 100))
        bar_w = max(4, int((pct / 100) * col1_bar_max_w))

        svg_content += f"""  <text x="{col1_label_x}" y="{y}" class="label">{lang}</text>
  <rect x="{col1_bar_x}" y="{y - 9}" width="{col1_bar_max_w}" height="8" class="bar-bg"/>
  <rect x="{col1_bar_x}" y="{y - 9}" width="{bar_w}" height="8" class="bar-fill"/>
  <text x="{col1_val_x}" y="{y}" class="value">{pct}%</text>
"""

    # Renderiza Coluna 2 (BY REPOS)
    svg_content += f"""\n  <!-- COLUNA 2: BY REPOS -->
  <text x="{col2_header_x}" y="20" class="header">BY REPOS</text>
"""

    for i, (lang, count) in enumerate(sorted_repos):
        y = 42 + i * row_height
        bar_w = max(4, int((count / max_repos) * col2_bar_max_w))

        svg_content += f"""  <text x="{col2_label_x}" y="{y}" class="label">{lang}</text>
  <rect x="{col2_bar_x}" y="{y - 9}" width="{col2_bar_max_w}" height="8" class="bar-bg"/>
  <rect x="{col2_bar_x}" y="{y - 9}" width="{bar_w}" height="8" class="bar-fill"/>
  <text x="{col2_val_x}" y="{y}" class="value">{count}</text>
"""

    svg_content += "</svg>\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"✅ {output_path} gerado com sucesso com espaçamento corrigido!")

if __name__ == "__main__":
    b_data, r_data = fetch_languages_data()
    generate_langs_svg(b_data, r_data)