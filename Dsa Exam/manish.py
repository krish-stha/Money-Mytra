# # import pandas as pd

# # # Prepare data
# # data = [
# #     {"SN": 1, "Title": "IELTS Overview", "Time": "67:20", "Remarks": ""},
# #     {"SN": 2, "Title": "Paraphrasing (Foundational Skill)", "Time": "61:01", "Remarks": ""},
# #     {"SN": 3, "Title": "Listening: Forms | Notes & Table | Flowchart Completion", "Time": "45:58", "Remarks": ""},
# #     {"SN": 4, "Title": "Listening: Multiple Choices", "Time": "31:48", "Remarks": ""},
# #     {"SN": 5, "Title": "Listening: Labelling Maps", "Time": "34:43", "Remarks": ""},
# #     {"SN": 6, "Title": "Listening: Short Answers", "Time": "07:06", "Remarks": ""},
# #     {"SN": 7, "Title": "Listening: Matching Names", "Time": "", "Remarks": "Not Found"},
# #     {"SN": 8, "Title": "Reading: Skimming | Scanning | Careful Reading", "Time": "", "Remarks": "Not Found"},
# #     {"SN": 9, "Title": "Reading: Forms Notes, Table & Summary Completion", "Time": "53:58", "Remarks": ""},
# #     {"SN": 10, "Title": "Reading: Multiple Choices", "Time": "21:54", "Remarks": ""},
# #     {"SN": 11, "Title": "Reading: True | False | Not Given & Yes | No | Not Given", "Time": "27:14", "Remarks": ""},
# #     {"SN": 12, "Title": "Reading: Labelling Diagram | Short Answers & Matching Sentence Endings", "Time": "39:26", "Remarks": ""},
# #     {"SN": 13, "Title": "Reading: Matching Names", "Time": "13:33", "Remarks": ""},
# #     {"SN": 14, "Title": "Reading: Matching Headings", "Time": "31:49", "Remarks": ""},
# #     {"SN": 15, "Title": "Reading: Matching Information", "Time": "25:16", "Remarks": ""},
# #     {"SN": 16, "Title": "Writing: Task 1 Band Descriptors", "Time": "81:50", "Remarks": ""},
# #     {"SN": 17, "Title": "Writing: Academic Task 1 Introduction & Overview", "Time": "32:56", "Remarks": ""},
# #     {"SN": 18, "Title": "Writing: Academic Task 1 Details Paragraphs", "Time": "23:10", "Remarks": ""},
# #     {"SN": 19, "Title": "Writing: General Training Task 1 (All in One)", "Time": "39:57", "Remarks": ""},
# #     {"SN": 20, "Title": "Writing: Task 2 Band Descriptors", "Time": "19:50", "Remarks": ""},
# #     {"SN": 21, "Title": "Writing: Task 2 Introduction", "Time": "31:41", "Remarks": ""},
# #     {"SN": 22, "Title": "Writing: Task 2 Main Body Paragraphs", "Time": "29:58", "Remarks": ""},
# #     {"SN": 23, "Title": "Writing: Task 2 Conclusion", "Time": "", "Remarks": "Not Found"},
# #     {"SN": 24, "Title": "Speaking: Band Descriptors", "Time": "72:90", "Remarks": ""},
# #     {"SN": 25, "Title": "Speaking: Part 1", "Time": "52:37", "Remarks": ""},
# #     {"SN": 26, "Title": "Speaking: Part 2", "Time": "20:54", "Remarks": ""},
# #     {"SN": 27, "Title": "Speaking: Part 3", "Time": "", "Remarks": "Not Found"}
# # ]

# # # Create DataFrame
# # df = pd.DataFrame(data)

# # # Function to convert "MM:SS" or "HH:MM" string into total minutes as float
# # def convert_to_minutes(time_str):
# #     if not time_str:
# #         return None
# #     try:
# #         parts = time_str.split(':')
# #         if len(parts) == 2:
# #             minutes = int(parts[0])
# #             seconds = int(parts[1])
# #             return round(minutes + seconds / 60, 2)
# #         else:
# #             return None
# #     except:
# #         return None

# # # Apply conversion
# # df['Duration (mins)'] = df['Time'].apply(convert_to_minutes)

