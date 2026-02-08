# Design Decisions and Tradeoffs

## 1. Time Complexity and Tradeoffs

### Time Complexity

The solution runs in **O(R log R)** time, where R is the number of vote results. The slowest part is counting votes by grouping data.

**What takes time:**
- Reading CSV files: Fast (O(n) - just read each row once)
- Joining data: Fast (O(n) - pandas uses hash joins)
- Counting votes: Slower (O(R log R) - needs to sort/group the data)

### Tradeoffs

1. Pandas **won't work eficiently for extremely large datasets** that don't fit in memory. We can use Ibis for these cases.
2. **Easy to read vs. super fast**: Used pandas functions because they're clear and easy to understand. Could write faster code with loops, but it would be harder to maintain.

2. **Use more memory vs. simpler code**: Load all data into memory at once. Makes the code simpler. Could process in chunks to save memory, but adds complexity.

3. **One pass vs. two passes**: Count both supported and opposed votes in a single operation instead of two separate ones. Cuts the work in half.

4. **Type safety**: Using model classes like `VoteResult.Cols.vote_type` instead of plain strings. Small performance cost but prevents typos and makes code safer.

## 2. Handling Future Columns

### How It Works Now

The code is set up to easily add new columns:

1. **Model classes**: Each data type has a model with a `Cols` class that holds column names (e.g., `Bill.Cols.vote_date`).

2. **Flexible joining**: The `prepare_joined_data()` function can include bill data. When you add columns to `bills.csv`, they automatically show up in the joined data.

3. **Separate functions**: New calculations can be added as new functions that use the joined data.

### Adding New Columns

**Example: Adding "Bill Voted On Date"**

1. Add `vote_date` to the `Bill` model and `Bill.Cols`
2. The join already includes bill data, so the column is available
3. Write a new function that uses `Bill.Cols.vote_date` to calculate what you need
4. Add the result to the output

**Example: Adding "Co-Sponsors"**

1. Add `co_sponsors` to the `Bill` model and `Bill.Cols`
2. Write a function that reads `Bill.Cols.co_sponsors` and counts co-sponsors
3. Add the result to the output

The code structure makes this easy - just update the model write a calculation function, and merge the results.

## 3. Handling List-Based Input Instead of CSVs

### Current Approach

Right now the code processes all data from CSV files.

### What Would Change

To support filtering by specific legislators or bills:

1. **Add a filter parameter**: Let the calculation functions accept an optional list of IDs:
  
   def calculate_legislator_votes(..., legislator_ids: Optional[List[int]] = None):
2. **Filter the data first**: Before calculating, filter to only the requested IDs:thon
if legislator_ids is not None:
    legislators_df = legislators_df[legislators_df['id'].isin(legislator_ids)]
    vote_results_df = vote_results_df[vote_results_df['legislator_id'].isin(legislator_ids)]
3. **Keep everything else the same**: The calculation logic doesn't need to change. Just filter the input data.

### Benefits

- **Works with or without filters**: If no list is provided, process everything (backward compatible)
- **Faster**: Only processes the data you need
- **No code duplication**: Reuses the same calculation functions
- **Simple**: Just add filtering at the start rest stays the same
## 4. Time Spent
3 hours