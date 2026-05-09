import csv
import sys
from html import escape
from urllib.parse import urlparse
 
 
def is_url(value: str) -> bool:
    try:
        result = urlparse(value)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except ValueError:
        return False

def csv_to_html_list(input_path: str, output_path: str | None = None) -> str:
    items = []
 
    with open(input_path, newline="", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
 
        if csv_file.fieldnames is None:
            raise ValueError("CSV has no headers.")
 
        headers = [h.strip().lower() for h in csv_file.fieldnames]
        csv_file.fieldnames = headers
        print("headers:", headers)
 
        required = {"paper title", "list of all authors", "paper link"}
        missing = required - set(headers)
        if missing:
            raise ValueError(f"CSV is missing expected columns: {missing}")
 
        for row in csv_file:
            title = escape(row["paper title"].strip())
            authors = escape(row["list of all authors"].strip())
            link = escape(row["paper link"].strip())

            title_html = f'<a href="{escape(link)}">{title}</a>' if is_url(link) else title

            item = (
                f"<li> {title_html} <br>\n"
                f"     <i>{authors}</i> </li> <br>"
            )
            items.append(item)
 
    html = "\n".join(items)
 
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Written to {output_path}")
    else:
        print(html)
 
    return html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
 
    input_csv = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) >= 3 else None
    csv_to_html_list(input_csv, output_html)
