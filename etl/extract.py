import pandas as pd
from pathlib import Path

dir = Path(__file__).resolve().parents[1] / "fklubdata"

def extract():
    member = pd.read_csv(dir / "member.csv", sep=";")
    sale = pd.read_csv(dir / "sale.csv", sep=";")
    return {
        "member": member,
        "sale": sale
    }