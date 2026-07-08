import re
import xml.etree.ElementTree as ET
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from util import *


def element_text(element):
    if element is None:
        return ""
    return "".join(element.itertext()).strip().rstrip(".")


def main(entry):
    """Expand a persistent DBLP person id into publication records."""

    pid = get_safe(entry, "pid", "").strip()
    if not pid:
        raise Exception('No "pid" key')

    transient_status_codes = {408, 425, 429, 500, 502, 503, 504}

    @log_cache
    @cache.memoize(name=__file__, expire=1 * (60 * 60 * 24))
    def query(person_id):
        url = f"https://dblp.org/pid/{person_id}.xml"
        request = Request(
            url,
            headers={
                "User-Agent": "RNX-MetaIndux publication sync (rnx_metaindux@163.com)"
            },
        )

        last_error = None
        for attempt in range(3):
            try:
                return urlopen(request, timeout=90).read()
            except HTTPError as error:
                if error.code not in transient_status_codes:
                    raise
                last_error = error
            except (TimeoutError, URLError) as error:
                last_error = error

            if attempt < 2:
                sleep(2 * (attempt + 1))

        raise TransientCitationSourceError(
            f'DBLP is temporarily unavailable for pid "{person_id}": {last_error}'
        )

    root = ET.fromstring(query(pid))
    sources = []
    type_names = {
        "article": "Journal",
        "inproceedings": "Conference",
        "incollection": "Book Chapter",
        "book": "Book",
        "phdthesis": "Thesis",
        "mastersthesis": "Thesis",
    }

    for wrapper in root.findall("r"):
        record = next(iter(wrapper), None)
        if record is None:
            continue

        title = element_text(record.find("title"))
        if not title:
            continue

        key = record.attrib.get("key", "")
        year = element_text(record.find("year"))
        venue = (
            element_text(record.find("journal"))
            or element_text(record.find("booktitle"))
            or element_text(record.find("publisher"))
            or element_text(record.find("school"))
        )
        record_type = type_names.get(record.tag, "Publication")
        if record.attrib.get("publtype") == "informal":
            record_type = "Preprint"

        authors = [element_text(author) for author in record.findall("author")]
        authors = [re.sub(r"\s+\d{4}$", "", author) for author in authors]

        electronic_editions = [element_text(ee) for ee in record.findall("ee")]
        doi_link = next(
            (link for link in electronic_editions if "doi.org/" in link.lower()), ""
        )
        doi = doi_link.split("doi.org/", 1)[-1] if doi_link else ""
        dblp_link = f"https://dblp.org/rec/{key}" if key else ""
        link = doi_link or next(iter(electronic_editions), "") or dblp_link

        source = {
            "title": title,
            "authors": authors,
            "publisher": venue,
            "date": f"{year}-01-01" if year else "",
            "year": int(year) if year.isdigit() else year,
            "type": record_type,
            "link": link,
            "dblp": dblp_link,
            "dblp_key": key,
        }
        if doi:
            source["doi"] = doi

        source.update(entry)
        sources.append(source)

    return sources
