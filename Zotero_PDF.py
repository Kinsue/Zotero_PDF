import csv
import argparse
import shutil
from pathlib import Path  

parser = argparse.ArgumentParser(
    description='Copy PDFs from Zotero to the given destination.')
parser.add_argument('-c', '--csv', type=Path,
                    required=True, help='CSV file exported from Zotero')
parser.add_argument('-d', '--dest', type=Path,
                    default='./pdfs', help='Destination folder for the PDFs')
args = parser.parse_args()

copySuccess = 0
copyFail = 0

if not args.dest.is_dir():
    print("Destination is not a folder.")
    exit(1)

if not args.dest.exists():
    args.dest.mkdir(parents=True)

with open(args.csv, newline='', encoding='utf-8-sig') as csvfile:
    cr = csv.DictReader(csvfile)
    for row in cr:
        file = row["File Attachments"]
        file_list = [Path(pdf.strip()) for pdf in file.split(";") if Path(pdf).suffix == ".pdf"]
        for f in file_list:
            try:
                shutil.copy(f, args.dest.absolute())
                copySuccess = copySuccess + 1
            except FileExistsError:
                print("Failed to copy {}".format(f))
                copyFail = copyFail + 1

print("Done. {} Succeed, {} Failed.".format(copySuccess, copyFail))


