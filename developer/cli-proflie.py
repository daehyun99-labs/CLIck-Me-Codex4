import json
from pathlib import Path
import logging
import click
from rich.console import Console
from rich.table import Table
from pyfiglet import figlet_format

# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 콘솔 객체 생성
console = Console()


def load_data(json_path: Path) -> dict:
    """JSON 파일에서 개발자 정보를 불러온다."""
    try:
        with json_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug("데이터 로드 성공: %s", data)
            return data
    except Exception as exc:  # 모든 예외 포착 후 로깅
        logger.exception("데이터 로드 중 오류 발생")
        raise exc


@click.command()
def main() -> None:
    """CLI에서 개발자 프로필을 출력한다."""
    data_path = Path(__file__).parent / "data.json"
    data = load_data(data_path)

    name: str = data.get("name", "")
    intro: str = data.get("intro", "")
    skills: list[str] = data.get("skills", [])

    # 이름의 첫 글자들로 이니셜 생성
    initials = "".join(word[0].upper() for word in name.split())

    # pyfiglet을 이용한 이니셜 출력
    console.print(figlet_format(initials, font="standard"))

    # 자기소개 출력
    console.print(f"[bold green]{intro}[/bold green]")

    # 기술 스택 테이블 생성 및 출력
    table = Table(title="기술 스택")
    table.add_column("번호", justify="right")
    table.add_column("기술명", style="cyan")
    for idx, skill in enumerate(skills, start=1):
        table.add_row(str(idx), skill)

    console.print(table)


if __name__ == "__main__":
    main()
