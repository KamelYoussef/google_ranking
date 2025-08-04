import pandas as pd
import os
from glob import glob
from datetime import datetime

# Set your folder path here
folder_path = './'  # Change this to your folder path if needed
files = glob(os.path.join(folder_path, 'broker_ranks_*.xlsx'))

# Organize files by month (yyyymm)
files_by_month = {}
for file in files:
    date_str = os.path.basename(file).split('_')[-1].replace('.xlsx', '')
    month = date_str[:6]
    if month not in files_by_month:
        files_by_month[month] = []
    files_by_month[month].append((file, date_str))

# Process each month
for month, file_info in files_by_month.items():
    # Sort by date to find the latest file for rating/reviews
    file_info.sort(key=lambda x: x[1])
    latest_file = file_info[-1][0]

    # Collect Rank data
    dfs = []
    for i, (file, _) in enumerate(file_info):
        df = pd.read_excel(file)
        df = df[['City', 'Keyword', 'Rank']].copy()
        df.rename(columns={'Rank': f'Rank_{i+1}'}, inplace=True)
        dfs.append(df)

    # Merge rank columns
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=['City', 'Keyword'], how='outer')

    # Load rating/review from the latest file
    last_df = pd.read_excel(latest_file)
    last_df = last_df[['City', 'Keyword', 'Rating', 'Reviews']]

    # Merge ratings and reviews
    final_df = pd.merge(merged_df, last_df, on=['City', 'Keyword'], how='left')

    # Compute average rank
    rank_cols = [col for col in final_df.columns if col.startswith('Rank_')]
    final_df['Avg Rank'] = final_df[rank_cols].mean(axis=1, skipna=True)

    # Reorder columns
    cols = ['City', 'Keyword'] + ['Avg Rank', 'Rating', 'Reviews']
    final_df = final_df[cols]
    final_df = final_df.fillna('None')
    # Save the output
    output_file = f'combined_ranks_{month}.xlsx'
    final_df.to_excel(output_file, index=False)
    print(f'Saved: {output_file}')
