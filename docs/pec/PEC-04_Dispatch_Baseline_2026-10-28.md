# PEC-04 — Dispatch (formerly Job Radar) · Baseline

| Field | Value |
|---|---|
| PEC ID / version | PEC-04 · protocol PEC v0.2 · report v1.0 |
| Cut-off | 2026-10-28 11:20 Europe/Berlin |
| Commit evaluated | `0184b2e` (main) — diagnostic baseline. The rename commit that archives this file is recorded in §8 |
| Prepared by | Claude (reporting role), read-only diagnostic + changes explicitly authorised by Jorge on 28.10 (listed in §1.3) |
| GitHub copy | `docs/pec/PEC-04_Dispatch_Baseline_2026-10-28.md` in `Jorgeaguilarsalas/job-radar` |
| Drive copy | `PROJECTS / Dispatch / PEC / PEC-04_Dispatch_Baseline_2026-10-28` |

---

## 1. Project Snapshot

### 1.1 Identity
- **Name:** Dispatch (renamed from "Job Radar" on 28.10.2026 — the system no longer detects vacancies; it dispatches and tracks applications).
- **Purpose (stated by Jorge, 28.10):** continuously improve the job search through analysis and methodology, and through document creation. Every method and specification is written into the protocol; as much data as possible is captured to improve the system and its results.
- **Components today:**
  1. **App** — static PWA (single `index.html`) on GitHub Pages, Google Sign-In, reads/writes the Google Sheet. Tabs: Home · Jobs · Insights · Docs · Report.
  2. **Data store** — Google Sheet `1vphtmlNtnpN0f8phSdmwOMa8pG4Eivfl9ryBv9V8HQo` (Sheet1, columns A–Q used by the app; R `jd_url` present but unused).
  3. **Method layer** — JD Analysis Protocol (8 dimensions, 0–2 each, max 16), CV template, mandatory application workflow (JD → CV → Drive → Sheet). Stored in Claude project memory; a v2.0 text export exists in Drive.
  4. **Document layer** — per-application JD Google Doc + CV PDF (+ cover letter / form answers) in the Drive applications folder.
  5. **Analysis** — scheduled task "Job Radar – Weekly Analysis" (Mondays 07:43 Berlin, first run 2026-11-02).
- **Repository:** `Jorgeaguilarsalas/job-radar`, single branch `main`, public. 15 commits (26.10–28.10 incl. the rename).
- **Live URL:** https://jorgeaguilarsalas.github.io/job-radar (URL unchanged by the rename).
- **Drive:** `CARRERA — Job Applications` (Setup Protocol + stale index.html copy, 26.10) · applications folder (Sheet, JD docs, CV PDFs) · `PROJECTS / Dispatch / PEC` (this report).

### 1.2 Status ladder (PLANNED → BUILT → DEPLOYED → ACCEPTED → RELEASED)

| Item | Status | Evidence |
|---|---|---|
| Core tracker (Jobs, Docs, Report, PDF export) | DEPLOYED · in daily use | commits `ac6cb78`…`82a34dc`; used daily by Jorge |
| Insights tab (funnel, KPIs) | DEPLOYED | `4252498` |
| Bottom nav + profile sheet | DEPLOYED | `25e4885` |
| Home tab + per-status lists + follow-up filter | DEPLOYED · informally accepted (Jorge: "listo", 28.10) | `0184b2e` |
| Rename to Dispatch + new icon | BUILT → DEPLOYED with this archive commit | §8 |
| Formal acceptance criteria for any item | MISSING | no acceptance record exists |

- **Last accepted milestone:** none formally defined. The Home tab is the only item with an explicit user confirmation.
- **Next milestone / acceptance criteria:** not defined (MISSING). Proposed in §4.
- **Original target date / forecast:** none exist. No delay can be stated.

### 1.3 Changes made on 28.10 with Jorge's explicit authorisation
1. Home tab shipped (`0184b2e`).
2. **Parallel system removed:** a second "Job Radar" (claude.ai artifact with its own database) was deleted. Before deletion, its 20 records were compared with the Sheet: 4 already existed, **16 were migrated** to the Sheet (rows 204–219), incl. one already-sent application (Shiftmove, PM B2B SaaS, with CV + cover-letter links; send date estimated = 27.10, flagged `datumGeschaetzt=TRUE`).
3. **Both daily vacancy-search tasks deleted** ("Jobradar" 07:00 weekdays → wrote to the deleted artifact; "Job Radar – Daily Recommendations" 07:30 → wrote to the Sheet with a wrong 60–80K salary band). Jorge does not want vacancy alerts.
4. Weekly Analysis kept (Jorge: needed to update vacancy evaluation).
5. Rename to Dispatch.

---

## 2. Evidence Coverage

