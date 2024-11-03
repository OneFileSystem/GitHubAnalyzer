import os
import time
import base64
import requests
import pandas as pd
import dotenv
import tensorflow as tf
from transformers import pipeline, BartTokenizer
from rich.console import Console
from rich.table import Table
import io
import sys

dotenv.load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
console = Console()
SUMMARY_MODEL = "facebook/bart-large-cnn"
SUMMARY_REVISION = "main"
API_HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
CACHE = {}
tokenizer = BartTokenizer.from_pretrained(SUMMARY_MODEL)
summarizer = pipeline("summarization", model=SUMMARY_MODEL, tokenizer=tokenizer, revision=SUMMARY_REVISION)

def fetch_github_data(url):
    if url in CACHE:
        return CACHE[url]

    for attempt in range(3):
        response = requests.get(url, headers=API_HEADERS)
        if response.status_code == 200:
            data = response.json()
            CACHE[url] = data
            return data
        elif response.status_code == 403:
            console.print("[bold red]⚠️ Limite de requêtes atteinte. Pause de 60 secondes...[/bold red]")
            time.sleep(60)
        else:
            console.print(f"[red]❌ Erreur {response.status_code} lors de l'accès à {url}. Tentative {attempt + 1}/3[/red]")
            time.sleep(2)
    return None

def get_repo_info(repo_url):
    repo_api_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}"
    return fetch_github_data(repo_api_url)

def get_commit_count(repo_url):
    commits_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/commits"
    data = fetch_github_data(commits_url)
    return len(data) if data else 0

def get_last_commit_date(repo_url):
    commits_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/commits"
    data = fetch_github_data(commits_url)
    return data[0]["commit"]["committer"]["date"] if data else "Pas de commits"

def get_language(repo_url):
    repo_data = get_repo_info(repo_url)
    return repo_data.get("language", "Langage non spécifié")

def get_contributors(repo_url):
    contributors_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/contributors"
    data = fetch_github_data(contributors_url)
    return [contributor["login"] for contributor in data[:5]] if data else []

def get_readme_summary(repo_url):
    readme_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/contents/README.md"
    data = fetch_github_data(readme_url)
    if not data:
        console.print("[yellow]⚠️ README non disponible.[/yellow]")
        return "README non disponible."

    readme_text = base64.b64decode(data["content"]).decode('utf-8')
    try:
        summarized_text = summarizer(
            readme_text,
            max_length=292,
            min_length=100,
            do_sample=False
        )[0]["summary_text"]
        return summarized_text
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la génération du résumé : {e}[/red]")
        return "Résumé indisponible."

def get_open_issues(repo_url):
    repo_data = get_repo_info(repo_url)
    return repo_data.get("open_issues_count", 0)

def get_pull_requests(repo_url):
    pulls_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/pulls?state=open"
    data = fetch_github_data(pulls_url)
    return len(data) if data else 0

def analyze_github_repo(repo_url):
    if not isinstance(repo_url, str) or not repo_url.startswith("https://github.com/"):
        console.print(f"[bold red]❌ URL non valide : {repo_url}[/bold red]")
        return None

    repo_data = get_repo_info(repo_url)
    if not repo_data:
        return "Impossible de récupérer les informations du dépôt."

    report = {
        "repository_name": repo_data.get("name", "Nom indisponible"),
        "owner": repo_data.get("owner", {}).get("login", "Propriétaire inconnu"),
        "description": repo_data.get("description", "Description indisponible"),
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "commit_count": get_commit_count(repo_url),
        "last_commit_date": get_last_commit_date(repo_url),
        "language": get_language(repo_url),
        "open_issues": get_open_issues(repo_url),
        "pull_requests": get_pull_requests(repo_url),
        "top_contributors": ', '.join(get_contributors(repo_url)),
        "readme_summary": get_readme_summary(repo_url),
        "url": repo_url
    }
    return report

def create_tensorflow_model(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

input_shape = (10,)
tensorflow_model = create_tensorflow_model(input_shape)

old_stdout = sys.stdout
sys.stdout = io.StringIO()

tensorflow_model.summary()

sys.stdout = old_stdout

input_file = 'urls.xlsx'
output_csv_file = 'CSV/results.csv'

csv_directory = os.path.dirname(output_csv_file)
os.makedirs(csv_directory, exist_ok=True)

try:
    xls = pd.ExcelFile(input_file)
    df = pd.read_excel(xls, sheet_name='urls')
except Exception as e:
    console.print(f"[bold red]❌ Erreur de chargement du fichier Excel : {e}[/bold red]")
    exit()

if not os.path.exists(output_csv_file):
    pd.DataFrame(columns=["repository_name", "owner", "description", "stars", "forks", "commit_count", "last_commit_date", "language", "open_issues", "pull_requests", "top_contributors", "readme_summary", "url"]).to_csv(output_csv_file, index=False, encoding='utf-8-sig')

total_repositories = len(df)
results_table = Table(title="Rapport d'Analyse des Dépôts GitHub")

results_table.add_column("Nom du dépôt", style="cyan")
results_table.add_column("Propriétaire", style="magenta")
results_table.add_column("Étoiles", justify="right", style="green")
results_table.add_column("Forks", justify="right", style="yellow")
results_table.add_column("Commits", justify="right", style="yellow")
results_table.add_column("Dernier commit", justify="right", style="yellow")
results_table.add_column("Langage", justify="right", style="yellow")
results_table.add_column("Problèmes ouverts", justify="right", style="yellow")
results_table.add_column("Pull requests", justify="right", style="yellow")

for index, row in df.iterrows():
    repo_url = row['url']
    report = analyze_github_repo(repo_url)

    if report:
        pd.DataFrame([report]).to_csv(output_csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
        console.print(f"\n✅ Rapport généré pour le dépôt : [green]{report['repository_name']}[/green]")

        results_table.add_row(
            report['repository_name'],
            report['owner'],
            str(report['stars']),
            str(report['forks']),
            str(report['commit_count']),
            report['last_commit_date'],
            report['language'],
            str(report['open_issues']),
            str(report['pull_requests'])
        )

console.print(results_table)
console.print(f"\n[bold green]Total des dépôts traités : {total_repositories}[/bold green]")
console.print(f"[bold cyan]Rapports sauvegardés dans {output_csv_file}.[/bold cyan]")