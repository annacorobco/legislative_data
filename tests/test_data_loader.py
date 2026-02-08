import pandas as pd
import pytest

from src.data_loader import prepare_joined_data
from src.models import Vote, VoteResult


def test_prepare_joined_data():
    """Test data joining."""
    votes_df = pd.DataFrame({
        'id': [10, 20],
        'bill_id': [100, 200]
    })

    vote_results_df = pd.DataFrame({
        'id': [1, 2],
        'legislator_id': [1, 2],
        'vote_id': [10, 20],
        'vote_type': [1, 2]
    })

    joined = prepare_joined_data(votes_df, vote_results_df)

    # Check that bill_id is added from votes
    assert Vote.Cols.bill_id in joined.columns
    assert len(joined) == 2
    assert joined[joined[VoteResult.Cols.vote_id] == 10][Vote.Cols.bill_id].values[0] == 100


def test_prepare_joined_data_with_bills():
    """Test data joining with bills."""
    votes_df = pd.DataFrame({
        'id': [10],
        'bill_id': [100]
    })

    vote_results_df = pd.DataFrame({
        'id': [1],
        'legislator_id': [1],
        'vote_id': [10],
        'vote_type': [1]
    })

    bills_df = pd.DataFrame({
        'id': [100],
        'title': ['Test Bill'],
        'sponsor_id': [1]
    })

    joined = prepare_joined_data(votes_df, vote_results_df, bills_df)

    # Check that bill columns are added
    assert 'title' in joined.columns
    assert 'sponsor_id' in joined.columns