| Dimension | Status | Source & location | Last update | Missing | Minimal adjustment |
|---|---|---|---|---|---|
| Time & effort | PARTIAL | Commit timestamps (git log); chat sessions | 28.10 | Human hours, agent run time, waits — none recorded | Log session time per work block (existing Portfolio time-tracking sheet pattern) |
| Errors & rework | PARTIAL | git log (dedup removed `dbe3938` then restored `741cf9e`; 3 redesigns in 2 days); session incidents 27–28.10: invalid status `offen` hid a row; duplicate row appended then cleared; Sheets API per-minute quota errors (reads & writes); 1-byte-corrupt Drive PDF upload; parallel data store | 28.10 | No incident log | `docs/INCIDENTS.md` (one line per incident: date, cause, fix) |
| Costs | PARTIAL | GitHub Pages, Sheets API, Drive: no cost (measured: free tier). Scheduled tasks run on Claude usage | 28.10 | AI usage per task/run not attributed | Record run count per task; attribute usage when the platform exposes it |
| Quality | MISSING | No tests, no CI beyond Pages build, no acceptance criteria. Browser test of Home (sample data, mobile+desktop, 0 JS errors) run 28.10 but not archived | 28.10 | Test evidence, acceptance records | Acceptance line per change in CHANGELOG |
| Decisions | PARTIAL | Setup Protocol (architecture, security); commit messages; this report §1.3 | 28.10 | No ADRs | Short ADRs in `docs/adr/` for: single data store, no alerts, rename |
| Replicability | PARTIAL | Drive "Job Radar — Setup Protocol" (6 install steps) | 26.10 | Outdated: no `espera`, no Home, no `jd_url`, old name | Move setup guide into repo README; Drive links to it |
| Results | PARTIAL | Insights tab; Drive "Job Radar — Análisis de Conversión (Oct 2026)" (one-off) | 26.10 | No recurring measurement until Weekly Analysis runs (02.11) | Data-capture spec (§3.2) |

---

## 3. Product Performance

### 3.1 Metric inventory
Vacancy detection was removed on 28.10; detection metrics are therefore NOT APPLICABLE going forward. Vacancies now enter only when Jorge brings a JD.

| Metric | Status |
|---|---|
| Vacancies evaluated (JDs run through the protocol) | NOT CAPTURED — evaluations live only in chat; SKIP decisions are not recorded |
| Vacancies relevant to profile (score / recommendation) | PARTIAL — score in free-text `notiz` for some rows; not per dimension, not structured |
| Precision of evaluation (score vs outcome) | UNKNOWN — no link between protocol score and response/interview |
| Duplicates | PARTIAL — 48 duplicate IDs in Sheet (app hides them; data not clean) |
| Listing freshness / link validity | NOT IMPLEMENTED — link stored in a minority of rows |
| Time from publication to detection | NOT APPLICABLE (no detection) |
| Time saved | UNKNOWN |
| Fit-explanation quality | PARTIAL — explanations in chat and JD docs, not evaluated |
| Applications & outcomes | IMPLEMENTED — status, dates, Insights funnel, Jobcenter report |
| Document production (CV/JD per application) | PARTIAL — complete for 27.10 onward (JD doc + CV PDF + Sheet link); gaps before (Knowunity & SafeDriver CVs, 4 JDs not stored) |

**Snapshot (Sheet, before migration, 28.10):** 202 rows with ID, 154 unique. Unique statuses: absage 139 · verschickt 10 · pruefen 4 · espera 1 · interview 0 (interviews that ended in rejection were closed as `absage`, so interview history is lost in the status field). After migration: +16 rows (15 `pruefen`, 1 `verschickt`).

### 3.2 Data-capture specification (new — implements Jorge's 28.10 instruction)
Goal: every application produces enough structured data to learn which roles, channels, documents and messages convert. Captured in the existing Sheet without breaking the app (the app reads A–Q only; extra columns are safe).

**Per JD evaluated (including SKIP/REVIEW not pursued)** — one row, status `verworfen` if not pursued:
- protocol score total and D1–D8, recommendation, hard filter fired (if any), CV cluster
- salary stated / estimated; applicants count; posting age; source; contact identified (Y/N)

**Per application sent:**
- channel (portal / email / LinkedIn / direct to founder or recruiter), direct-contact message sent (Y/N, date)
- salary expectation entered
- document set: CV cluster + language + CV file link, cover letter (Y/N), form answers (Y/N), motivation note (Y/N)
- referral / boomerang / 1st-degree contact (Y/N)

**Per outcome event (append, never overwrite):**
- date of first response, response type (rejection / screen / interview / ghosted after N days)
- interview rounds reached (count) and stage of exit
- rejection reason if given; feedback received (Y/N)

**Derived weekly (Weekly Analysis):** conversion by score band, by cluster, by channel, by direct-contact, by salary band, by language; median days to first response; ghost rate after 14 and 30 days.

Until new columns are approved, the same fields are appended to `notiz` as one machine-readable line:
`DSP|score=14|d=2,2,2,1,2,2,2,1|rec=APPLY_P|cluster=HeadOps|sal_ask=—|channel=portal|direct=Y|docs=CV-EN,note|`

---

## 4. Completion Outlook

