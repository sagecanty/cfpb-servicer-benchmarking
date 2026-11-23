# DCM Misrouting Audit — Full Census Results

*Exec-facing version of this finding: [../../docs/05_executive_brief.md](../../docs/05_executive_brief.md).*

Follow-up to the Phase 2 feasibility eval's flagged next step (evals/README.md):
"Debt or credit management" showed 44% classifier agreement on a 50-complaint
stratified sample — 20+ points below every other category. This audit pulls
the FULL population (not a sample) to size the problem.

## Method

- **Population:** every CA "Debt or credit management" complaint with a
  published narrative, Jan 2024–Jun 2026 (504 narratives — see
  `pull_dcm.py`, wider window than the main benchmarking analysis since this
  is an intake-behavior question, not a benchmarking-snapshot question)
- **Two independent probes per complaint**, run separately with no
  cross-visibility:
  - **Probe A** — the exact 10-way closed-set classifier from the Phase 2
    eval (same prompt, same model). Flags if predicted category ≠ DCM.
  - **Probe B** — a binary yes/no against a written definition of the
    category (credit counseling / debt management plan / debt
    settlement / credit repair *services*), asked without showing the
    category list or Probe A's answer. Flags on "NO." *This definition is
    narrower than CFPB's own. See [Definition gap](#definition-gap).*
- **Verdict per complaint:** both probes agree it's a misroute → high
  confidence; only one flags → uncertainty band; neither flags → belongs.

## Results

| | count | % of 504 |
|---|---|---|
| **Misroute — both probes agree** | 281 | **55.8%** |
| Misroute — one probe only (uncertainty band) | 56 | 11.1% |
| Belongs (both probes agree) | 167 | 33.1% |

**Headline: a majority of "Debt or credit management" complaints, on the
strictest two-probe standard, don't belong in the category** — not a 44%
agreement footnote, a structural intake problem.

## Hand-inspection (10 flagged, 5 belongs — see below for the actual text)

The flagged complaints are NOT concentrated in one adjacent category the way
the original 44% finding suggested. They're heterogeneous:
- FCRA credit-report accuracy disputes (2 of 10) — "under FCRA 15 USC
  1681c-2... need these items blocked and removed"
- Debt collection disputes — court documents served without prior notice,
  wrongful interest charges
- Fraud/scam complaints — fake reviews from a loan company, a fraudulent
  lease opened via identity theft
- Mortgage servicing dispute (partial claim processing)
- Account-service complaints — a bank refund delay, a solar-financing
  installation dispute

The "belongs" sample checked out clean: Freedom Debt Relief, National Debt
Relief, Bay Area Credit — genuine debt-settlement/credit-repair service
complaints matching CFPB's own definition.

**Revised interpretation:** "Debt or credit management" isn't absorbing one
specific neighboring category (debt collection) — it functions as a general
catch-all for financial complaints that don't fit cleanly elsewhere. That's a
different, more actionable finding than the original sample suggested, and
only visible at full-census scale.

## Blind precision audit (human-adjudicated)

The hand-inspection above was 15 cases the author chose after seeing the probe
verdicts. The precision audit replaces it with a blind check: a stratified
random sample of 60 complaints (seed fixed in `precision_audit/build_sheet.py`),
shuffled and relabeled C01–C60 so the labeler can't tell which bucket a case
came from, labeled `belongs` / `misroute` against CFPB's four sub-products
**before** the answer key was opened. Full output:
[`precision_audit/results.md`](precision_audit/results.md).

| Probe bucket (census size) | Sampled | Human: real misroute | Rate (95% Wilson CI) |
|---|---|---|---|
| Misroute, both probes (281) | 35 | **35** | **100%** (90–100%) |
| Misroute, one probe (56) | 10 | 8 | 80% (49–94%) |
| Belongs, both probes (167) | 15 | 3 | 20% (7–45%) |

**What it shows:**

1. **The flags are right.** Every complaint both probes flagged was a misroute
   to a human reading the full narrative: 35/35, CI lower bound 90%. The 55.8%
   is not inflated by probe false positives.
2. **The definition gap didn't bite in this sample.** None of the 35 flagged
   cases turned out to be a foreclosure-avoidance or student-loan-relief
   company, the false flags the narrower probe definition could have produced
   (see *Definition gap*).
3. **55.8% is a floor, not the answer.** The probes *missed* misroutes: 3 of 15
   in the "belongs" bucket and 8 of 10 in the one-probe band were misroutes to
   the human. Flag recall on the sample is 76% (35/46). Weighting each bucket's
   human rate by its census size gives a **stratified estimate of ~71%
   (359/504)**, with a conservative range of **58–81%** from the bucket CIs.
   The "majority misrouted" headline holds at every point in that range.

**Limits of this audit:**

- **One adjudicator, and it's the author.** I wrote the hypothesis and the
  labeling rule, so confirmation bias is possible even with verdicts hidden. A
  second independent labeler (and an agreement score) is the next step before
  this number justifies a budget ask.
- **Small strata.** The two smaller buckets drive the 58–81% width; the
  both-probe bucket is the only one tight enough to call precise.
- **Hard-case rule applied:** a scam relief seller still `belongs` (C03, C04,
  C11, C19, C56): CFPB files by what the company claims to sell. A
  collector or bureau that upsells "dispute" services (C46, C59) is a
  `misroute`, by the relief-seller vs. holder/bureau test.
- **Narrative-only population**, as with the census itself.

## Definition gap

*Found 2026-11-22 while preparing the blind precision audit, before any case
was labeled.*

CFPB's complaint form lists four sub-products under "Debt or credit
management": credit repair services, debt settlement, **mortgage modification
or foreclosure avoidance**, and **student loan debt relief**. Probe B's prompt
covered the first two (plus credit counseling / debt management plans) and left
out the last two. A complaint about a foreclosure-rescue or student-loan
"forgiveness" company is a legitimate member of this category, but Probe B
would answer "NO" and the complaint could be counted as a misroute.

**Size of the exposure:** of the 281 both-probe misroutes, 28 had Probe A
predicting *Mortgage* (24) or *Student loan* (4). That's where these false
flags would sit. Not all 28 are relief companies; many are ordinary servicer
disputes, which really are misroutes. Worst case, if every one of them was a
relief company, the strict figure falls from 55.8% to 50.2% (253/504). The
"majority" headline is plausible but no longer assumed.

**Outcome (2026-11-22):** the blind audit found no such false flags. All 35
sampled both-probe flags were real misroutes under the four-sub-product rule.
See *Blind precision audit* above.

**What changed:** the blind audit's labeling rule now uses CFPB's four
sub-products, with an explicit relief-seller vs. lender/servicer test
(`precision_audit/LABELING_SHEET.md`). Flag precision is therefore measured
against the official taxonomy, so any probe false-positives from this gap show
up in the certified number instead of being baked into it.

## Recommendation

- This is no longer a "flag for review" finding — at 55.8%+ misroute, DCM
  needs an intake-form redesign (a "what's this complaint about" branch
  question), not a downstream ML classifier patching over a broken taxonomy.
- The FCRA-dispute and fraud-complaint clusters suggest two concrete new
  category options are missing from intake, not just a debt-collection
  branch as originally hypothesized.
- The blind precision audit is done (100% flag precision, single
  adjudicator). Before an actual taxonomy change, add a second independent
  labeler and report inter-rater agreement.
