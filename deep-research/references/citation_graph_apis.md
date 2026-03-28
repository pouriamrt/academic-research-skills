# Citation Graph APIs — Semantic Scholar & OpenAlex Reference

## Purpose

Reference guide for agents that need programmatic access to citation graph data. Used primarily by `concept_lineage_agent` for citation chain tracing and `bibliography_agent` for enhanced literature search.

**Both APIs are free and open access. No API key is required for basic use, but authentication increases rate limits.**

---

## 1. Semantic Scholar Academic Graph API

### Overview

| Property | Value |
|----------|-------|
| Base URL | `https://api.semanticscholar.org/graph/v1` |
| Coverage | ~214M papers |
| Auth | Optional. API key via `x-api-key` header. Request at https://www.semanticscholar.org/product/api#api-key-form |
| Rate limit (unauth) | Shared pool — may be throttled under load |
| Rate limit (auth) | 1 RPS per key (introductory tier) |
| Response format | JSON |

### Unique Strengths
- **Citation context**: `contexts` field shows the exact sentence where a paper is cited
- **Citation intent**: `intents` field classifies why a paper was cited (methodology, background, result comparison)
- **Influential citations**: `isInfluential` flag identifies citations that meaningfully engage with the paper (not just passing mentions)
- **SPECTER embeddings**: Semantic similarity vectors for finding related papers
- **TL;DR summaries**: Auto-generated paper summaries

### Paper ID Formats

The `{paper_id}` parameter accepts multiple formats:
- `DOI:10.1038/s41586-020-2649-2`
- `ARXIV:2006.10256`
- `PMID:12345678`
- `CorpusId:219792763`
- `URL:https://www.semanticscholar.org/paper/...`

### Key Endpoints

#### Paper Search (Relevance-Ranked)
```
GET /paper/search?query={query}&fields={fields}&limit={limit}&offset={offset}
```
- `fields`: Comma-separated. Key fields: `paperId,title,year,citationCount,influentialCitationCount,abstract,fieldsOfStudy,isOpenAccess,openAccessPdf`
- `publicationDateOrYear`: Filter by date range (e.g., `2020-01-01:2024-12-31`)
- `fieldsOfStudy`: Filter by field (e.g., `Computer Science`, `Education`)
- `minCitationCount`: Minimum citation threshold
- Max 1,000 results total (paginate with `offset`)

#### Paper Search (Bulk / Boolean)
```
GET /paper/search/bulk?query={query}&fields={fields}&token={token}
```
- Supports boolean: `+required`, `|optional`, `-excluded`, `"exact phrase"`, `*wildcard`
- Supports sorting: `sort=citationCount:desc`
- Returns up to 1,000 per call, 10M total via token pagination

#### Paper Details
```
GET /paper/{paper_id}?fields={fields}
```
All fields available: `paperId,corpusId,externalIds,url,title,abstract,venue,publicationVenue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,citationStyles,authors,citations,references,embedding,tldr`

#### Batch Paper Details
```
POST /paper/batch?fields={fields}
Body: { "ids": ["DOI:...", "ARXIV:...", ...] }
```
Max 500 IDs per request.

#### Forward Citations (Who Cited This Paper)
```
GET /paper/{paper_id}/citations?fields={fields}&offset={offset}&limit={limit}
```
Response includes per-citation metadata:
- `citingPaper`: The citing paper object
- `contexts`: Array of citation sentences (exact text where this paper is mentioned)
- `intents`: Why it was cited (`methodology`, `background`, `result`)
- `isInfluential`: Boolean — meaningful engagement vs. passing mention

Max 1,000 per page. Paginate with `offset`.

#### Backward References (Papers Cited By This Paper)
```
GET /paper/{paper_id}/references?fields={fields}&offset={offset}&limit={limit}
```
Same per-reference metadata as citations (contexts, intents, isInfluential).

#### Author Search
```
GET /author/search?query={name}&fields={fields}
```
Author fields: `authorId,name,affiliations,homepage,paperCount,citationCount,hIndex`

