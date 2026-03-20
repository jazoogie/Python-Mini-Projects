# By Jesse M, 30/5/2024
# Last modified: 02/03/2026

# This program helps print large documents on a printer that only supports
# one-sided printing

import subprocess
import time
import math

# Average time derived from printing pages '3,5,7,9,11,13,15,17,19,21,23,25' 
# from 2022 Methods Exam 2 - 3m:15s, 12 pages -> ~16.25s per page.
# maybe a low-ball estimate; a lot of pages were quite empty.
PAGE_DURATION = 195 / 12

# Max number of sheets per group - to allowing for easy stapling
MAX_PER_STAPLE = 8

# Ask the user for a page range
def get_page_range():
    while True:
        inp = input(" > ")
        
        # Try to parse the user's input for a start and end page
        try:
            start_page_str, end_page_str = inp.replace(" ", "").split("-")

            return int(start_page_str), int(end_page_str)
        except: pass

        # Otherwise, warn the user of an input error
        print("Error: page range could not be parsed. Try again.")
        print()

def display_group_info(group_start, group_end):
    # Calculate the number of pages in the group
    pages = group_end - group_start + 1
    # Calculate estimated printing time
    print_time = time.strftime("%-Mm %Ss", time.gmtime(PAGE_DURATION * pages))
    # Calculate the number of paper sheets required to print the group
    sheets = math.ceil(pages / 2)

    print(f"Processing pages {group_start}-{group_end} ({pages} pages)")
    print(f"Estimated print time: {print_time}")
    print(f"Sheets of paper required: {sheets}")

def print_group(group_start, group_end):

    display_group_info(group_start, group_end)
    print()

    start_parity = group_start % 2

    odd_pages = []
    even_pages = []
    for page in range(group_start, group_end + 1):
        # If our start was an even number, e.g. 4, then this logic will consider
        # subsequent even pages as 'odd' - and vice-versa for if start was odd.
        if (page + start_parity) % 2:
            even_pages.append(str(page))
        else:
            odd_pages.append(str(page))

    odd_pages_str = str.join(",", odd_pages)
    even_pages_str = str.join(",", even_pages)

    # 'Odd' pages
    subprocess.run("pbcopy", text=True, input=odd_pages_str)
    print("Print the 'odd' pages - copied to clipboard:")
    input(odd_pages_str)
    print()

    # If there are an odd number of pages being printed, set aside the bottom page
    pages_in_group = group_end - group_start + 1
    if pages_in_group % 2:
        input("Set aside the page on the bottom (the first page that was printed).")
        print()

    input("Preserve the order, put the pages in upside down with the blank side facing you.")
    print()

    # 'Even' pages
    subprocess.run("pbcopy", text=True, input=even_pages_str)
    print("Print the 'even' pages - copied to clipboard:")
    input(even_pages_str)
    print()
    
    # If there is a set-aside page, tell the user to put it on it
    if pages_in_group % 2:
        input("Reverse the order of the pages, flip the stack, and place on the set aside page.")
    else:
        input("Reverse the order of the pages and flip the stack.")
    print()
    print()


# - Intro -
# User warnings
print("-- WARNINGS --")
print(" -> Make sure the paper is correctly aligned to the right of the printer input.")
print(" -> Don't load too many pages in the printer at a time - they can stick.")
print(" -> If you run out of pages mid-way through printing, just wait for the printer to error, then continue.")
print()
input("Press enter to continue.")
print()

# Get the user's page range and save the start and end pages
print("Input the range of pages (e.g. 5-11).")
start_page, end_page = get_page_range()

# Find how many groups we should split the document into
total_pages = end_page - start_page + 1
total_sheets = math.ceil(total_pages / 2)

groups_required = math.ceil(total_sheets / MAX_PER_STAPLE)

# Display document printing info
print()
print("- Total Document Printing Info -")
display_group_info(start_page, end_page)
print(f"Groups required: {groups_required}")
print()
input("Press enter to continue to the group printing.")
print()

# - Printing Page Groups -
divisor = groups_required
sheets_remaining = total_sheets
pages_remaining = total_pages

group_start = start_page
for group_id in range(1, groups_required + 1):
    sheets_in_group = math.ceil(sheets_remaining / divisor)
    pages_in_group = sheets_in_group * 2

    pages_remaining -= pages_in_group
    if pages_remaining == -1:
        pages_in_group -= 1

    sheets_remaining -= sheets_in_group
    divisor -= 1

    group_end = group_start + pages_in_group - 1

    print(f"Group {group_id}/{groups_required}")
    print_group(group_start, group_end)

    group_start = group_end + 1

input("- DONE! -")
print()
