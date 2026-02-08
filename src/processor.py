import pandas as pd

from src.models import Vote, VoteResult, Person, Bill, BillVoteSummary
from src.data_loader import prepare_joined_data

VOTE_TYPE_YEA = 1
VOTE_TYPE_NAY = 2


def _ensure_vote_type_columns(counts_df: pd.DataFrame) -> pd.DataFrame:
    """Ensure both vote_type columns (1 and 2) exist in the counts DataFrame."""
    if VOTE_TYPE_YEA not in counts_df.columns:
        counts_df[VOTE_TYPE_YEA] = 0
    if VOTE_TYPE_NAY not in counts_df.columns:
        counts_df[VOTE_TYPE_NAY] = 0
    return counts_df


def _merge_and_fill_counts(
        result_df: pd.DataFrame,
        counts_df: pd.DataFrame,
        id_column: str,
        count_columns: list[str]
) -> pd.DataFrame:
    """Merge counts and fill NaN values with 0."""
    result = result_df.merge(counts_df, on=id_column, how='left')
    for col in count_columns:
        result[col] = result[col].fillna(0).astype(int)
    return result


def calculate_legislator_votes(
        legislators_df: pd.DataFrame,
        votes_df: pd.DataFrame,
        vote_results_df: pd.DataFrame
) -> pd.DataFrame:
    """Calculate the number of bills each legislator supported and opposed."""
    vote_results_with_bills = prepare_joined_data(votes_df, vote_results_df)

    counts = vote_results_with_bills.groupby([VoteResult.Cols.legislator_id, VoteResult.Cols.vote_type])[
        Vote.Cols.bill_id
    ].nunique().unstack(fill_value=0).reset_index()

    counts = _ensure_vote_type_columns(counts)
    counts.columns = [Person.Cols.id, 'num_supported_bills', 'num_opposed_bills']

    result = legislators_df[[Person.Cols.id, Person.Cols.name]].copy()
    result = _merge_and_fill_counts(
        result,
        counts,
        Person.Cols.id,
        ['num_supported_bills', 'num_opposed_bills']
    )

    return result


def calculate_bill_votes(
        bills_df: pd.DataFrame,
        legislators_df: pd.DataFrame,
        votes_df: pd.DataFrame,
        vote_results_df: pd.DataFrame
) -> pd.DataFrame:
    """Calculate the number of legislators who supported and opposed each bill."""
    vote_results_with_bills = prepare_joined_data(votes_df, vote_results_df, bills_df)

    counts = vote_results_with_bills.groupby([Vote.Cols.bill_id, VoteResult.Cols.vote_type])[
        VoteResult.Cols.legislator_id
    ].nunique().unstack(fill_value=0).reset_index()

    counts = _ensure_vote_type_columns(counts)
    counts.columns = [Bill.Cols.id, BillVoteSummary.Cols.supporter_count, BillVoteSummary.Cols.opposer_count]

    result = bills_df[[Bill.Cols.id, Bill.Cols.title, Bill.Cols.sponsor_id]].copy()
    result = _merge_and_fill_counts(
        result,
        counts,
        Bill.Cols.id,
        [BillVoteSummary.Cols.supporter_count, BillVoteSummary.Cols.opposer_count]
    )

    # Get primary sponsor names
    sponsor_lookup = legislators_df[[Person.Cols.id, Person.Cols.name]].copy()
    sponsor_lookup.columns = [Bill.Cols.sponsor_id, BillVoteSummary.Cols.primary_sponsor]

    result = result.merge(sponsor_lookup, on=Bill.Cols.sponsor_id, how='left')
    result[BillVoteSummary.Cols.primary_sponsor] = result[BillVoteSummary.Cols.primary_sponsor].fillna("Unknown")

    result = result[[
        Bill.Cols.id,
        Bill.Cols.title,
        BillVoteSummary.Cols.supporter_count,
        BillVoteSummary.Cols.opposer_count,
        BillVoteSummary.Cols.primary_sponsor
    ]].copy()

    return result