#!/usr/bin/env python3
"""Saturday Weekly Retrospective — aggregator + classifier over pastweek."""
import json, os, sys, re, datetime
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(__file__))
from classify import BUCKETS, assign_bucket, primary_badge

OUT = "out"
TODAY = datetime.date.today().isoformat()
ISO_YEAR, ISO_WEEK, _ = datetime.date.today().isocalendar()
WEEK_LABEL = f"{ISO_YEAR}-W{ISO_WEEK:02d}"
WEEK_END = datetime.date.today()
WEEK_START = WEEK_END - datetime.timedelta(days=6)

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def classify_pastweek():
    cv = load(f"{OUT}/cv_pastweek.json")
    ro = load(f"{OUT}/ro_pastweek.json")
    by_id = {}
    for p in cv + ro:
        by_id.setdefault(p["arxiv_id"], p)
    papers = list(by_id.values())
    for p in papers:
        p["bucket"] = assign_bucket(p["title"], p.get("abstract", ""), p.get("subjects", ""))
        p["badge"] = primary_badge(p)
    return papers

def bucket_aggregate(papers):
    g = defaultdict(list)
    for p in papers:
        if p["bucket"]:
            g[p["bucket"]].append(p)
    out = {}
    for b, _ in BUCKETS:
        items = g[b]
        cv_n = sum(1 for p in items if "CV" in p["badge"] and "/" not in p["badge"])
        ro_n = sum(1 for p in items if p["badge"] == "RO")
        cvro_n = sum(1 for p in items if p["badge"] == "CV/RO")
        out[b] = {"total": len(items), "cv": cv_n, "ro": ro_n, "cvro": cvro_n, "papers": items}
    return out

def keyword_extract(papers, top_n=15):
    """Top keywords from titles+abstracts (lowercase, length>=3)."""
    KEYS = []
    for _, kws in BUCKETS:
        KEYS.extend(kws)
    KEYS = list(set(KEYS))
    cv_c, ro_c = Counter(), Counter()
    for p in papers:
        text = (p["title"] + " " + p.get("abstract","")).lower()
        is_cv = "CV" in p["badge"] and "/" not in p["badge"]
        is_ro = p["badge"] == "RO"
        is_cvro = p["badge"] == "CV/RO"
        for kw in KEYS:
            if kw in text:
                if is_cv or is_cvro: cv_c[kw] += 1
                if is_ro or is_cvro: ro_c[kw] += 1
    return cv_c.most_common(top_n), ro_c.most_common(top_n)

def main():
    papers = classify_pastweek()
    buckets = bucket_aggregate(papers)
    cv_kw, ro_kw = keyword_extract(papers, top_n=20)
    snapshot = {
        "date": TODAY,
        "iso_week": WEEK_LABEL,
        "week_start": WEEK_START.isoformat(),
        "week_end": WEEK_END.isoformat(),
        "totals": {
            "selected": sum(buckets[b]["total"] for b, _ in BUCKETS),
            "total_scanned": len(papers),
        },
        "buckets": {b: {k: v for k, v in buckets[b].items() if k != "papers"} for b, _ in BUCKETS},
        "keywords_cv": cv_kw,
        "keywords_ro": ro_kw,
    }
    # Save full snapshot (with paper detail) for HTML builder.
    with open(f"{OUT}/weekly_full.json", "w", encoding="utf-8") as f:
        json.dump({"snapshot": snapshot, "buckets_full": buckets}, f, ensure_ascii=False, indent=1, default=str)
    # Save light snapshot like trends/.
    with open(f"trends/{TODAY}.json", "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=1)
    print("OK", WEEK_LABEL, "selected", snapshot["totals"]["selected"], "of", snapshot["totals"]["total_scanned"])

if __name__ == "__main__":
    main()
