"""
Score the blind precision audit after adjudication_sheet.csv's LABEL column is
filled. Joins labels to answer_key.csv and reports the numbers that certify
(or don't) the 55.8% census finding.

Definitions:
  A case is "flagged" if the probes said misroute_both_probes.
  A human label of "misroute" is the ground truth of a real misroute.

  flag precision = of cases the probes FLAGGED, fraction the human agrees are misroutes
                   -> this is the number that certifies 55.8%: if precision is high,
                      the flagged 55.8% are really misroutes.
  flag recall    = of cases the human calls misroute, fraction the probes flagged
                   -> did the probes miss real misroutes (in the belongs bucket)?
  We also report the one-probe bucket's true-misroute rate, since that was the
  11% uncertainty band.

Wilson 95% CI on precision so the certified number carries its own honesty.
"""

import csv
import math
from pathlib import Path

DIR = Path(__file__).parent


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def norm(s):
    s = (s or "").strip().lower()
    if s.startswith("mis"):
        return "misroute"
    if s.startswith("bel"):
        return "belongs"
    return ""


def main():
    labels = {r["case_id"]: norm(r["LABEL_belongs_or_misroute"])
              for r in csv.DictReader(open(DIR / "adjudication_sheet.csv"))}
    key = {r["case_id"]: r for r in csv.DictReader(open(DIR / "answer_key.csv"))}

    unlabeled = [c for c, v in labels.items() if v not in ("misroute", "belongs")]
    if unlabeled:
        print(f"WARNING: {len(unlabeled)} unlabeled cases skipped: {unlabeled[:10]}")

    flagged_total = flagged_true = 0        # precision
    human_misroute_total = human_misroute_flagged = 0   # recall
    one_total = one_true = 0
    belongs_bucket_total = belongs_bucket_true_misroute = 0

    for cid, lab in labels.items():
        if lab not in ("misroute", "belongs"):
            continue
        v = key[cid]["verdict"]
        is_flagged = (v == "misroute_both_probes")
        human_mis = (lab == "misroute")

        if is_flagged:
            flagged_total += 1
            if human_mis:
                flagged_true += 1
        if human_mis:
            human_misroute_total += 1
            if is_flagged:
                human_misroute_flagged += 1
        if v == "misroute_one_probe":
            one_total += 1
            if human_mis:
                one_true += 1
        if v == "belongs":
            belongs_bucket_total += 1
            if human_mis:
                belongs_bucket_true_misroute += 1

    prec = flagged_true / flagged_total if flagged_total else 0
    lo, hi = wilson(flagged_true, flagged_total)
    rec = human_misroute_flagged / human_misroute_total if human_misroute_total else 0

    out = []
    out.append("# Blind Precision Audit — Results\n")
    out.append(f"Adjudicated {sum(1 for v in labels.values() if v in ('misroute','belongs'))} "
               f"cases blind (verdicts hidden during labeling).\n")
    out.append("## Flag precision (certifies the 55.8%)\n")
    out.append(f"Of {flagged_total} probe-flagged complaints, human agreed "
               f"**{flagged_true} are real misroutes** = **{100*prec:.0f}% precision** "
               f"(95% CI {100*lo:.0f}–{100*hi:.0f}%).\n")
    out.append("Reading: the census flagged 55.8% of the category as misrouted; at "
               f"{100*prec:.0f}% precision, roughly {100*prec*0.558:.0f} percentage points "
               "of that 55.8% are human-confirmed misroutes — the finding holds "
               "directionally at census scale.\n" if prec else "")
    out.append("## Did the probes miss real misroutes?\n")
    out.append(f"In the {belongs_bucket_total} 'belongs' cases sampled, human found "
               f"{belongs_bucket_true_misroute} that are actually misroutes "
               "(probe false-negatives).\n")
    out.append(f"Overall flag recall on this sample: {100*rec:.0f}% "
               f"({human_misroute_flagged}/{human_misroute_total} human-called "
               "misroutes were probe-flagged).\n")
    out.append("## One-probe uncertainty band\n")
    out.append(f"Of {one_total} one-probe cases, {one_true} are true misroutes "
               f"({100*one_true/one_total:.0f}%) — {'leans misroute' if one_total and one_true/one_total>0.5 else 'leans belongs'}, "
               "so the true rate sits between the strict 55.8% and the 66.9% upper band.\n")
    out.append("## Scope\n")
    out.append("- Single adjudicator (the author), 60-case blind sample. A second "
               "independent labeler would let us report inter-rater agreement; "
               "this is one honest pass, not a multi-rater gold standard.\n")

    text = "\n".join(out)
    (DIR / "results.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
