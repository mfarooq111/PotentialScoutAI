from workflow.graph import graph

initial_state = {
    "company_name": "Careem",
    "search_results": [],
    "draft_report": "",
    "report": "",
    "opportunity_report": "",
    "qualification_report": ""
}


result = graph.invoke(initial_state)

print("\n========== STATE DEBUG ==========")

print("Available keys:", result.keys())

print("Draft report:", repr(result.get("draft_report")))
print("Draft length:", len(result.get("draft_report", "")))

print("Final report length:", len(result.get("report", "")))

print("\n========== INITIAL REPORT ==========\n")
print(result.get("draft_report"))

print("\n========== EVIDENCE-REVIEWED REPORT ==========\n")
print(result.get("report"))

print("\n========== OPPORTUNITY REPORT ==========\n")
print(result.get("opportunity_report"))

print(
    "\nOpportunity report length:",
    len(result.get("opportunity_report", ""))
)

print("\n========== OPPORTUNITY SCORING ==========\n")
print(result.get("qualification_report"))