#### Author's Papers
```
GET /author/{author_id}/papers?fields={fields}&offset={offset}&limit={limit}
```

### Citation Chain Tracing Pattern

```
To trace the lineage of Concept X:

1. Find the seminal paper:
   GET /paper/search?query="concept X" original&fields=title,year,citationCount&limit=5
   → Take the oldest, most-cited result

2. Get its forward citations (who built on it):
   GET /paper/{seminal_id}/citations?fields=title,year,citationCount,isInfluential,intents,contexts&limit=100
   → Filter: isInfluential=true
   → Sort by year to see temporal evolution

3. Get its backward references (what it built on):
   GET /paper/{seminal_id}/references?fields=title,year,citationCount,isInfluential&limit=50
   → Identifies the intellectual ancestors

4. For key challengers/refiners, repeat steps 2-3 one level deeper:
   GET /paper/{challenger_id}/citations?fields=title,year,citationCount,isInfluential&limit=50
   → Shows whether the challenge was adopted or ignored by the field

Budget: ~10-15 API calls per concept (1 search + 2-3 citation/reference calls + 2-3 deeper dives)
```

---

## 2. OpenAlex API

### Overview

| Property | Value |
|----------|-------|
| Base URL | `https://api.openalex.org` |
| Coverage | ~250M+ works |
| Auth | Optional. Free API key from https://openalex.org (passed as `?api_key=YOUR_KEY`) |
| Rate limit | 100 RPS; daily credit-based limits (free daily allowance sufficient for research) |
| Response format | JSON |

### Unique Strengths
- **Topic hierarchy**: 4-level classification (domain → field → subfield → topic) for any work
- **Institution and funder data**: 110K+ institutions, 35K+ funders linked to works
- **Broader coverage**: Includes more non-English, grey literature, and preprints
- **Powerful filtering**: Complex filter expressions with boolean logic
- **Bulk data access**: Complete database snapshot available for download
- **FWCI**: Field-Weighted Citation Impact for normalized citation comparison

### Key Endpoints

#### Works by DOI
```
GET /works/https://doi.org/{doi}?select={fields}
```
Or filter-based:
```
GET /works?filter=doi:{doi}&select={fields}
```

#### Works Search
```
GET /works?search={query}&per_page={n}&select={fields}
```
- `select`: Comma-separated fields to return (reduces response size)
- `sort`: e.g., `cited_by_count:desc`, `publication_date:desc`
- `per_page`: Max 200

#### Forward Citations (Papers That Cite Work X)
```
GET /works?filter=cites:{openalex_id}&sort=cited_by_count:desc&per_page=50
```
**Note**: `cites:X` means "find papers whose reference list includes X" — i.e., forward citations of X.

#### Backward References (Papers Cited BY Work X)
```
GET /works/{id}?select=referenced_works
```
Returns an array of OpenAlex IDs. Resolve in batch:
```
GET /works?filter=openalex:{id1}|{id2}|{id3}&select=id,title,publication_date,cited_by_count
```

#### Author Search
```
GET /authors?search={name}&select=id,display_name,works_count,cited_by_count,h_index
```

#### Topic/Concept Exploration
```
GET /works?filter=primary_topic.id:{topic_id}&sort=cited_by_count:desc&per_page=20
```

### Key Work Fields

| Field | Description |
|-------|-------------|
| `id` | OpenAlex ID (e.g., `W3035965352`) |
| `doi` | DOI URL |
| `title` | Paper title |
| `publication_date` | ISO date |
| `publication_year` | Year integer |
| `cited_by_count` | Total forward citations |
| `referenced_works` | Array of OpenAlex IDs this paper cites |
| `referenced_works_count` | Count of references |
| `primary_topic` | 4-level hierarchy: `{domain, field, subfield, topic}` |
| `is_retracted` | Boolean — retraction status |
| `fwci` | Field-Weighted Citation Impact |
| `citation_normalized_percentile` | Citation percentile within field+year |
| `counts_by_year` | Year-by-year citation counts |
| `authorships` | Authors with institution affiliations |
| `open_access` | `{is_oa, oa_status, oa_url}` |

