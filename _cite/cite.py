"""
cite process to convert sources and metasources into full citations
"""

import traceback
import re
from importlib import import_module
from pathlib import Path
from dotenv import load_dotenv
from util import *


# load environment variables
load_dotenv()


# save errors/warnings for reporting at end
errors = []
warnings = []
source_unavailable = False

# output citations file
output_file = "_data/citations.yaml"


log()

log("Compiling sources")

# compiled list of sources
sources = []

# in-order list of plugins to run
plugins = ["dblp", "google-scholar", "pubmed", "orcid", "sources"]

# loop through plugins
for plugin in plugins:
    # convert into path object
    plugin = Path(f"plugins/{plugin}.py")

    log(f"Running {plugin.stem} plugin")

    # get all data files to process with current plugin
    files = Path.cwd().glob(f"_data/{plugin.stem}*.*")
    files = list(filter(lambda p: p.suffix in [".yaml", ".yml", ".json"], files))

    log(f"Found {len(files)} {plugin.stem}* data file(s)", indent=1)

    # loop through data files
    for file in files:
        log(f"Processing data file {file.name}", indent=1)

        # load data from file
        try:
            data = load_data(file)
            # check if file in correct format
            if not list_of_dicts(data):
                raise Exception(f"{file.name} data file not a list of dicts")
        except Exception as e:
            log(e, indent=2, level="ERROR")
            errors.append(e)
            continue

        # loop through data entries
        for index, entry in enumerate(data):
            log(f"Processing entry {index + 1} of {len(data)}, {label(entry)}", level=2)

            # run plugin on data entry to expand into multiple sources
            try:
                expanded = import_module(f"plugins.{plugin.stem}").main(entry)
                # check that plugin returned correct format
                if not list_of_dicts(expanded):
                    raise Exception(f"{plugin.stem} plugin didn't return list of dicts")
            # catch any plugin error
            except Exception as e:
                if isinstance(e, TransientCitationSourceError):
                    source_unavailable = True
                    log(e, indent=3, level="WARNING")
                    warnings.append(str(e))
                    continue

                # log detailed pre-formatted/colored trace
                print(traceback.format_exc())
                # log high-level error
                log(e, indent=3, level="ERROR")
                errors.append(e)
                continue

            # loop through sources
            for source in expanded:
                if plugin.stem != "sources":
                    log(label(source), level=3)

                # include meta info about source
                source["plugin"] = plugin.name
                source["file"] = file.name

                # add source to compiled list
                sources.append(source)

            if plugin.stem != "sources":
                log(f"{len(expanded)} source(s)", indent=3)


log("Merging sources by id")

# merge sources with matching (non-blank) ids
for a in range(0, len(sources)):
    a_id = get_safe(sources, f"{a}.id", "")
    if not a_id:
        continue
    for b in range(a + 1, len(sources)):
        b_id = get_safe(sources, f"{b}.id", "")
        if b_id == a_id:
            log(f"Found duplicate {b_id}", indent=2)
            sources[a].update(sources[b])
            sources[b] = {}
sources = [entry for entry in sources if entry]


log(f"{len(sources)} total source(s) to cite")


log()

log("Generating citations")

# list of new citations
citations = []


# loop through compiled sources
for index, source in enumerate(sources):
    log(f"Processing source {index + 1} of {len(sources)}, {label(source)}")

    # if explicitly flagged, remove/ignore entry
    if get_safe(source, "remove", False) == True:
        continue

    # new citation data for source
    citation = {}

    # source id
    _id = get_safe(source, "id", "").strip()

    # manubot doesn't work without an id
    if _id:
        log("Using Manubot to generate citation", indent=1)

        try:
            # run manubot and set citation
            citation = cite_with_manubot(_id)

        # if manubot cannot cite source
        except Exception as e:
            plugin = get_safe(source, "plugin", "")
            file = get_safe(source, "file", "")
            # if regular source (id entered by user), throw error
            if plugin == "sources.py":
                log(e, indent=3, level="ERROR")
                errors.append(f"Manubot could not generate citation for source {_id}")
            # otherwise, if from metasource (id retrieved from some third-party api), just warn
            else:
                log(e, indent=3, level="WARNING")
                warnings.append(
                    f"Manubot could not generate citation for source {_id} (from {file} with {plugin})"
                )
                # discard source from citations
                continue

    # preserve fields from input source, overriding existing fields
    citation.update(source)

    # ensure date in proper format for correct date sorting
    if get_safe(citation, "date", ""):
        citation["date"] = format_date(get_safe(citation, "date", ""))

    # add new citation to list
    citations.append(citation)


log()

log("Merging duplicate citations and assigning tags")


def normalized_title(citation):
    title = str(get_safe(citation, "title", "")).lower()
    return re.sub(r"[^a-z0-9]+", "", title)


