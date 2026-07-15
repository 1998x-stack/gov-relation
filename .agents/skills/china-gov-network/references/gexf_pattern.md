# GEXF Generation Pattern

When generating GEXF XML, use string formatting (NOT ElementTree) to avoid namespace
prefix issues. ElementTree's namespace handling causes duplicate attribute errors and
unbound prefix errors with the viz namespace.

## Correct Pattern

```python
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>...</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
# ... more attributes
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
# ...
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)  # "r,g,b" string
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    # ... more attvalues
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes (same pattern, size="8.0")

# Edges: person->organization (worked_at)
for pos in positions:
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    # ...
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Edges: person<->person (relationship), weight="2.0"

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
```

## Color Scheme

### Person nodes (by role)
- Party Secretary (县委书记/区委书记): `"255,50,50"` — Red
- County/District Mayor/Deputy Mayor: `"50,100,255"` — Blue
- Discipline Inspection (纪委书记/监委): `"255,165,0"` — Orange
- Others: `"100,100,100"` — Grey

### Organization nodes (by type)
- 党委: `"255,200,200"` — Pink
- 政府: `"200,200,255"` — Light blue
- 开发区: `"200,255,200"` — Light green
- 乡镇/街道: `"255,255,200"` — Light yellow
- 事业单位: `"220,220,220"` — Light grey
- 群团: `"255,220,255"` — Light purple
- 人大: `"200,255,255"` — Cyan
- 政协: `"255,240,200"` — Cream
- Default: `"200,200,200"`

## Node Sizes
- Top leaders (书记/县长): 20.0
- Other persons: 12.0
- Organizations: 8.0
