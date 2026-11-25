# CFPB Servicer Benchmarking — Within-Category Complaint Methodology

> A naive portfolio-wide relief-rate comparison flags the wrong company. Using
> 391,728 real CA consumer complaints (Jan 2024–Apr 2025), this project finds why,
> and what to compare against instead. It also evaluates whether an LLM is safe to
> use in complaint triage, and in what role: see
> [AI evaluation & risk](#ai-evaluation--risk-should-an-llm-triage-these-complaints).

**Deliverables:** [Executive Brief — misrouting](docs/05_executive_brief.md) · [Intake Redesign (as-is/to-be)](docs/06_intake_redesign_flow.md) · [Decision Memo](docs/01_decision_memo.md) · [BRD](docs/02_brd.md) · [KPI Dictionary](docs/03_kpi_dictionary.md) · [Data Notes](docs/04_data_notes.md) · [Live Dashboard](https://public.tableau.com/app/profile/sez.ozrn/viz/CFPBCAServicerBenchmarking/Dashboard1)

**Stack:** Python (API ingestion) · DuckDB / SQL (analysis) · Tableau (dashboard) · Claude + Copilot (AI-assisted)

---

## The 3-minute version

**Problem.** Companies handling consumer financial complaints are often benchmarked
against a single portfolio-wide "relief rate" target. Does that comparison actually
identify real service-quality problems, or does it just reflect which product a
company happens to service?

**Approach.** Pulled 391,728 real CFPB consumer complaints for California (Jan
2024–Apr 2025) via CFPB's public API, cleaned and scoped the data (excluded credit
reporting — 84.9% of volume, a separate workflow), and analyzed relief and
timely-response rates by product and by company using SQL (DuckDB).

**Findings.**
1. Relief rate varies **14x by product alone** — 2.6% (student loan) to 36.8%
   (credit card) — before any company-level effect is considered.
2. A naive company-vs-portfolio-average comparison flagged **MOHELA** as a poor
   performer (2.8% relief vs. 23.4% portfolio average). That's a false positive:
   MOHELA is roughly mid-pack **within its own product category** — 4 of 8 major
   student loan servicers show 0.0% relief.
3. The real, evidence-backed outlier is **EdFinancial Services**: 50.7% timely
   response, about half of every peer servicer (88–100%), while still granting 0%
   relief.
4. **AI-assisted feasibility check, then a full-census follow-up.** An LLM
   classification eval on 500 narratives (79.8% overall agreement with official
   categories) flagged one category — "Debt or credit management" — as an
   outlier at 44% agreement, pointing at an intake-labeling problem rather than
   model error. A full-census audit of that category (504 complaints, two
   independent probes) then sized it: **55.8% of the category doesn't belong in
   it** — and a blind human precision audit confirmed the flags (35/35, 100%
   precision, CI 90–100%) and showed 55.8% is a floor (stratified estimate
   ~71%). Hand-inspection showed it acts as a general catch-all (FCRA
   disputes, fraud, mortgage servicing), not a debt-collection dump as the
   sample first suggested. Method + results:
   [evals/misrouting/](evals/misrouting/README.md) · exec-facing version:
   [docs/05_executive_brief.md](docs/05_executive_brief.md).

**Recommendation.** Replace portfolio-wide comparison with within-product-category
benchmarking (KPI-04). Pilot on the student loan category (8 servicers, already
scoped) for one quarter before extending. Full case in the
[decision memo](docs/01_decision_memo.md).

---

## AI evaluation & risk: should an LLM triage these complaints?

The BRD's future state proposed AI-assisted complaint triage. Before recommending
it, this repo evaluates the model the way a deployment decision needs: by where it
fails and why, not just a headline accuracy number. The evals changed the
recommendation, which is the point of running them.

| AI risk | How it was tested | What it changed |
|---|---|---|
| **A headline accuracy hides weak segments** | 500-narrative eval, stratified 50 per category ([evals/](evals/README.md)) | 79.8% overall, but **44%–94% by category**. No single "the model is X% accurate" claim; per-category validation is a deployment gate |
| **The ground truth is wrong, not the model** | Disagreements hand-inspected against CFPB's own category definitions | In the 44% category, the model was often *more* right than the official label: the eval exposed label noise in the reference data |
| **One model's verdict is over-trusted** | Full-census audit (504 complaints) with two independent probes that never see each other's answers, plus an uncertainty band where they disagree ([evals/misrouting/](evals/misrouting/README.md)) | **55.8% misroute** on the strict both-probes standard, 66.9% including the band. Reported as a range, not a point |
| **The sample isn't the production population** | Narrative opt-in rates measured per product (25.3%–73.1%) | Results framed as a feasibility signal, not a deployment accuracy estimate |
| **An unvalidated model drives a real-world change** | Blind human precision audit with a written labeling rule and a hard-case rule ([precision_audit/](evals/misrouting/precision_audit/)) | Taxonomy change gated on human adjudication. **Done: 35/35 both-probe flags confirmed** (CI 90–100%); 55.8% is a floor, stratified estimate ~71% ([results](evals/misrouting/precision_audit/results.md)) |
| **Too much autonomy** | Error profile above | Recommended role: a **QA layer that flags disagreements for human review**, not an autonomous router that reassigns categories |

---

## Dashboard

![CFPB CA Servicer Benchmarking dashboard — relief rate by product and student-loan servicer scorecard](dashboard/screenshots/01_dashboard_full.png)

*[Explore the interactive version on Tableau Public →](https://public.tableau.com/app/profile/sez.ozrn/viz/CFPBCAServicerBenchmarking/Dashboard1)*

---

## Repo map

| Path | What it is |
|---|---|
| `docs/01_decision_memo.md` | 1-page recommendation, with the corrected finding and why the naive comparison failed |
| `docs/02_brd.md` | Requirements for a within-category servicer scorecard |
| `docs/03_kpi_dictionary.md` | 4 KPIs, including the mandatory product-stratification rule for relief rate |
| `docs/04_data_notes.md` | 6 real API/ingestion bugs found (incl. a currently-open upstream CFPB bug) + 4 data-quality findings |
| `sql/05_dq_*.sql` | Data quality checks: coverage, duplicates, taxonomy drift, narrative bias |
| `sql/10_*.sql` | Core analysis: routing/timeliness, relief outcomes (findings F1–F3) |
| `sql/20_kpi_within_category_deviation.sql` | KPI-04 implemented — the within-category scorecard the memo recommends, with the verified flag output in the header |
| `src/ingest.py` | CA-scoped CFPB API ingestion (search_after pagination, documented API workarounds) |
| `evals/` | LLM classification eval: stratified sample, per-category agreement, confusion breakdown |
| `evals/misrouting/` | Full-census misrouting audit with two independent probes and an uncertainty band |
| `evals/misrouting/precision_audit/` | Blind human-adjudication harness that gates any taxonomy change |

## A note on how this was built

**This is a self-directed analysis on public data.** It was not commissioned by
CFPB, any servicer, or any employer. The stakeholder roles in the decision memo
and BRD (VP of Consumer Response Operations, compliance analyst, etc.) are
illustrative — they define who the deliverables are *written for*, not a real
engagement. The data, the bugs found, and the findings are real.

This project hit a real methodological trap and corrected course in the open rather
than quietly fixing it: an early cut of the analysis compared each company's relief
rate against a pooled "all other companies" average, which flagged MOHELA as an
outlier. Checking that finding against product-level base rates (not just
company-level) showed the comparison was confounded — student loan servicing is
structurally low-relief across the board, not specific to MOHELA. The corrected
analysis, which controls for product category, is what's reflected in the memo and
BRD. The near-miss itself is documented in `docs/03_kpi_dictionary.md`'s change log
and `docs/04_data_notes.md`, since knowing what comparison NOT to make is as much a
BA finding as the final recommendation.

## Reproducing

```bash
pip install -r requirements.txt
# To approximate the snapshot analyzed here (391,728 rows). The original pull
# targeted a full 2 years and was stopped deliberately at 2025-04-13 — see
# data notes, ingestion issue #5:
python src/ingest.py --from 2024-01-01 --to 2025-04-13 --state CA --db data/complaints.db --snapshot my-pull
# create the analysis-scope view first, then run the numbered queries in order:
duckdb data/complaints.db < sql/00_views.sql
# then sql/05_*.sql, sql/10_*.sql, sql/20_*.sql against data/complaints.db (DuckDB)
```

Note: a wider `--to` date will pull more data but won't reproduce the row
counts in this analysis, and sustained pulls get heavily throttled by the API
(see data notes, ingestion issue #5 — the original 15.4-month pull took ~9h40m
wall-clock). The CFPB database also updates daily, so even the exact command
above will return slightly different rows over time as new complaints for the
window are published.

## Data source & caveats

CFPB Consumer Complaint Database (public, updated daily):
https://www.consumerfinance.gov/data-research/consumer-complaints/search/

- **CA only** (deliberate scope decision — see data notes)
- **Jan 2024–Apr 2025**, not the full 2 years (stopped deliberately after a 15.4-month
  pull rather than burn ~6 more hours for diminishing-returns data — see data notes)
- Complaints ≠ incidents: this measures who complained to a federal regulator, not
  underlying service-failure rates
- Full caveat list in [docs/04_data_notes.md](docs/04_data_notes.md)
