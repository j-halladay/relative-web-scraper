import argparse
import requests
import re
from bs4 import BeautifulSoup

__author__ = "j_halladay"


def print_results(list1):
    for element in list1:
        print(element[0])


def create_parser():
    """Create a cmd line parser object"""
    parser = argparse.ArgumentParser()

    parser.add_argument('web_address', help='html to search')
    return parser


def get_html(url):
    r = requests.get(url)
    # print(r.text, str(r))
    return r.content


def find_url(string):
    found = re.findall(
        "((http|https)://[.+a-zA-Z0-9\-]*/(.*?)(\.(.*?)|/))", string)
    return found


def find_phone(string):
    found = re.findall("((\d*-|\(\d*\)-|)\d{3}-\d{3}-\d{4})", string)
    return found


def find_email(string):
    found = re.findall("([.+a-zA-Z0-9]*@[.+a-zA-Z0-9]*\.(\w+))", string)
    return found


def main():
    list1 = []
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    html = get_html(args.web_address)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    email = find_email(html)
    phone = find_phone(html)
    url = find_url(html)
    print_results(email)
    print("...")
    print_results(phone)
    print("...")
    print_results(url)
    for i, link in enumerate(soup.find_all("a")):
        # print(link, i)
        list1.append(str(link.get("href")))
    for src in soup.find_all("img"):
        # print(src)
        list1.append(str(src.get("src")))
    # string = "".join(list(set(list1)))
    string = list(set(list1))
    print("...")
    tag_url = find_url("".join(string))
    print_results(tag_url)


if __name__ == '__main__':
    main()
