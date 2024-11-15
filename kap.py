import click
import os
import json
import subprocess

# TODO: kapack init -> api(android.d.ts, api2.d.ts 등), kakao_modules, kapack.json 생성

# `kapack.json`의 기본 템플릿
DEFAULT_KAPACK_JSON = {
    "name": "your_project",
    "version": "1.0.0",
    "dependencies": []
}

# `kapack.json` 파일 경로
KAPACK_FILE = "kapack.json"
KAKAO_MODULES_DIR = "kakao_modules"

def load_kapack_file():
    """Load kapack.json file. If it doesn't exist, create a new one."""
    if not os.path.exists(KAPACK_FILE):
        click.echo(f'{KAPACK_FILE} not found. Creating a new one...')
        with open(KAPACK_FILE, 'w') as f:
            json.dump(DEFAULT_KAPACK_JSON, f, indent=4)
    with open(KAPACK_FILE, 'r') as f:
        return json.load(f)

def save_kapack_file(data):
    """Save the given data to kapack.json."""
    with open(KAPACK_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def clone_repository(repo_url):
    """Clone a GitHub repository into the kakao_modules directory."""
    # kakao_modules 폴더가 없으면 생성
    if not os.path.exists(KAKAO_MODULES_DIR):
        os.makedirs(KAKAO_MODULES_DIR)
    
    # 레포지토리 이름 추출 (예: https://github.com/user/repo -> repo)
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')

    # 해당 경로에 이미 레포지토리가 클론되어 있는지 확인
    target_dir = os.path.join(KAKAO_MODULES_DIR, repo_name)
    if os.path.exists(target_dir):
        click.echo(f'Repository {repo_name} is already cloned.')
        return
    
    # Git 명령어를 사용해 클론 실행
    click.echo(f'Cloning {repo_url} into {KAKAO_MODULES_DIR}...')
    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    click.echo(f'Successfully cloned {repo_name}.')

# CLI의 기본 그룹 (kap 명령어의 루트)
@click.group()
def cli():
    """KaPack - A simple package manager for KakaoTalk bot modules."""
    pass

# 패키지 설치 명령어
@cli.command()
@click.argument('repo_url')
def install(repo_url):
    """Install a package from a GitHub repository."""
    click.echo(f'Installing package from {repo_url}...')
    
    # kapack.json 파일을 불러오고 없으면 생성
    kapack_data = load_kapack_file()
    
    # 이미 dependencies에 추가된 패키지인지 확인
    if repo_url in kapack_data["dependencies"]:
        click.echo(f'{repo_url} is already installed.')
    else:
        # 새로운 패키지를 dependencies에 추가
        kapack_data["dependencies"].append(repo_url)
        save_kapack_file(kapack_data)
        click.echo(f'{repo_url} added to kapack.json.')
        
        # GitHub 레포지토리 클론
        clone_repository(repo_url)

@cli.command('i')
@click.argument('repo_url')
def install_alias(repo_url):
    """Alias for 'install'."""
    install(repo_url)

# 패키지 삭제 명령어
@cli.command()
@click.argument('repo_url')
def uninstall(repo_url):
    """Remove a package."""
    click.echo(f'Removing package: {repo_url}...')
    
    # kapack.json 파일을 불러옴
    kapack_data = load_kapack_file()
    
    # 패키지가 설치되어 있는지 확인
    if repo_url in kapack_data["dependencies"]:
        kapack_data["dependencies"].remove(repo_url)
        save_kapack_file(kapack_data)
        click.echo(f'{repo_url} removed from kapack.json.')
        
        # 로컬에서 레포지토리 폴더 삭제
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        target_dir = os.path.join(KAKAO_MODULES_DIR, repo_name)
        if os.path.exists(target_dir):
            click.echo(f'Removing cloned repository: {target_dir}')
            subprocess.run(["rm", "-rf", target_dir], check=True)
        else:
            click.echo(f'No cloned repository found for {repo_url}.')
    else:
        click.echo(f'{repo_url} is not installed.')

@cli.command('ui', short_help='Uninstall a package')
@click.argument('repo_url')
def uninstall_alias(repo_url):
    """Alias for 'uninstall'."""
    uninstall(repo_url)

# 패키지 검색 명령어
@cli.command()
@click.argument('query')
def search(query):
    """Search for a package."""
    click.echo(f'Searching for package: {query}')
    # 검색 로직이 들어갈 수 있습니다.

# 패키지 업데이트 명령어
@cli.command()
@click.argument('repo_url')
def update(repo_url):
    """Update a package."""
    click.echo(f'Updating package: {repo_url}')
    # 패키지 업데이트 로직이 들어갈 수 있습니다.

if __name__ == '__main__':
    cli()
