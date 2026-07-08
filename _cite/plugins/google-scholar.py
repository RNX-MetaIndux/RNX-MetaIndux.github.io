import os
from serpapi import GoogleSearch
from util import *


def main(entry):
    """
    receives single list entry from google-scholar data file
    returns list of sources to cite
    """

    # get api key (serp api key to access google scholar)
    api_key = os.environ.get("GOOGLE_SCHOLAR_API_KEY", "")
    if not api_key:
        log(
            'Skipping Google Scholar: no "GOOGLE_SCHOLAR_API_KEY" env var',
            indent=3,
            level="WARNING",
        )
        return []

    # serp api properties
    params = {"engine": "google_scholar_author", "api_key": api_key, "num": 100}

    # get id from entry
    _id = get_safe(entry, "gsid", "")
    if not _id:
        raise Exception('No "gsid" key')

    # query api
    @log_cache
    @cache.memoize(name=__file__, expire=1 * (60 * 60 * 24))
    def query(_id, start):
        request_params = params | {"author_id": _id, "start": start, "sort": "pubdate"}
        return get_safe(GoogleSearch(request_params).get_dict(), "articles", [])

    response = []
    for start in range(0, 1000, 100):
        page = query(_id, start)
        response.extend(page)
        if len(page) < 100:
            break

    # list of sources to return
    sources = []

    # go through response and format sources
    for work in response:
        # create source
        year = get_safe(work, "year", "")
        source = {
            # Scholar citation ids are not DOI-like identifiers and cannot be
            # passed to Manubot. Keep them in a dedicated field instead.
            "scholar_id": get_safe(work, "citation_id", ""),
            "title": get_safe(work, "title", ""),
            "authors": list(map(str.strip, get_safe(work, "authors", "").split(","))),
            "publisher": get_safe(work, "publication", ""),
            "date": (year + "-01-01") if year else "",
            "link": get_safe(work, "link", ""),
            "scholar_link": get_safe(work, "link", ""),
            "citation_count": get_safe(work, "cited_by.value", 0),
        }

        # copy fields from entry to source
        source.update(entry)

        # add source to list
        sources.append(source)

    return sources