1. **To close the next milestone ("M1 — Single source of truth & measurable pipeline", proposed):**
   - Data model: add structured columns per §3.2 (or adopt the `DSP|` line) — PLANNED
   - Clean the 48 duplicate IDs in the Sheet (keep newest) — PLANNED
   - Restore interview history (`interview` / rounds) for closed processes — PLANNED
   - Point Weekly Analysis at the JD protocol (it still targets the deleted daily tasks and writes to a memory file that does not exist) — BLOCKED (see 2)
   - README + CHANGELOG with acceptance lines — PLANNED
   - Acceptance criteria (proposal): app shows every Sheet row once; every application from M1 on has score, cluster, channel and docs captured; Weekly Analysis produces the conversion cuts in §3.2.
2. **Blocked:** editing scheduled tasks from this session is denied by the platform's safety layer (attempted 28.10). Needs Jorge to approve or edit the task himself.
3. **Critical dependencies:** Google OAuth client (Cloud project), Sheets API per-minute quota (caused failed writes on 27–28.10), GitHub Pages, Drive editor access of the work account to the personal-account folders.
4. **Baseline date / estimate:** none exist. No percentages or delays stated.
5. **Could extend the project:** schema change + backfill of historical rows; data cleaning; repeated UI iterations without acceptance criteria.
6. **Detectable daily:** GitHub commits & Pages builds; Sheet `modifiedTime` and row count; Drive files created in the applications folder; Weekly Analysis `last_run`.
7. **Executed tests not archived:** yes — browser tests of 28.10.
8. **Stale sources that could mislead an analyst:**
   - Drive `job-radar — index.html` (26.10) — 15 commits behind; do not use.
   - Drive "Job Radar — Setup Protocol" (26.10) — outdated statuses, tabs, name.
   - Drive "Análisis de Conversión" — cites "250+ vehicles" at Nexio, not supported by CV/profile facts; treat as unverified.
   - Weekly Analysis prompt — describes daily tasks that no longer exist; targets memory file `areas/job-search.md` that does not exist.
   - "Stellenbeschreibungen — Aktive Bewerbungen" (26.10) — 4 JDs marked pending.

---

## 5. Replication Readiness

- **Reusable (built):** single-file PWA; Sheet schema A–Q; browser OAuth flow; JD Analysis Protocol structure (filters, 8 dimensions, interpretation, clusters); CV generator pattern (ReportLab, ~6 KB PDF, Drive-uploadable); application workflow checklist; Jobcenter PDF report.
- **Per-user configuration:** `SPREADSHEET_ID`, `CLIENT_ID`, `OWNER_NAME`, hard-coded `INTERESTED_IDS` list in code; OAuth authorised origin; Sheet copy; experience portfolio, hard filters, salary band and clusters in the protocol; CV fixed elements; Drive folder IDs; Kundennummer (localStorage).
- **Repeatable work:** fork repo → enable Pages → create OAuth client → copy Sheet header → set IDs → write user's protocol §A–§C and CV template → create Drive folders.
- **Unresolved:** no multi-tenant architecture (one fork + Sheet per user); public repo contains personal identifiers (no secrets); per-user cost unknown; no tests; protocol content is Jorge-specific and lives in Claude memory, not in the repo.
- **Comparison baseline for user #2:** not measurable yet — effort and cost of build #1 were not recorded (§2).

---

## 6. Evidence Gaps

| Known loss pattern | Present in Dispatch? | Minimal fix |
|---|---|---|
| Execution logs not kept | Yes — task runs only push a notification | Weekly Analysis writes its summary to a Drive doc / Sheet tab each run |
| Tests verified but not archived | Yes | Acceptance line in CHANGELOG with test date |
| Drive outdated vs GitHub | Yes — index.html copy and Setup Protocol | Replace copies with links to the repo |
| No initial estimates / rework time | Yes | Estimate + actual per work block |
| Costs not attributed | Yes | Run count per task |
| Additional: decisions & evaluations only in chat | Yes — JD evaluations and SKIPs vanish | §3.2 capture rule |

---

## 7. Three Minimal Improvements (need Jorge's authorisation)

1. **Adopt the §3.2 data capture** (start with the `DSP|` line in `notiz` today; columns later) — makes every future application a data point.
2. **Re-point Weekly Analysis** to compute the §3.2 cuts and to write results into the JD protocol's evidence section + a Drive "Dispatch — Weekly Analysis" log.
3. **Clean the data once:** remove 48 duplicate IDs; mark processes that reached interviews (rounds) so conversion can be measured.

---

## 8. Archive Status

| Copy | Location | Status |
|---|---|---|
| GitHub | `docs/pec/PEC-04_Dispatch_Baseline_2026-10-28.md` — see commit link in the Drive copy | recorded at publish time |
| Google Drive | `PROJECTS / Dispatch / PEC / PEC-04_Dispatch_Baseline_2026-10-28` | recorded at publish time |

Sync status and URLs are verified after both writes and stated in the chat reply and in the Drive copy's header.