### Filter Semantics (Critical)

| Filter | Meaning | Use Case |
|--------|---------|----------|
| `cites:W123` | Papers whose reference list includes W123 | Forward citations (who cited this?) |
| `cited_by:W123` | Papers that appear in W123's reference list | Backward references (what does this cite?) |
| `authorships.author.id:A123` | Papers by a specific author | Author bibliography |
| `primary_topic.id:T123` | Papers on a specific topic | Topic exploration |
| `publication_year:2020-2024` | Year range filter | Temporal filtering |
| `cited_by_count:>100` | Citation count threshold | Finding influential papers |
| `is_retracted:false` | Exclude retracted papers | Quality filtering |

Combine filters with `,` (AND) or `|` (OR within same field). Negate with `!`.

---

## 3. Recommended Combined Workflow

### For Concept Lineage Tracing

```
Step 1: Identify seminal paper
  └── Semantic Scholar /paper/search (better relevance ranking for specific concepts)

Step 2: Get citation metrics
  ├── Semantic Scholar: influentialCitationCount, isInfluential per citation
  └── OpenAlex: fwci, citation_normalized_percentile, counts_by_year

Step 3: Trace forward citations
  ├── Semantic Scholar /paper/{id}/citations (rich: contexts, intents, isInfluential)
  └── OpenAlex /works?filter=cites:{id} (broad: better coverage, sortable)

Step 4: Classify citation purpose
  └── Semantic Scholar only: intents field + contexts field

Step 5: Enrich with institutional/topic data
  └── OpenAlex only: authorships.institutions, primary_topic hierarchy, fwci
```

### For Enhanced Bibliography Search

```
Step 1: Broad discovery
  └── OpenAlex /works?search={query} (250M+ works, powerful filters)

Step 2: Academic-specific search
  └── Semantic Scholar /paper/search (better relevance, SPECTER-based)

Step 3: Verify and enrich
  ├── Semantic Scholar: tldr summary, isOpenAccess, openAccessPdf
  └── OpenAlex: is_retracted, fwci, primary_topic, authorships

Step 4: Citation context
  └── Semantic Scholar only: how each paper cites key works (contexts, intents)
```

---

## 4. Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `429 Too Many Requests` | Rate limit exceeded | Exponential backoff: wait 2s, 4s, 8s, then skip |
| `404 Not Found` | Paper not in database | Try alternative ID format (DOI → title search) |
| `500 / 503` | API temporarily down | Retry once after 5s, then fall back to other API |
| Timeout (>10s) | Network issue | Retry once, then fall back |
| Empty results | Paper not indexed | Try the other API; if both empty, use WebSearch |

### Graceful Degradation Priority

```
1. Both APIs available → Full citation graph analysis
2. Only Semantic Scholar → Citation chain with context/intent data (no FWCI/topic hierarchy)
3. Only OpenAlex → Citation chain with bibliometric data (no citation context/intent)
4. Neither API available → WebSearch + bibliography-based inference
   → Add prominent disclaimer in output
```

---

## 5. Rate Budget Guidelines

| Task | Estimated API Calls | Target | Budget Cap |
|------|-------------------|--------|-----------|
| Single concept lineage trace | 10-15 calls | ≤2 min | Part of 50-call agent budget |
| Full lineage report (3-5 concepts) | 30-50 calls | ≤8 min | 50 calls (concept_lineage_agent) |
| Enhanced bibliography search (15 papers) | 15-20 calls | ≤3 min | 50 calls (bibliography_agent) |
| Paper verification (DOI check) | 1 call per paper | Negligible | Part of agent budget |

**Budget per agent per invocation**: 50 API calls across both services. If approaching limit, prioritize remaining concepts by centrality rank. When `concept_lineage_agent` and `bibliography_agent` run in the same pipeline session, each agent has its own 50-call budget (100 total across both agents).
