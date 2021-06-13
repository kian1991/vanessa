import PyPDF2
import re

PAGE_OFFSET = - 6

umlaute = {'ä': 'Ñ', 'ü': 'Õ', 'ö': 'Ó', 'ß': 'û'}
ignore_list = ['der', 'das', 'die', '#', ' - ']
skip_list = ['siehe', 'auch']

# Open the pdf file
pdf = PyPDF2.PdfFileReader("decrypted.pdf")

# Get number of pages
num_pages = pdf.getNumPages()


with open('names.txt', 'r') as inputfile:
    for line in inputfile.readlines():
        new_line = '';
        stripped_line = line.rstrip()
        strings = stripped_line.split(',')
        if len(strings) < 2:
            strings = stripped_line.split('/')


        # check skip list
        for index, string in enumerate(strings):
            for item in skip_list:
                if item in string:
                    if len(strings) > 1:
                        del strings[index]

        # Replace Umlaute
        for key, value in umlaute.items():
            strings = [string.replace(key, value) for string in strings]
        # ignore words or characters
        for item in ignore_list:
            strings = [string.replace(item, '') for string in strings]
        # strip whitespaces
        strings = [string.replace(' ', '') for string in strings]
        print(strings)
        results = []

        # Extract text and do the search
        for i in range(0, num_pages):
            page_obj = pdf.getPage(i)
            text = page_obj.extractText()
            for string in strings:
                if re.search(string.lower(),text.lower()):
                    results.append(str(i + PAGE_OFFSET))

        result_string = ''
        for x in results:
            result_string += f'{x}, '
        result_string = result_string[:-2]

        new_line += f'{line.rstrip()}  {result_string}\n'
        with open('output.txt', 'a') as output_file:
            output_file.writelines(new_line)