def merge_values(target, incoming):
    for key, value in incoming.items():
        if value in [None, "", [], {}]:
            continue
        if key == "citation_count":
            target[key] = max(int(target.get(key, 0) or 0), int(value or 0))
        elif key == "authors" and target.get(key):
            continue
        elif not target.get(key):
            target[key] = value


deduplicated = []
by_doi = {}
by_title = {}
for citation in citations:
    doi_key = str(get_safe(citation, "doi", "")).strip().lower()
    title_key = normalized_title(citation)
    existing = by_doi.get(doi_key) if doi_key else None
    existing = existing or (by_title.get(title_key) if title_key else None)
    if existing:
        merge_values(existing, citation)
        continue
    deduplicated.append(citation)
    if doi_key:
        by_doi[doi_key] = citation
    if title_key:
        by_title[title_key] = citation


tag_rules = {
    "Foundation Models": [
        "foundation model",
        "large language model",
        "llm",
        "aigc",
        "genai",
        "generative model",
        "large-small model",
    ],
    "Industrial Agents": [
        "agent",
        "embodied",
        "robot",
        "grasp",
        "manipulation",
        "task and motion",
    ],
    "Industrial Time Series": [
        "time series",
        "time-series",
        "anomaly",
        "remaining useful life",
        "rul",
        "fault",
        "health status",
        "temporal",
    ],
    "Industrial Internet & Edge": [
        "industrial internet",
        "iiot",
        "edge computing",
        "cloud computing",
        "offloading",
        "cyber-physical",
    ],
    "Industrial Software & Control": [
        "industrial software",
        "plc",
        "control logic",
        "process control",
        "automation",
    ],
    "Knowledge & Decision Intelligence": [
        "knowledge graph",
        "domain adaptation",
        "graph clustering",
        "fuzzy",
        "optimization",
        "scheduling",
        "differential evolution",
        "reinforcement learning",
    ],
    "Smart Manufacturing": [
        "manufactur",
        "shopfloor",
        "job shop",
        "production",
        "machining",
        "supply chain",
    ],
}


for citation in deduplicated:
    date = str(get_safe(citation, "date", ""))
    year = str(get_safe(citation, "year", "")) or date[:4]
    citation["year"] = int(year) if year.isdigit() else year

    publication_type = str(get_safe(citation, "type", "")).strip()
    searchable = " ".join(
        [
            str(get_safe(citation, "title", "")),
            str(get_safe(citation, "publisher", "")),
        ]
    ).lower()
    if not publication_type:
        if "arxiv" in searchable or "corr" in searchable or "preprint" in searchable:
            publication_type = "Preprint"
        elif "conference" in searchable or "proceedings" in searchable:
            publication_type = "Conference"
        else:
            publication_type = "Journal"
    citation["type"] = publication_type

    tags = list(get_safe(citation, "tags", []) or [])
    if publication_type not in tags:
        tags.append(publication_type)
    for tag, keywords in tag_rules.items():
        if any(keyword in searchable for keyword in keywords) and tag not in tags:
            tags.append(tag)
    if len(tags) == 1:
        tags.append("Industrial AI")
    citation["tags"] = tags

    if not get_safe(citation, "link", ""):
        citation["link"] = get_safe(citation, "dblp", "") or get_safe(
            citation, "scholar_link", ""
        )


citations = sorted(
    deduplicated,
    key=lambda citation: (
        int(get_safe(citation, "year", 0) or 0)
        if str(get_safe(citation, "year", "")).isdigit()
        else 0,
        str(get_safe(citation, "title", "")).lower(),
    ),
    reverse=True,
)

log(f"{len(citations)} unique citation(s)", indent=1)

log()

log("Saving updated citations")


# save new citations
if not citations and Path(output_file).exists():
    message = (
        "Skipping citation file update because no citation sources were found. "
        f"Existing {output_file} remains unchanged."
    )
    log(message, level="WARNING")
    warnings.append(message)
elif source_unavailable and Path(output_file).exists():
    message = (
        "Skipping citation file update because an external citation source was "
        f"temporarily unavailable. Existing {output_file} remains unchanged."
    )
    log(message, level="WARNING")
    warnings.append(message)
else:
    try:
        save_data(output_file, citations)
    except Exception as e:
        log(e, level="ERROR")
        errors.append(e)


log()


# exit at end, so user can see all errors/warnings in one run
if len(warnings):
    log(f"{len(warnings)} warning(s) occurred above", level="WARNING")
    for warning in warnings:
        log(warning, indent=1, level="WARNING")

if len(errors):
    log(f"{len(errors)} error(s) occurred above", level="ERROR")
    for error in errors:
        log(error, indent=1, level="ERROR")
    log()
    exit(1)

else:
    log("All done!", level="SUCCESS")

log()
