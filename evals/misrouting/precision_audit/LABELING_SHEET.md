# Precision Audit — Labeling Sheet

**Rule.** `belongs` = the complaint is about a *third-party company selling
relief* from a debt or credit problem, and the gripe is about that service.
That's CFPB's four sub-products for this category (complaint form, Oct 2026):

- **Credit repair services**
- **Debt settlement** (debt relief / consolidation programs; credit counseling
  and debt management plans count here too)
- **Mortgage modification or foreclosure avoidance**: a company offering to get
  a loan modified or stop a foreclosure. *Not* the mortgage lender or servicer.
- **Student loan debt relief**: a company offering forgiveness or consolidation
  help. *Not* the student loan servicer.

`misroute` = the real subject is anything else (credit-report/FCRA dispute, debt
collection, fraud/identity theft, bank/card/account issue, a lender or servicer's
own handling of a loan, etc.), even when debt or credit is involved.

**The one-question test:** is the company being complained about *selling relief*
from the debt, or is it the company that *holds, services, collects, or reports*
the debt? Relief seller → `belongs`. Everyone else → `misroute`.

> **Rule revised 2026-11-22, before any case was labeled.** The original rule
> (and Probe B's prompt) left out two of CFPB's four sub-products: mortgage
> modification / foreclosure avoidance and student loan debt relief. Labeling
> against the official taxonomy means the audit measures the probes against
> CFPB's definition, not against the probes' own narrower one. See
> `../README.md` → *Definition gap*.

**Hard-case rule (decide once, apply consistently):** a debt-settlement/relief
company that turns out to be a *scam* — is it a debt-management-service complaint
(belongs) or a fraud complaint (misroute)? Pick one, note it below, stick to it.

Fill each blank with `belongs` or `misroute`. Then transfer to
`adjudication_sheet.csv`'s LABEL column and run `score.py`.
(One-line reminders of each case's gist are here so you don't have to keep the
CSV open alongside. **Label on the full narrative, not the gist.** The gists were
AI-written and some already lean toward a category; treat them as a reminder of
which case is which, nothing more.)

Hard-case rule as applied in the labels: a scam relief seller still `belongs` (CFPB files by what the company claims to sell). A collector or bureau upselling "dispute" services is a `misroute`.

---

C01 → misroute     FCRA "block and remove from my report"
C02 → belongs      Credit Saint — credit-repair company, poor service
C03 → belongs      "New Education Relief" debt-relief — scam / SSN access
C04 → belongs      Consumer Credit Counseling Foundation — won't cancel
C05 → misroute     receiving checks, fraud confirmed, reimbursement
C06 → belongs      Beyond Finance — debt-settlement account mismanaged
C07 → belongs      ClearOne Advantage — debt-settlement program
C08 → misroute     can't reach TransUnion to report fraud
C09 → misroute     TransUnion rep told me to file with FTC
C10 → misroute     TekCollect — debt collection, disputed under FDCPA
C11 → belongs      Freedom Debt Relief — set up account, "scamming me"
C12 → misroute     Creedence Resource Mgmt — collection on debt not owed
C13 → misroute     IC Systems — collection on old house/utility debt
C14 → misroute     Jefferson Capital — collection, possible SSN misuse
C15 → misroute     Money Network — benefits debit card hacked
C16 → misroute     MoneyLion app — transfer error, unwanted loan
C17 → belongs      Unlimited Credit — credit-repair contract, no results
C18 → belongs      old company overcharged, sold my info
C19 → belongs      Boostify — debt-settlement, coached to commit fraud
C20 → belongs      Americor — debt-settlement, extra drafts/fees
C21 → misroute     FDCPA cease-and-desist letter to a collector
C22 → misroute     Jefferson Capital — collection on credit report
C23 → misroute     missed Target credit card payment, can I still use it
C24 → misroute     collector calling family re: Acima lease, harassment
C25 → misroute     TransUnion credit monitoring + cyber breach
C26 → misroute     Columbia Debt Recovery — collection, court-order breach
C27 → misroute     FCRA reinvestigation demand, remove from file
C28 → misroute     Experian wrong DOB, can't access credit report
C29 → misroute     bank fraud, no translator, stolen debit card funds
C30 → misroute     diffuse credit/bank "targeting" narrative
C31 → misroute     Kick Off — missed payments, won't remove negative marks
C32 → misroute     Account Resolution Services — called family, FDCPA
C33 → misroute     GoodLeap — predatory home-improvement loan
C34 → misroute     FCRA "block and remove off my report"
C35 → misroute     Midland Credit — collection/lawsuit, credit not reported
C36 → misroute     repairman stole card, fraudulent charges, card issuer
C37 → misroute     wrong payment-date info hurt my credit
C38 → misroute     "relentless calls 10 in a row" — harassment
C39 → misroute     was sick a year, they didn't close my account
C40 → belongs      $99/mo credit-repair fees, nothing done
C41 → belongs      Lexington Law — credit-repair, removed nothing
C42 → belongs      NY "fix my debt" program — no settlements, being sued
C43 → misroute     Credit Karma — inaccurate loan offers, hard pull
C44 → misroute     FCRA "unauthorized info, block and remove"
C45 → misroute     Portfolio Recovery — collection on charged-off debt
C46 → misroute     "Experian employee" upfront-fee credit scam
C47 → misroute     Pep Boys — unwanted credit inquiries after tire visit
C48 → misroute     SN Servicing — mortgage modification denied
C49 → misroute     FCRA "block and remove" (Equifax et al.)
C50 → misroute     dental-financing medical-debt FCRA/FCBA dispute
C51 → misroute     FCRA block-and-remove, statute citations
C52 → misroute     Comenity/credit-card score dropping, disputes
C53 → misroute     three fraudulent accounts, remove from credit
C54 → misroute     Capital One closed account, no payment plan
C55 → misroute     PennyMac — mortgage forbearance wrongly closed
C56 → belongs      Alleviate — debt-consolidation, hidden 25% fee, "scam"
C57 → misroute     SSN compromised, fraudulent accounts opened
C58 → misroute     Credit Karma — "karma guarantee" loan not honored
C59 → misroute     Midland Credit — collection + "dispute all" upsell
C60 → misroute     TomoBoost subscription won't cancel, billing
```
```
