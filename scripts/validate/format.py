# -*- coding: utf-8 -*-

import re
import sys
from string import punctuation
from typing import List, Tuple, Dict


# Temporary replacement
# The descriptions that contain () at the end must adapt to the new policy later
punctuation = punctuation.replace('()', '')

anchor = '###'
auth_keys = ['apiKey', 'OAuth', 'X-Mashape-Key', 'User-Agent', 'No']
https_keys = ['Yes', 'No']
cors_keys = ['Yes', 'No', 'Unknown']

index_title = 0
index_desc = 1
index_auth = 2
index_https = 3
index_cors = 4

num_segments = 5
min_entries_per_category = 3
max_description_length = 100

anchor_re = re.compile(anchor + '\s(.+)')
category_title_in_index_re = re.compile('\*\s\[(.*)\]')
link_re = re.compile('\[(.+)\]\((http.*)\)')

# Type aliases
APIList = List[str]
Categories = Dict[str, APIList]
CategoriesLineNumber = Dict[str, int]


def error_message(line_number: int, message: str) -> str:
    line = line_number + 1
    return f'(L{line:03d}) {message}'


def get_categories_content(contents: List[str]) -> Tuple[Categories, CategoriesLineNumber]:
    """
    Given a string of code contents, identifies and extracts categories from the
    content by looking for lines that start with an anchor (``), followed by a
    space-separated list of category names. It then creates a dictionary of
    categories with their corresponding line numbers.

    Args:
        contents (List[str]): 1D list of lines to be processed by the function,
            which contains the content of the Markdown file to be parsed and
            analyzed for categories.

    Returns:
        Tuple[Categories, CategoriesLineNumber]: a dictionary of categories and
        their corresponding line numbers in the input contents.

    """
    categories = {}
    category_line_num = {}
    for line_num, line_content in enumerate(contents):
        if line_content.startswith(anchor):
            category = line_content.split(anchor)[1].strip()
            categories[category] = []
            category_line_num[category] = line_num
            continue
        if not line_content.startswith('|') or line_content.startswith('|---'):
            continue
        raw_title = [raw_content.strip() for raw_content in line_content.split('|')[1:-1]][0]
        title_match = link_re.match(raw_title)
        if title_match:
                title = title_match.group(1).upper()
                categories[category].append(title)
    return (categories, category_line_num)


def check_alphabetical_order(lines: List[str]) -> List[str]:
    """
    Takes a list of categories and their corresponding API lists as input, checks
    if the API lists are alphabetized, and returns an array of error messages if
    they are not.

    Args:
        lines (List[str]): contents of a file that needs to be analyzed for
            categorization purposes.

    Returns:
        List[str]: a list of error messages related to non-alphabetical ordering
        of API lists.

    """
    err_msgs = []
    categories, category_line_num = get_categories_content(contents=lines)
    for category, api_list in categories.items():
        if sorted(api_list) != api_list:
            err_msg = error_message(category_line_num[category], f'{category} category is not alphabetical order')
            err_msgs.append(err_msg)
    return err_msgs


def check_title(line_num: int, raw_title: str) -> List[str]:
    """
    Validates the title of a documentation page, ensuring it meets specific
    formatting requirements, and returns an error message if not.

    Args:
        line_num (int): 1: line number where the issue was encountered in the code
            being documented, and is used to create a descriptive error message.
        raw_title (str): Markdown title of the documentation entry to be checked
            for validity.

    Returns:
        List[str]: a list of error messages corresponding to each error in the
        title format.

    """
    err_msgs = []
    title_match = link_re.match(raw_title)
    # url should be wrapped in "[TITLE](LINK)" Markdown syntax
    if not title_match:
        err_msg = error_message(line_num, 'Title syntax should be "[TITLE](LINK)"')
        err_msgs.append(err_msg)
    else:
        # do not allow "... API" in the entry title
        title = title_match.group(1)
        if title.upper().endswith(' API'):
            err_msg = error_message(line_num, 'Title should not end with "... API". Every entry is an API here!')
            err_msgs.append(err_msg)
    return err_msgs


