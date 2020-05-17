import bs4, csv, os, time
from urllib import request


URL = "https://otakudesu.org/"
filename = "anime_schedule.csv"
fieldnames = ['Name', 'Episode', 'Day', 'Date', 'Href', 'Src_img']
current_path = os.path.dirname(__file__)
full_path = os.path.join(current_path, filename)

def get_tags(url):
    html = request.urlopen(url)
    soup = bs4.BeautifulSoup(html, "html.parser")

    parent = soup.find('div', class_="venz")
    subparent = parent.ul.find_all('div', class_='detpost')
    return subparent

def parse_html(tags, fieldnames):
    data_rows = []
    for children in tags:
        rows = []
        # This code replacable (until 'end')
        for child in children:
            if child.a:
                rows.append(child.a['href'])
                src_img = child.a.find('div', class_="thumbz").img
                rows.append(src_img['src'])
                rows.insert(0, src_img['alt']) # Insert name to index 0
            else:
                rows.append(child.text)
        # end

        data = {field: row for field, row in zip(fieldnames, rows)}
        data_rows.append(data)

    return data_rows


def create_csv(filename, fieldnames, tags):
    with open(filename, 'w') as fh:
        data = parse_html(tags, fieldnames)
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)



if __name__ == '__main__':
    tags = get_tags(URL)
    create_csv(filename=full_path, fieldnames=fieldnames,
               tags=tags)