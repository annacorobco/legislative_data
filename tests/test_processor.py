import pandas as pd
import pytest

from src.processor import calculate_legislator_votes, calculate_bill_votes


def test_calculate_legislator_votes():
    """Test legislator vote calculation."""
    # Sample data
    legislators_df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Legislator A', 'Legislator B']
    })

    votes_df = pd.DataFrame({
        'id': [10, 20],
        'bill_id': [100, 200]
    })

    vote_results_df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'legislator_id': [1, 1, 2, 2],
        'vote_id': [10, 20, 10, 20],
        'vote_type': [1, 2, 1, 1]  # 1=yea, 2=nay
    })

    result = calculate_legislator_votes(legislators_df, votes_df, vote_results_df)

    # Legislator 1: supported bill 100, opposed bill 200
    assert result[result['id'] == 1]['num_supported_bills'].values[0] == 1
    assert result[result['id'] == 1]['num_opposed_bills'].values[0] == 1

    # Legislator 2: supported both bills
    assert result[result['id'] == 2]['num_supported_bills'].values[0] == 2
    assert result[result['id'] == 2]['num_opposed_bills'].values[0] == 0


def test_calculate_legislator_votes_no_votes():
    """Test legislator with no votes."""
    legislators_df = pd.DataFrame({
        'id': [1],
        'name': ['Legislator A']
    })

    votes_df = pd.DataFrame({
        'id': [10],
        'bill_id': [100]
    })

    # Empty vote_results
    vote_results_df = pd.DataFrame({
        'id': [],
        'legislator_id': [],
        'vote_id': [],
        'vote_type': []
    })

    result = calculate_legislator_votes(legislators_df, votes_df, vote_results_df)

    assert result[result['id'] == 1]['num_supported_bills'].values[0] == 0
    assert result[result['id'] == 1]['num_opposed_bills'].values[0] == 0


def test_calculate_bill_votes():
    """Test bill vote calculation."""
    bills_df = pd.DataFrame({
        'id': [100, 200],
        'title': ['Bill A', 'Bill B'],
        'sponsor_id': [1, 2]
    })

    legislators_df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Sponsor A', 'Sponsor B', 'Legislator C']
    })

    votes_df = pd.DataFrame({
        'id': [10, 20],
        'bill_id': [100, 200]
    })

    vote_results_df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'legislator_id': [1, 2, 3, 3],
        'vote_id': [10, 10, 10, 20],
        'vote_type': [1, 1, 2, 1]  # Bill 100: 2 yea, 1 nay. Bill 200: 1 yea
    })

    result = calculate_bill_votes(bills_df, legislators_df, votes_df, vote_results_df)

    # Bill 100: 2 supporters, 1 opposer
    bill_100 = result[result['id'] == 100]
    assert bill_100['supporter_count'].values[0] == 2
    assert bill_100['opposer_count'].values[0] == 1
    assert bill_100['primary_sponsor'].values[0] == 'Sponsor A'

    # Bill 200: 1 supporter, 0 opposers
    bill_200 = result[result['id'] == 200]
    assert bill_200['supporter_count'].values[0] == 1
    assert bill_200['opposer_count'].values[0] == 0


def test_calculate_bill_votes_unknown_sponsor():
    """Test bill with unknown sponsor."""
    bills_df = pd.DataFrame({
        'id': [100],
        'title': ['Bill A'],
        'sponsor_id': [999]  # Non-existent sponsor
    })

    legislators_df = pd.DataFrame({
        'id': [1],
        'name': ['Legislator A']
    })

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

    result = calculate_bill_votes(bills_df, legislators_df, votes_df, vote_results_df)

    assert result['primary_sponsor'].values[0] == "Unknown"
    assert result['supporter_count'].values[0] == 1
    assert result['opposer_count'].values[0] == 0