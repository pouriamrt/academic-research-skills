# Third-party projects

This page lists third-party projects, platforms, and services that build on, wrap,
or integrate Academic Research Skills (ARS). It also acknowledges upstream projects
whose mechanisms ARS has adapted (see **Upstream & related projects** below).

## Disclaimer

**Listing here is not an endorsement.** The entries below are community-submitted
and have **not been reviewed, tested, or verified** by the ARS maintainer. They are
operated by independent third parties, not affiliated with this project.

- Being listed here does not mean the maintainer vouches for the project's quality,
  security, privacy practices, or continued availability.
- Links may point to external platforms with their own terms, pricing, tracking, and
  data-handling policies. Read them before you sign up or upload anything.
- **Use at your own risk.** Do not paste unpublished research, personal data, or any
  confidential material into a third-party service without checking its policies first.

If you want a project *reviewed and officially recognized* by ARS (rather than merely
listed), that is a separate track — see **Getting officially recognized** below.

## How to get listed

The bar to be listed here is intentionally low, and separate from endorsement. Open an
issue or a pull request adding a row to the table. To be eligible, your project must:

1. **Credit ARS** — visibly attribute Academic Research Skills and link back to this
   repository.
2. **Describe it faithfully** — do not misrepresent what ARS is or what your project
   does with it.

That is all that is required for a listing. The maintainer may decline or remove an
entry that violates these two conditions, or that turns out to be spam, malware, or
otherwise harmful.

## Getting officially recognized

Listing on this page is *not* the same as ARS officially supporting or bundling your
integration. If you are building a platform port or a first-class integration and want
it recognized in the main README or shipped with the suite, that goes through the
**platform-ports policy** (community-maintained ports), which sets a higher bar than a
directory listing. See the Platform Port Reminder policy and open an issue to discuss.

## Listed projects

| Project | Maintainer | What it does | Link |
|---------|-----------|--------------|------|
| ClawMama | kinhunt (third party) | Hosted OpenClaw/Hermes-style agent offering a first-run trial of the Academic Research Pipeline via Telegram or WhatsApp | [Try in Telegram or WhatsApp](https://app.clawmama.run/skills/639wu5/hermes?utm_source=github&utm_medium=issue&utm_campaign=skill_outreach_academic_research_skills) |

*Columns:* **Project** name as the third party calls it · **Maintainer** the account
that submitted / operates it · **What it does** a one-line neutral description ·
**Link** where it lives. Descriptions are the submitters' own claims, restated
neutrally; the maintainer has not verified them.

## Upstream & related projects

The reverse direction: independent projects whose mechanisms ARS has adapted, with
credit recorded in the corresponding issues and pull requests. Listing here is
acknowledgement, not endorsement, and implies no affiliation.

| Project | Maintainer | Relationship | Link |
|---------|-----------|--------------|------|
| sci-ssci-skills | [@MissOrangePeel](https://github.com/MissOrangePeel) (Yila-AI) | Origin of the claim-strength ladder + deterministic invariant-checking mechanism shape adapted into the v3.19.0 revision-round claim-drift guards (#569 / #570, PR [#571](https://github.com/Imbad0202/academic-research-skills/pull/571)) | [Yila-AI/sci-ssci-skills](https://github.com/Yila-AI/sci-ssci-skills) |
| vibecoded-design-tells | [@jcarterjohnson](https://github.com/jcarterjohnson) | **Vendored code**, not merely an adapted mechanism: `scripts/check_prose_tells.py` (v3.22.0) is a port of the four copy rules in that project's `devibe_scan.py`, reaching ARS via `humanizer-stack`. MIT — see the obligation note below | [jcarterjohnson/vibecoded-design-tells](https://github.com/jcarterjohnson/vibecoded-design-tells) |
| humanizer-stack | [@jensheitmann](https://github.com/jensheitmann) | Intermediate packaging the port travelled through: narrowed the rules to prose files and added the standalone CLI that `check_prose_tells.py` inherits. MIT | — |

### MIT obligation on `scripts/check_prose_tells.py`

This is a license condition, not a courtesy. The file carries a header naming both
upstreams, and that header must survive edits and redistribution. The four rule
patterns (`copy-em-dash`, `copy-antithesis`, `hype-copy`, `copy-servile`) are the
substance taken; ARS additions on top — fenced-block tracking, `--exclude-quotes`,
the test suite — are original work under this repository's license.

**Not vendored, deliberately.** `humanizer-stack`'s `skills/humanizer/SKILL.md` derives
from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
(**CC BY-SA 4.0**). ShareAlike does not permit adding the NonCommercial restriction this
repository ships under, and upstream's own `ATTRIBUTION.md` flags the same hazard. Its
rules are substantially covered by `academic-paper/references/writing_quality_check.md`
in any case. Anyone considering importing that file should get an independent read first.
