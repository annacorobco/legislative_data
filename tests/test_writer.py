import pandas as pd
import tempfile

from pathlib import Path

from src.writer import write_legislator_support_oppose_count, write_bill_votes


def test_write_legislator_support_oppose_count():
    """Test writing legislator CSV."""
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Legislator A', 'Legislator B'],
        'num_supported_bills': [5, 3],
        'num_opposed_bills': [2, 4]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        write_legislator_support_oppose_count(df, output_dir=tmpdir)

        output_file = Path(tmpdir) / "legislators-support-oppose-count.csv"
        assert output_file.exists()

        # Verify content
        result = pd.read_csv(output_file)
        assert len(result) == 2
        assert 'num_supported_bills' in result.columns


def test_write_bill_votes():
    """Test writing bills CSV."""
    df = pd.DataFrame({
        'id': [100],
        'title': ['Test Bill'],
        'supporter_count': [10],
        'opposer_count': [5],
        'primary_sponsor': ['John Doe']
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        write_bill_votes(df, output_dir=tmpdir)

        output_file = Path(tmpdir) / "bills.csv"
        assert output_file.exists()

        # Verify content
        result = pd.read_csv(output_file)
        assert len(result) == 1
        assert result['primary_sponsor'].values[0] == 'John Doe'