"""Atualiza o período do curso no README.

Referência: 2º semestre de 2026 = 8º período. Os semestres viram em
1º de fevereiro e 1º de agosto, e o período para de subir no 10º.
"""
import datetime
import pathlib
import re

BASE_YEAR, BASE_HALF, BASE_PERIOD = 2026, 2, 8
MAX_PERIOD = 10

# "8º período" em texto e URL-encoded (%20 ou + como espaço)
PATTERN = re.compile(r"\d+(?=º período|%C2%BA(?:%20|\+)per%C3%ADodo)")


def current_period(today: datetime.date) -> int:
    if today.month >= 8:
        year, half = today.year, 2
    elif today.month >= 2:
        year, half = today.year, 1
    else:  # janeiro ainda é férias do 2º semestre do ano anterior
        year, half = today.year - 1, 2
    elapsed = (year - BASE_YEAR) * 2 + (half - BASE_HALF)
    return max(BASE_PERIOD, min(MAX_PERIOD, BASE_PERIOD + elapsed))


def main() -> None:
    readme = pathlib.Path(__file__).resolve().parent.parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    period = current_period(datetime.date.today())
    updated = PATTERN.sub(str(period), text)
    if updated != text:
        readme.write_text(updated, encoding="utf-8")
    print(f"Período atual: {period}º")


if __name__ == "__main__":
    main()
