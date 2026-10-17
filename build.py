#!/usr/bin/env python3
"""Build index.html for the awesome-free-llm-apis website.

Verbatim content renderer: every word of provider content comes from the
source README (mnfst/awesome-free-llm-apis, CC0-1.0). Chrome text (buttons,
labels, colophon) is the only added copy.

Usage:
  python build.py            # one-off LOCAL build, reads ./source-README.md
  python build.py --remote   # scheduled path: fetches the latest README over
                             # the network (never local) -- used by GitHub Actions
"""
import re
import sys
import html as htmllib
import datetime
import pathlib
import urllib.request

SOURCE = "mnfst/awesome-free-llm-apis"
RAW_URL = f"https://raw.githubusercontent.com/{SOURCE}/main/README.md"
GH_BLOB = f"https://github.com/{SOURCE}/blob/main"

HERE = pathlib.Path(__file__).resolve().parent


def esc(s: str) -> str:
    return htmllib.escape(s, quote=False).replace('"', "&quot;")


def resolve(url: str) -> str:
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    return f"{GH_BLOB}/{url}"


def inline(md: str) -> str:
    """Markdown inline (links, code, footnote refs, bare URLs) -> HTML."""
    s = esc(md)
    s = re.sub(r"\[([^\]]+)\]\((\S+?)\)",
               lambda m: f'<a href="{esc(resolve(m.group(2)))}">{m.group(1)}</a>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[\^(\d+)\]",
               lambda m: f'<sup><a href="#fn-{m.group(1)}" title="footnote">{m.group(1)}</a></sup>', s)
    # bare http(s) URLs not already inside an attribute or a tag
    s = re.sub(r'(?<!["\'=/])(https?://[^\s<]+[^\s<."])',
               r'<a href="\1">\1</a>', s)
    return s


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "provider"


def paragraphs(lines):
    out, cur = [], []
    for l in lines:
        if l.strip() == "":
            if cur:
                out.append(" ".join(cur))
                cur = []
        else:
            cur.append(l.strip())
    if cur:
        out.append(" ".join(cur))
    return out


