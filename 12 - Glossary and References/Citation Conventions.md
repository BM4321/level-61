---
title: "Citation Conventions"
type: "system"
tags:
  - semester-6
  - references
---

# Citation Conventions

Two things: how **this vault** cites its sources, and how **you** should cite in your coursework and FYP.

> [!warning] Your department decides
> No referencing style was prescribed in the material supplied for this build ([[Syllabus Verification Log]]). APA, IEEE and Harvard are all common in computing. Use the style your department or supervisor requires, and apply it consistently.

## 1. How the vault cites
- **In lessons:** short author–year mentions in the text (e.g. Hevner et al., 2004), and full entries in each lesson's "Sources" section.
- **Everywhere:** each Sources section ends with a note that links weren't checked during the build (there was no network access).
- **Register:** all sources are collected in [[Source Register]], with where they're cited and their verification status (none were verified online).
- **Fictional material:** organisations, people, data and authors in examples are fictional, and labelled as such (e.g. "Mwakyusa (2021)" in [[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]] is a placeholder, not a real paper).
- **Standards and laws:** cited by number and year, with a reminder to check for the current version or official text.

**Don't cite this vault** as an academic source in assessed work. Use it to learn, then find, read and cite the original sources.

## 2. How to cite in your work

### 2.1 The non-negotiable rules
1. **Find it, read it, verify it.** Every source in your reference list must exist, must say what you claim, and must be one you've read (at least the part you rely on).
2. **Every in-text citation has a reference entry, and every entry is cited.** Check with `citation_crosscheck` (in `04 - Final Year Project I/code/fyp_tools.py`) or your reference manager.
3. **One style, consistently**, including punctuation, italics and the order of elements.
4. **Quote rarely, with quotation marks and a page number; paraphrase properly**, with a citation.
5. **Credit code** you adapt (libraries, tutorials, Q&A answers) in comments and in your report, and respect licences.
6. **Disclose AI-tool use** as your institution requires; never cite a reference an AI tool suggested without finding and reading it.

### 2.2 The same journal article in three styles
Using a source from the register (verify its details before you use it):

| Style | In text | Reference list |
|---|---|---|
| APA 7 | (Hevner et al., 2004) | Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105. |
| IEEE | [1] | [1] A. R. Hevner, S. T. March, J. Park, and S. Ram, "Design science in information systems research," *MIS Quarterly*, vol. 28, no. 1, pp. 75–105, 2004. |
| Harvard (one common variant) | (Hevner et al. 2004) | Hevner, A.R., March, S.T., Park, J. and Ram, S. (2004) 'Design science in information systems research', *MIS Quarterly*, 28(1), pp. 75–105. |

Add a DOI where the style asks for one, and only after resolving it yourself at doi.org (`looks_like_doi` checks syntax only).

### 2.3 Other source types (APA 7 pattern)
| Type | Pattern |
|---|---|
| Book | Author, A. A. (Year). *Title* (ed.). Publisher. |
| Chapter in an edited book | Author, A. A. (Year). Chapter title. In E. Editor (Ed.), *Book title* (pp. x–y). Publisher. |
| Standard or report | Organisation. (Year). *Title* (Report or standard number). URL |
| Web page | Author or organisation. (Year, Month Day). *Title*. Site. URL |
| Software / library | Author or organisation. (Year). *Name* (Version x) [Computer software]. URL |
| Your own data | Not in the reference list: describe it in your methodology ("interviews with 8 staff, March 2026"). |

### 2.4 Secondary citations
If you only read source B, which discusses source A, cite B (in APA: "Smith (2010, as cited in Jones, 2020)"), and list only Jones in your references. Better: find and read A.

## 3. Checklist before you submit
- [ ] Every source found, read and verified (existence, details, content)
- [ ] `citation_crosscheck` (or your reference manager) reports nothing missing and nothing uncited
- [ ] One style throughout
- [ ] Quotations marked, with page numbers
- [ ] Code and AI use acknowledged as required

Back to [[Source Register]] · [[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]] · [[00 Dashboard]]
