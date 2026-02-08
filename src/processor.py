import pandas as pd

from src.models import Vote, VoteResult, Person, Bill, BillVoteSummary
from src.data_loader import prepare_joined_data


def calculate_legislator_votes(
    legislators_df: pd.DataFrame,
    votes_df: pd.DataFrame,
    vote_results_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate the number of bills each legislator supported and opposed.

    Args:
        legislators_df: DataFrame with columns [id, name]
        votes_df: DataFrame with columns [id, bill_id]
        vote_results_df: DataFrame with columns [id, legislator_id, vote_id, vote_type]

    Returns:
        pd.DataFrame: DataFrame with columns [id, name, num_supported_bills, num_opposed_bills]
    """
    # Prepare joined data (without bills_df for current calculation)
    vote_results_with_bills = prepare_joined_data(votes_df, vote_results_df)

    # Calculate both supported and opposed counts in one groupby operation
    counts = vote_results_with_bills.groupby([VoteResult.Cols.legislator_id, VoteResult.Cols.vote_type])[
        Vote.Cols.bill_id
    ].nunique().unstack(fill_value=0).reset_index()

    # Rename columns: 1 -> num_supported_bills, 2 -> num_opposed_bills
    counts.columns = [Person.Cols.id, 'num_supported_bills', 'num_opposed_bills']

    # Start with all legislators using model Cols
    result = legislators_df[[Person.Cols.id, Person.Cols.name]].copy()

    # Merge counts (left join, fill NaN with 0)
    result = result.merge(counts, on=Person.Cols.id, how='left')
    result['num_supported_bills'] = result['num_supported_bills'].fillna(0).astype(int)
    result['num_opposed_bills'] = result['num_opposed_bills'].fillna(0).astype(int)

    return result


def calculate_bill_votes(
    bills_df: pd.DataFrame,
    legislators_df: pd.DataFrame,
    votes_df: pd.DataFrame,
    vote_results_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate the number of legislators who supported and opposed each bill.

    Args:
        bills_df: DataFrame with columns [id, title, sponsor_id]
        legislators_df: DataFrame with columns [id, name]
        votes_df: DataFrame with columns [id, bill_id]
        vote_results_df: DataFrame with columns [id, legislator_id, vote_id, vote_type]

    Returns:
        pd.DataFrame: DataFrame with columns [id, title, supporter_count, opposer_count, primary_sponsor]
    """
    # Prepare joined data with bills_df to get bill information
    vote_results_with_bills = prepare_joined_data(votes_df, vote_results_df, bills_df)

    # Calculate both supported and opposed counts in one groupby operation
    counts = vote_results_with_bills.groupby([Vote.Cols.bill_id, VoteResult.Cols.vote_type])[
        VoteResult.Cols.legislator_id
    ].nunique().unstack(fill_value=0).reset_index()

    # Rename columns: 1 -> supporter_count, 2 -> opposer_count
    counts.columns = [Bill.Cols.id, BillVoteSummary.Cols.supporter_count, BillVoteSummary.Cols.opposer_count]

    # Start with all bills
    result = bills_df[[Bill.Cols.id, Bill.Cols.title, Bill.Cols.sponsor_id]].copy()

    # Merge counts (left join, fill NaN with 0)
    result = result.merge(counts, on=Bill.Cols.id, how='left')
    result[BillVoteSummary.Cols.supporter_count] = result[BillVoteSummary.Cols.supporter_count].fillna(0).astype(int)
    result[BillVoteSummary.Cols.opposer_count] = result[BillVoteSummary.Cols.opposer_count].fillna(0).astype(int)

    # Get primary sponsor names by merging with legislators_df
    sponsor_lookup = legislators_df[[Person.Cols.id, Person.Cols.name]].copy()
    sponsor_lookup.columns = [Bill.Cols.sponsor_id, BillVoteSummary.Cols.primary_sponsor]

    result = result.merge(
        sponsor_lookup,
        on=Bill.Cols.sponsor_id,
        how='left'
    )
    result[BillVoteSummary.Cols.primary_sponsor] = result[BillVoteSummary.Cols.primary_sponsor].fillna("Unknown")
    result = result[[
        Bill.Cols.id,
        Bill.Cols.title,
        BillVoteSummary.Cols.supporter_count,
        BillVoteSummary.Cols.opposer_count,
        BillVoteSummary.Cols.primary_sponsor
    ]].copy()

    return result