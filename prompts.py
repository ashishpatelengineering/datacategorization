# prompts.py
CATEGORY_SUGGESTION_PROMPT = """
Analyze the complete CSV dataset below.
Infer broad, meaningful, high-level semantic categories suitable for
classifying each row.

OUTPUT RULES:
1. Output exactly 6 lines.
2. Lines 1 to 5 must be category names.
3. Each category name must be a single word.
4. Categories must be broad, high-level, and directly supported by patterns in the CSV.
5. Categories must avoid overly specific or narrow terminology.
6. Do not repeat any category.
7. Line 6 must be exactly: Unknown
8. Output one category per line with no commas, bullets, numbering, quotes, or formatting.
9. Provide no explanations or commentary.
10. Output only the 6 category lines.

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