def check_description(line_num: int, description: str) -> List[str]:
    """
    Checks the first character and last character of a string, and calculates its
    length to ensure it conforms to specified rules for a description in code
    documentation. It returns an array of error messages if any rule is violated.

    Args:
        line_num (int): line number of the code snippet where the description is
            located, which is used to generate specific error messages for each
            violation of the description rules.
        description (str): 2D code's description, which is evaluated for validity
            based on its length and character content to produce an array of error
            messages.

    Returns:
        List[str]: a list of error messages associated with the given description.

    """
    err_msgs = []
    first_char = description[0]
    if first_char.upper() != first_char:
        err_msg = error_message(line_num, 'first character of description is not capitalized')
        err_msgs.append(err_msg)
    last_char = description[-1]
    if last_char in punctuation:
        err_msg = error_message(line_num, f'description should not end with {last_char}')
        err_msgs.append(err_msg)
    desc_length = len(description)
    if desc_length > max_description_length:
        err_msg = error_message(line_num, f'description should not exceed {max_description_length} characters (currently {desc_length})')
        err_msgs.append(err_msg)
    return err_msgs


def check_auth(line_num: int, auth: str) -> List[str]:
    """
    Checks whether the `auth` value is properly enclosed with backticks and if it
    is a valid auth option based on a list of known options.

    Args:
        line_num (int): 1: line number of the code snippet where the `auth` value
            is encountered.
        auth (str): authentication value that is checked for proper enclosure with
            backticks and validity against a list of possible auth options.

    Returns:
        List[str]: an array of error messages for each input authentication value
        that does not meet the requirements.

    """
    err_msgs = []
    backtick = '`'
    if auth != 'No' and (not auth.startswith(backtick) or not auth.endswith(backtick)):
        err_msg = error_message(line_num, 'auth value is not enclosed with `backticks`')
        err_msgs.append(err_msg)
    if auth.replace(backtick, '') not in auth_keys:
        err_msg = error_message(line_num, f'{auth} is not a valid Auth option')
        err_msgs.append(err_msg)
    return err_msgs


def check_https(line_num: int, https: str) -> List[str]:
    """
    Verifies if an provided HTTPS option is valid or not, and returns an array of
    error messages if it's not.

    Args:
        line_num (int): line number of the line containing the HTTPS option being
            checked for validity.
        https (str): HTTPS option to check if it is valid.

    Returns:
        List[str]: a list of error messages, each containing a line number and a
        message indicating that the input HTTPS option is invalid.

    """
    err_msgs = []
    if https not in https_keys:
        err_msg = error_message(line_num, f'{https} is not a valid HTTPS option')
        err_msgs.append(err_msg)
    return err_msgs


def check_cors(line_num: int, cors: str) -> List[str]:
    """
    Checks if the given CORS options are valid. If not, it appends an error message
    to a list of errors.

    Args:
        line_num (int): 10-digit line number of the error message to be generated
            if the `cors` input is not a valid CORS option.
        cors (str): 2nd option for the `cors` parameter in the given line of code,
            and checks if it is a valid CORS option.

    Returns:
        List[str]: an array of error messages if the provided CORS options are invalid.

    """
    err_msgs = []
    if cors not in cors_keys:
        err_msg = error_message(line_num, f'{cors} is not a valid CORS option')
        err_msgs.append(err_msg)
    return err_msgs


