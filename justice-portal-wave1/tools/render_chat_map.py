from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment="Justice Project Chat Map", format="png")
dot.attr(rankdir="LR", size="10,8")

# Main project node
dot.node("Main", "Justice Project\n(Mission Hub)", shape="ellipse", style="filled", fillcolor="#FFD966")

# Core branches
dot.node("Case", "Jace & Josh Case\n(Systemic Failures, Misconduct)", shape="box", style="filled", fillcolor="#F4CCCC")
dot.node("System", "Justice Dashboard & AI Evidence System", shape="box", style="filled", fillcolor="#C9DAF8")
dot.node("Distribution", "Evidence Packet Distribution Plan", shape="box", style="filled", fillcolor="#B6D7A8")
dot.node("Analysis", "Contradiction & Misconduct Analysis", shape="box", style="filled", fillcolor="#EAD1DC")
dot.node("Narrative", "Personal Narrative & Advocacy", shape="box", style="filled", fillcolor="#FFE599")
dot.node("Creative", "Creative Family Projects\n(Calendars, Journals, Dashboards)", shape="box", style="filled", fillcolor="#D9EAD3")

# Sub-branches for System
dot.node("Coding", "Coding & Debugging", shape="note", fillcolor="#D0E0E3", style="filled")
dot.node("OCR", "OCR & AI Summaries", shape="note", fillcolor="#D0E0E3", style="filled")
dot.node("Export", "Export & Dropbox Integration", shape="note", fillcolor="#D0E0E3", style="filled")

# Sub-branches for Distribution
dot.node("FBI", "FBI / DOJ / State\nOversight Packets", shape="note", fillcolor="#D9EAD3", style="filled")
dot.node("Media", "Media & Advocacy Outreach", shape="note", fillcolor="#D9EAD3", style="filled")

# Sub-branches for Analysis
dot.node("Contradictions", "Contradiction Tables", shape="note", fillcolor="#FCE5CD", style="filled")
dot.node("WhoIsWho", "Who is Who Tables", shape="note", fillcolor="#FCE5CD", style="filled")

# Sub-branches for Narrative
dot.node("Faith", "Faith & Prayer Integration", shape="note", fillcolor="#FFF2CC", style="filled")
dot.node("Book", "Book / Chapter Structure", shape="note", fillcolor="#FFF2CC", style="filled")

# Connections
dot.edges([("Main", "Case"), ("Main", "System"), ("Main", "Distribution"), ("Main", "Analysis"), ("Main", "Narrative"), ("Main", "Creative")])
dot.edges([("System", "Coding"), ("System", "OCR"), ("System", "Export")])
dot.edges([("Distribution", "FBI"), ("Distribution", "Media")])
dot.edges([("Analysis", "Contradictions"), ("Analysis", "WhoIsWho")])
dot.edges([("Narrative", "Faith"), ("Narrative", "Book")])

# Render the diagram
output_path = 'c:/Users/ssped/Desktop/justice-portal-wave1/tools/justice_project_chat_map'
dot.render(output_path, cleanup=True)

print(output_path + ".png")
