"""
Blind precision audit for the DCM misrouting finding.

The census says 55.8% of "Debt or credit management" complaints don't belong
(two probes agreed). That's a model-vs-model number. This audit certifies it
against a blind human judgment: sample flagged AND unflagged complaints, shuffle
them so the labeler can't tell which the probes picked, have a human label each
belongs/doesn't, THEN compare to the probes.

Two scripts:
  build_sheet.py  -> makes adjudication_sheet.csv (shuffled, verdicts hidden)
                     and answer_key.csv (held separately, NOT for the labeler)
  score.py        -> after the human fills the LABEL column, joins to the key
                     and computes flag precision, recall, and agreement.

Sampling (seed fixed for reproducibility):
  35 flagged (misroute_both_probes)  -> precision numerator/denominator
  15 belongs                          -> false-negative check (did probes miss real misroutes?)
  10 misroute_one_probe               -> the uncertainty band, adjudicated
  = 60 cases. Enough to certify direction and put a real CI on precision;
  not so many the hand-labeling becomes a second job.
"""

import csv
import random
from pathlib import Path

DIR = Path(__file__).parent
SRC = DIR.parent
SEED = 20260725
N_FLAGGED, N_BELONGS, N_ONE = 35, 15, 10


def main():
    res = {r["complaint_id"]: r for r in csv.DictReader(open(SRC / "results.csv"))}
    narr = {r["complaint_id"]: r["narrative"]
            for r in csv.DictReader(open(SRC / "dcm_narratives.csv"))}

    buckets = {"misroute_both_probes": [], "belongs": [], "misroute_one_probe": []}
    for cid, r in res.items():
        if cid in narr and r["verdict"] in buckets:
            buckets[r["verdict"]].append(cid)

    random.seed(SEED)
    picked = (random.sample(buckets["misroute_both_probes"], N_FLAGGED)
              + random.sample(buckets["belongs"], N_BELONGS)
              + random.sample(buckets["misroute_one_probe"], N_ONE))
    random.shuffle(picked)

    # sheet: shuffled, NO verdict shown. case_id is a fresh index, not the
    # complaint_id, so ordering leaks nothing.
    with open(DIR / "adjudication_sheet.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "narrative",
                    "LABEL_belongs_or_misroute", "notes_optional"])
        for i, cid in enumerate(picked, 1):
            w.writerow([f"C{i:02d}", narr[cid].strip().replace("\r", " "), "", ""])

    # key: held separately, maps case_id -> true complaint_id + what the probes said
    with open(DIR / "answer_key.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "complaint_id", "verdict",
                    "probe_a_category", "probe_b_belongs"])
        for i, cid in enumerate(picked, 1):
            r = res[cid]
            w.writerow([f"C{i:02d}", cid, r["verdict"],
                        r["probe_a_category"], r["probe_b_belongs"]])

    print(f"Wrote adjudication_sheet.csv ({len(picked)} cases, verdicts hidden)")
    print("Wrote answer_key.csv (do NOT open before labeling)")
    print("\nHow to label: follow the rule in LABELING_SHEET.md (CFPB's four")
    print("sub-products; relief seller -> 'belongs', lender/servicer/collector/")
    print("bureau -> 'misroute'), fill the LABEL column, then run score.py.")


if __name__ == "__main__":
    main()