def parse_table(lines):
    rows = []
    for l in lines:
        if not l.strip().startswith("|"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return None
    return rows[0], rows[1:]


def render_table(t):
    head, body = t
    th = "".join(f'<th scope="col">{esc(h)}</th>' for h in head)
    trs = "".join(
        "<tr>" + "".join(
            (f"<td>{inline(c)}</td>" if c else "<td></td>") for c in r
        ) + "</tr>" for r in body)
    return (f'<div class="tablewrap"><table>\n<thead><tr>{th}</tr></thead>\n'
            f"<tbody>{trs}</tbody>\n</table></div>")


def split_sections(md: str):
    sec, cur_title, cur = {}, None, []
    for l in md.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^## (?!#)\s*(.*)$", l)
        if m:
            if cur_title is not None:
                sec[cur_title] = cur
            cur_title, cur = m.group(1).strip(), []
        else:
            if cur_title is not None:
                cur.append(l)
    if cur_title is not None:
        sec[cur_title] = cur
    return sec


def parse_provider(block_lines):
    lines = block_lines
    m = re.match(r"^###\s*\[(.+?)\]\((\S+)\)\s*(\S+)\s*$", lines[0])
    assert m, f"bad provider header: {lines[0]!r}"
    name, url, flag = m.group(1), m.group(2), m.group(3)
    k = next((i for i, l in enumerate(lines) if l.startswith("Base URL:")), None)
    assert k is not None, f"no Base URL in {name}"
    base = re.match(r"^Base URL:\s*`([^`]+)`", lines[k]).group(1)
    desc_paras = paragraphs(lines[1:k])  # skip the heading line itself
    table = parse_table(lines) if any(l.strip().startswith("|") for l in lines) else None
    return {"name": name, "key_url": resolve(url), "flag": flag, "base": base,
            "desc_paras": desc_paras, "table": table}


def parse_group(lines):
    pre = []
    for l in lines:
        if l.startswith("###"):
            break
        pre.append(l)
    intro = paragraphs(pre)
    provs, cur = [], []
    for l in lines:
        if l.startswith("###"):
            if cur:
                provs.append(parse_provider(cur))
            cur = [l]
        elif cur:
            cur.append(l)
    if cur:
        provs.append(parse_provider(cur))
    return intro, provs


def card_html(pr, kind, seq):
    desc = "".join(f"<p>{inline(p)}</p>" for p in pr["desc_paras"])
    table = render_table(pr["table"]) if pr["table"] else ""
    return f"""
<details class="card" id="p-{slug(pr['name'])}" data-kind="{kind}">
<summary>
<span class="seq">{seq:02d}</span>
<span class="pname">{esc(pr["name"])}</span>
<span class="flag">{esc(pr["flag"])}</span>
<a class="klink" href="{esc(pr["key_url"])}" target="_blank" rel="noopener">key page</a>
<span class="chip" title="{esc(pr["base"])}">{esc(pr["base"].removeprefix("https://"))}</span>
<span class="chev" aria-hidden="true">+</span>
</summary>
<div class="c-body">
<div class="desc">{desc}</div>
<div class="urlbox">
<span class="urlbox-label">Base URL</span>
<code data-url>{esc(pr["base"])}</code>
<button type="button" class="copy" aria-label="Copy base URL">copy</button>
</div>
{table}
</div>
</details>"""


def group_html(title, kind, intro_paras, provs, seq_start):
    sid = "provider-apis" if kind == "provider" else "inference-providers"
    gn = {"provider-apis": "P", "inference-providers": "I"}[sid]
    cards, s = [], seq_start
    for pr in provs:
        cards.append(card_html(pr, kind, s))
        s += 1
    intro = "".join(f'<p class="g-intro">{inline(p)}</p>' for p in intro_paras)
    return (f'<section class="group" id="{sid}" data-kind="{kind}">\n'
            f'<div class="g-head"><h2 class="g-title"><span class="g-no">{gn}</span>'
            f'{esc(title)}</h2></div>\n{intro}{"".join(cards)}</section>'), s


def head_part(title, gn, inner):
    return (f'<section class="group side" id="{title.lower()}">\n'
            f'<div class="g-head"><h2 class="g-title"><span class="g-no">{gn}</span>'
            f'{esc(title)}</h2></div>\n{inner}</section>')


def main():
    remote = "--remote" in sys.argv
    if remote:
        with urllib.request.urlopen(RAW_URL, timeout=60) as r:
            md = r.read().decode("utf-8")
        print(f"fetched {RAW_URL} ({len(md)} bytes)")
    else:
        md = (HERE / "source-README.md").read_text(encoding="utf-8")
        print("local one-off build from source-README.md")

    sec = split_sections(md)

    # tagline + subnote live in the preamble HTML, above "## Contents"
    tagline = re.search(r"<p[^>]*>(LLM APIs[^<]*)</p>", md.replace("\r\n", "\n"))
    subnote = re.search(r"<sub>(All endpoints.*?)</sub>",
                        md.replace("\r\n", "\n"), re.S)
    assert tagline and subnote, "preamble tagline/subnote not found"
    tagline = tagline.group(1).strip()
    subnote = " ".join(subnote.group(1).split())

    intro_a, provs_a = parse_group(sec["Provider APIs"])
    intro_i, provs_i = parse_group(sec["Inference providers"])
    body_a, n = group_html("Provider APIs", "provider", intro_a, provs_a, 1)
    body_i, _ = group_html("Inference providers", "inference", intro_i, provs_i, n)

    gtab = parse_table(sec["Glossary"])
    glossary = head_part("Glossary", "G", render_table(gtab))

    cont_paras = paragraphs([l for l in sec["Contributing"] if not l.startswith("[^")])
    contributing = head_part("Contributing", "C",
                             "".join(f"<p>{inline(p)}</p>" for p in cont_paras))

    fnotes = {}
    for l in md.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^\[\^(\d+)\]:\s*(.*)$", l)
        if m:
            fnotes[int(m.group(1))] = m.group(2)
    fn_items = "".join(
        f'<p class="fnote" id="fn-{n}"><b><a href="#fn-{n}">[{n}]</a></b> {inline(t)}</p>'
        for n, t in sorted(fnotes.items()))
    footnotes = f'<section class="smallprint" id="footnotes" aria-label="footnotes">{fn_items}</section>'

    n_providers = len(provs_a) + len(provs_i)
    n_models = sum(len(p["table"][1]) for p in provs_a + provs_i if p["table"])
    build_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    cover = (f'<p class="zsub">{esc(tagline)}</p>\n'
             f'<p class="znote">{esc(subnote)}</p>')

    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    out = (tpl
           .replace("%%COVER%%", cover)
           .replace("%%BODY%%", body_a + "\n" + body_i + "\n" + glossary + "\n" + contributing)
           .replace("%%FOOTNOTES%%", footnotes)
           .replace("%%BUILD_DATE%%", build_date)
           .replace("%%N_PROVIDERS%%", str(n_providers))
           .replace("%%N_MODELS%%", str(n_models)))
    (HERE / "index.html").write_text(out, encoding="utf-8", newline="\n")
    print(f"built index.html: {n_providers} providers, {n_models} model rows, "
          f"{len(fnotes)} footnotes, synced {build_date}")


if __name__ == "__main__":
    main()
