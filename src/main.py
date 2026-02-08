#!/usr/bin/env python3

from src.data_loader import load_data
from src.processor import calculate_legislator_votes, calculate_bill_votes
from src.writer import write_legislator_support_oppose_count, write_bill_votes


def main():
    """Main function to process legislative data and generate reports."""
    print("Loading data...")
    legislators_df, bills_df, votes_df, vote_results_df = load_data()

    print("Calculating legislator vote counts...")
    legislator_result_df = calculate_legislator_votes(legislators_df, votes_df, vote_results_df)
    print("Writing legislator output...")
    write_legislator_support_oppose_count(legislator_result_df)

    print("Calculating bill vote counts...")
    bill_result_df = calculate_bill_votes(bills_df, legislators_df, votes_df, vote_results_df)
    print("Writing bill output...")
    write_bill_votes(bill_result_df)

    print("Processing is completed!")
    return 0


if __name__ == "__main__":
    exit(main())