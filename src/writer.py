import pandas as pd

from pathlib import Path


def write_legislator_support_oppose_count(
        df: pd.DataFrame,
        output_dir: str = "output",
        filename: str = "legislators-support-oppose-count.csv"
) -> None:
    """
    Write the legislator support/oppose count to a CSV file.

    Args:
        df: DataFrame with columns [id, name, num_supported_bills, num_opposed_bills]
        output_dir: Directory to write the output file
        filename: Name of the output file
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    filepath = output_path / filename
    df.to_csv(filepath, index=False)
    print(f"Output written to: {filepath}")


def write_bill_votes(
    df: pd.DataFrame,
    output_dir: str = "output",
    filename: str = "bills.csv"
) -> None:
    """
    Write the bill vote statistics to a CSV file.

    Args:
        df: DataFrame with columns [id, title, supporter_count, opposer_count, primary_sponsor]
        output_dir: Directory to write the output file
        filename: Name of the output file
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    filepath = output_path / filename
    df.to_csv(filepath, index=False)
    print(f"Output written to: {filepath}")
