import pandas as pd

from pathlib import Path
from pydantic import ValidationError, RootModel
from typing import Tuple, Optional

from src.models import Vote, VoteResult, Bill, Person


def load_data(data_dir: str = "data") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load all CSV files from the data directory.

    Returns:
        tuple: Tuple of (legislators_df, bills_df, votes_df, vote_results_df)
    """
    data_path = Path(data_dir)

    legislators_df = pd.read_csv(data_path / "legislators.csv")
    bills_df = pd.read_csv(data_path / "bills.csv")
    votes_df = pd.read_csv(data_path / "votes.csv")
    vote_results_df = pd.read_csv(data_path / "vote_results.csv")

    validate_dataframe(legislators_df, Person, "legislators.csv")
    validate_dataframe(bills_df, Bill, "bills.csv")
    validate_dataframe(votes_df, Vote, "votes.csv")
    validate_dataframe(vote_results_df, VoteResult, "vote_results.csv")

    return legislators_df, bills_df, votes_df, vote_results_df


def validate_dataframe(df: pd.DataFrame, model_class, filename: str):
    """Bulk validate DataFrame rows efficiently."""
    try:
        data_dicts = df.to_dict(orient='records')
        validator = RootModel[list[model_class]]
        validator(data_dicts)

    except ValidationError as e:
        error_summary = e.errors()
        formatted_errors = [
            f"Row {err['loc'][0] + 2} in {filename}: {err['msg']} ({err['loc'][1]})"
            for err in error_summary[:10]  # Limit to first 10
        ]
        raise ValueError(f"Validation errors in {filename}:\n" + "\n".join(formatted_errors))


def prepare_joined_data(
    votes_df: pd.DataFrame,
    vote_results_df: pd.DataFrame,
    bills_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Prepare joined data with vote_results, votes, and optionally bills.

    Args:
        votes_df: DataFrame with columns [id, bill_id]
        vote_results_df: DataFrame with columns [id, legislator_id, vote_id, vote_type]
        bills_df: Optional DataFrame with bill information (for future columns)

    Returns:
        DataFrame with joined vote_results, votes, and optionally bills data
    """
    joined = vote_results_df.merge(
        votes_df[[Vote.Cols.id, Vote.Cols.bill_id]],
        left_on=VoteResult.Cols.vote_id,
        right_on=Vote.Cols.id,
        suffixes=('', '_vote')
    )

    if bills_df is not None:
        bill_columns = [Bill.Cols.id] + [col for col in bills_df.columns if col != Bill.Cols.id]
        joined = joined.merge(
            bills_df[bill_columns],
            left_on=Vote.Cols.bill_id,
            right_on=Bill.Cols.id,
            suffixes=('', '_bill')
        )

    return joined