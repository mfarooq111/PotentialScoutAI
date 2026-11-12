from typing import TypedDict

class ResearchState(TypedDict):
    company_name: str
    search_results: list
    draft_report: str
    report: str
    opportunity_report: str
    qualification_report: str