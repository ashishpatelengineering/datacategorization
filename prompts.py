# prompts.py
CATEGORY_SUGGESTION_PROMPT = """
Analyze the complete CSV dataset below.
Infer broad, meaningful, high-level semantic categories suitable for
classifying each row.

OUTPUT RULES:
1. Output exactly 6 lines.
2. The first 5 lines must be category names.
3. The 6th line must be exactly: Unknown
4. One category per line. No commas, bullets, or numbering.
5. No explanations or comments.
6. No repeated categories.
7. No markdown or formatting.
8. No quotes.
9. Categories must be broad and general.
10. Categories must reflect patterns in the CSV.
11. Return only the 6 category lines.

CSV DATA:
{csv_text}
"""

CATEGORY_ASSIGNMENT_PROMPT = """
Analyze this CSV and add a new column called 'Category' as the last column.

OUTPUT RULES:
1. Add a new column called 'Category' as the last column.
2. Assign only one of the following categories to each row: {categories}.
3. Do NOT invent any new categories.
4. If a row does not fit any category, use 'Unknown'.
5. Return only the CSV text with the new column.
6. No markdown, explanations, or extra text.
7. Do not modify existing columns or their values.

CSV DATA:
{csv_text}
"""