# # # Save to Excel
# # output_path = r"C:\Users\97798\OneDrive\Documents\ielts_launch_schedule.xlsx"  # ✅ Correct


# # df.to_excel(output_path, index=False)

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns




# import pandas as pd

# # Step 1: Load the Excel file
# df = pd.read_excel("C:\\Users\\97798\\OneDrive\\Documents\\Ambition Guru Sales Reporting\\retentionOfBaisakhLoksewa.xlsx", sheet_name="Result 1")


# # Step 2: Function to clean and split packages by comma
# def split_packages(packages):
#     if pd.isna(packages):
#         return set()
#     return set(p.strip() for p in str(packages).split(','))

# # Step 3: Apply the function to previous and current packages
# df['previous_set'] = df['Previous_packages'].apply(split_packages)
# df['current_set'] = df['primary_packages'].apply(split_packages)

# # Step 4: Check if there's any common package (same)
# df['same_package'] = df.apply(lambda row: not row['previous_set'].isdisjoint(row['current_set']), axis=1)

# # Step 5: Count same vs different
# same_count = df['same_package'].sum()
# different_count = len(df) - same_count


# # Step 6: Calculate ratios
# total = same_count + different_count
# same_ratio = same_count / total
# different_ratio = different_count / total
# print(df.columns)


# # Step 7: Print results
# print("Same Package Count:", same_count)
# print("Different Package Count:", different_count)
# print("Same Package Ratio:", round(same_ratio * 100, 2), "%")
# print("Different Package Ratio:", round(different_ratio * 100, 2), "%")


# # Visualization starts here

# # Data for plotting
# counts = [same_count, different_count]
# ratios = [same_ratio * 100, different_ratio * 100]
# labels = ['Same Package', 'Different Package']

# # Bar chart of counts
# # plt.figure(figsize=(8,5))
# # sns.barplot(x=labels, y=counts, palette='pastel')
# # plt.title('Count of Same vs Different Packages')
# # plt.ylabel('Count')
# # plt.xlabel('Package Comparison')
# # for i, count in enumerate(counts):
# #     plt.text(i, count + total*0.01, str(count), ha='center', fontsize=12)
# # plt.show()

# # Pie chart of ratios
# plt.figure(figsize=(7,7))
# colors = sns.color_palette('pastel')[0:2]
# plt.pie(ratios, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': 14})
# plt.title('Ratio of Same vs Different Packages')
# plt.show()

# https://admin.ambition.guru/students/155882/course-enrolled

# # Filter rows where same_package is True
# same_package_customers = df[df['same_package']]

# # Extract the Customer IDs
# customer_ids_with_same_package = same_package_customers['customer_id'].tolist()

# print("Customer IDs with same packages:")
# print(customer_ids_with_same_package)


# Define the relevant keywords
relevant_keywords = ["Loksewa", "Sikshak Sewa", "Physical Loksewa"]

# Filter rows based on presence of keywords in any of the product category columns
filtered_df = df[
    df["Product category"].fillna("").str.contains('|'.join(relevant_keywords), case=False) |
    df["Product category 1"].fillna("").str.contains('|'.join(relevant_keywords), case=False) |
    df["Product category 2"].fillna("").str.contains('|'.join(relevant_keywords), case=False)
]

# Rename date column for convenience
filtered_df = filtered_df.rename(columns={"date(cc.created_at)": "Date"})

# Create a new column to classify the calls
def classify_call(row):
    if row["Department"] == "Sales" and row["Call Type"] == "Incoming":
        return "Sales Incoming"
    elif row["Department"] == "Sales" and row["Call Type"] == "Outgoing":
        return "Sales Outgoing"
    elif row["Department"] == "Support" and row["Call Type"] == "Incoming":
        return "Support Incoming"
    elif row["Department"] == "Support" and row["Call Type"] == "Outgoing":
        return "Support Outgoing"
    else:
        return "Other"

filtered_df["Call Category"] = filtered_df.apply(classify_call, axis=1)

# Group by date and call category, then count
summary = filtered_df.groupby(["Date", "Call Category"]).size().unstack(fill_value=0).reset_index()

# Define output path
output_path = "/mnt/data/Ambition_Guru_Sales_Call_Summary.xlsx"

# Save to Excel
summary.to_excel(output_path, index=False)

output_path