def check_entry(line_num: int, segments: List[str]) -> List[str]:
    """
    Performs error checking for various segments in an HTML document: title,
    description, authorization, HTTPS, and CORS. It returns an array of error
    messages if any are found.

    Args:
        line_num (int): 1-based line number of the section of code being processed,
            which is used to generate error messages for each validation check
            performed in the function.
        segments (List[str]): 5 sections of information to be checked for errors,
            including the title, description, authentication information, HTTPS
            status, and CORS configuration.

    Returns:
        List[str]: an array of error messages related to the title, description,
        authentication, HTTPS, and CORS configuration of a web API.

    """
    raw_title = segments[index_title]
    description = segments[index_desc]
    auth = segments[index_auth]
    https = segments[index_https]
    cors = segments[index_cors]
    title_err_msgs = check_title(line_num, raw_title)
    desc_err_msgs = check_description(line_num, description)
    auth_err_msgs = check_auth(line_num, auth)
    https_err_msgs = check_https(line_num, https)
    cors_err_msgs = check_cors(line_num, cors)
    err_msgs = [*title_err_msgs, 
                *desc_err_msgs, 
                *auth_err_msgs, 
                *https_err_msgs, 
                *cors_err_msgs]
    return err_msgs


def check_file_format(lines: List[str]) -> List[str]:
    """
    Processes a list of text files and returns an array of error messages if any
    are found in the files.

    Args:
        lines (List[str]): 1D list of lines that contain the text to be checked
            for formatting errors, and the function processes each line in the
            list and adds any errors found to a list of error messages.

    Returns:
        List[str]: a list of error messages indicating discrepancies in the format
        of the given code documentation.

    """
    err_msgs = []
    category_title_in_index = []
    alphabetical_err_msgs = check_alphabetical_order(lines)
    err_msgs.extend(alphabetical_err_msgs)
    num_in_category = min_entries_per_category + 1
    category = ''
    category_line = 0
    for line_num, line_content in enumerate(lines):
        category_title_match = category_title_in_index_re.match(line_content)
        if category_title_match:
            category_title_in_index.append(category_title_match.group(1))
        # check each category for the minimum number of entries
        if line_content.startswith(anchor):
            category_match = anchor_re.match(line_content)
            if category_match:
                if category_match.group(1) not in category_title_in_index:
                    err_msg = error_message(line_num, f'category header ({category_match.group(1)}) not added to Index section')
                    err_msgs.append(err_msg)
            else:
                err_msg = error_message(line_num, 'category header is not formatted correctly')
                err_msgs.append(err_msg)
            if num_in_category < min_entries_per_category:
                err_msg = error_message(category_line, 
                                        f'{category} category does not have the minimum {min_entries_per_category} entries (only has {num_in_category})')
                err_msgs.append(err_msg)
            category = line_content.split(' ')[1]
            category_line = line_num
            num_in_category = 0
            continue
        # skips lines that we do not care about
        if not line_content.startswith('|') or line_content.startswith('|---'):
            continue
        num_in_category += 1
        segments = line_content.split('|')[1:-1]
        if len(segments) < num_segments:
            err_msg = error_message(line_num, f'entry does not have all the required columns (have {len(segments)}, need {num_segments})')
            err_msgs.append(err_msg)
            continue
        for segment in segments:
            # every line segment should start and end with exactly 1 space
            if len(segment) - len(segment.lstrip()) != 1 or len(segment) - len(segment.rstrip()) != 1:
                err_msg = error_message(line_num, 'each segment must start and end with exactly 1 space')
                err_msgs.append(err_msg)
        segments = [segment.strip() for segment in segments]
        entry_err_msgs = check_entry(line_num, segments)
        err_msgs.extend(entry_err_msgs)
    return err_msgs


def main(filename: str) -> None:
    """
    Reads a file in 'utf-8' encoding and mode 'r' (opening in read mode). It then
    lists each line and checks if there are any errors in the file format using
    `check_file_format()`; If any errors are found, it prints each error message
    and exits the program with a status code of 1.

    Args:
        filename (str): name of the file to be checked for proper format.

    """
    with open(filename, mode='r', encoding='utf-8') as file:
        lines = list(line.rstrip() for line in file)
    file_format_err_msgs = check_file_format(lines)
    if file_format_err_msgs:
        for err_msg in file_format_err_msgs:
            print(err_msg)
        sys.exit(1)


if __name__ == '__main__':
    num_args = len(sys.argv)
    if num_args < 2:
        print('No .md file passed (file should contain Markdown table syntax)')
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)
