
from langgraph.graph import StateGraph, START, END

from workflow.state import ResearchState
from tools.search import search_web
from config.models import llm


# Node 1: Research company
def research_node(state: ResearchState):

    company_name = state["company_name"]

    results = search_web(
        query=f"{company_name} company services products business operations",
        max_results=3
    )

    return {
        "search_results": results
    }


# Node 2: Analyze research results
def analysis_node(state: ResearchState):

    company_name = state["company_name"]
    search_results = state["search_results"]

    context_parts = []

    for index, result in enumerate(search_results, start=1):

        title = result.get("title", "Untitled")
        url = result.get("url", "URL unavailable")
        content = result.get("content", "No content available")

        source_info = f"""
Source [{index}]
Title: {title}
URL: {url}
Content: {content}
"""

        context_parts.append(source_info)

    context = "\n\n".join(context_parts)

    prompt = f"""
    You are a careful business research analyst.

    Research the following company using only the supplied sources.

    Company: {company_name}

    Research Sources:
    {context}

    Instructions:
    - Use only information supported by the supplied sources.
    - Do not invent statistics or financial figures.
    - Identify conflicting information between sources.
    - If information is unavailable, say so.
    - Cite factual claims using [Source 1], [Source 2], etc.
    - Label business opportunities as recommendations,
      not confirmed company plans.
    - Do not present assumptions as verified facts.
    - Keep recommendations separate from factual findings.

    Sections:
    1. Company Overview
    2. Main Products and Services
    3. Business Operations
    4. Potential Business Opportunities
    5. Key Findings and Information Gaps

    Keep the report informative and concise.
    """

    response = llm.invoke(prompt)

    print("\n[DEBUG] Analysis node executed")
    print("[DEBUG] Draft length:", len(response.content))

    return {
        "draft_report": response.content
    }


# Node 3: Review factual claims against sources
def verification_node(state: ResearchState):

    company_name = state["company_name"]
    search_results = state["search_results"]
    draft_report = state["draft_report"]

    print("\n[DEBUG] Verification node executed")
    print("[DEBUG] Received draft length:", len(draft_report))

    sources = []

    for index, result in enumerate(search_results, start=1):

        sources.append(f"""
Source [{index}]
Title: {result.get("title", "Untitled")}
URL: {result.get("url", "URL unavailable")}
Content: {result.get("content", "No content available")}
""")

    source_context = "\n\n".join(sources)

    prompt = f"""
    You are an evidence reviewer auditing a company research report.

    Company: {company_name}

    ORIGINAL SOURCES:
    {source_context}

    DRAFT REPORT:
    {draft_report}

    Your task is to review the report against the original sources.

    First, perform a claim-by-claim evidence audit.

    For every factual claim:

    1. Identify the individual factual claim.
    2. Identify the source or sources relevant to that claim.
    3. Check the actual source content.
    4. Extract a short supporting or contradicting evidence excerpt.
    5. Assign exactly one evidence status.

    Allowed evidence statuses:

    - SUPPORTED: Directly supported by the provided sources.
    - CONTRADICTED: Contradicted by the provided sources.
    - CONFLICTING: Different sources provide inconsistent information.
    - UNSUPPORTED: No provided source establishes the claim.

    Instructions:
    - Review every factual claim individually.
    - Break compound statements into separate factual claims.
    - Do not assume a citation supports a claim just because
      its source number is present.
    - Do not use external knowledge.
    - Do not invent evidence or replacement facts.
    - If a claim is unsupported, remove it or explicitly qualify it.
    - If sources conflict, explain the disagreement without guessing.
    - Preserve supported information and its source references.
    - Keep business recommendations separate from verified facts.
    - Do not turn recommendations into confirmed company plans.
    - Do not classify a recommendation as a factual claim.

    Produce the output in two parts.

    PART 1: CLAIM-BY-CLAIM EVIDENCE AUDIT

    Use the following columns:

    | Claim | Source | Evidence | Status | Action Taken |

    Include every important factual claim from the draft.

    PART 2: REVIEWED BUSINESS RESEARCH REPORT

    Return the reviewed report using these sections:

    1. Company Overview
    2. Main Products and Services
    3. Business Operations
    4. Potential Business Opportunities
    5. Evidence Issues and Information Gaps

    At the end, briefly summarize:

    - Unsupported claims removed or qualified.
    - Contradicted claims identified.
    - Conflicting information identified.
    - Important information still missing.

    Important:
    The reviewed report must reflect the evidence audit.
    Do not retain a factual claim as verified if the audit
    identifies it as unsupported or contradicted.

    Company: {company_name}
    """

    response = llm.invoke(prompt)

    return {
        "report": response.content
    }



# Node 4: Identify potential business opportunities
def opportunity_node(state: ResearchState):

    company_name = state["company_name"]
    report = state["report"]

    prompt = f"""
    You are an AI business opportunity analyst.

    Analyze the following company research report and identify
    potential opportunities where AI, automation, or software
    solutions could create business value.

    Company: {company_name}

    Research Report:
    {report}

    Instructions:

    - Base your analysis on the supplied research report.
    - Do not invent company problems or claim that the company
      is currently looking for these solutions.
    - Distinguish evidence from assumptions.
    - Focus on practical AI, automation, and software opportunities.
    - Avoid generic recommendations that could apply to any company.
    - Explain why each opportunity is relevant to this company.

    For each opportunity, provide:

    1. Opportunity Title
    2. Relevant Business Activity
    3. Potential Improvement Area
    4. Proposed AI or Software Solution
    5. Supporting Evidence from the Research
    6. Expected Business Value

    Identify 3 to 5 meaningful opportunities.

    Clearly label these as potential opportunities,
    not confirmed company requirements.

    Company: {company_name}
    """

    response = llm.invoke(prompt)

    print("\n[DEBUG] Opportunity node executed")
    print("[DEBUG] Opportunity report length:", len(response.content))

    return {
        "opportunity_report": response.content
    }



# Node 5: Score and prioritize opportunities
def scoring_node(state: ResearchState):

    company_name = state["company_name"]
    report = state["report"]
    opportunities = state["opportunity_report"]

    prompt = f"""
    You are a business opportunity evaluation analyst.

    Evaluate and rank the following AI/software opportunities
    for {company_name}.

    COMPANY RESEARCH:
    {report}

    IDENTIFIED OPPORTUNITIES:
    {opportunities}

    Score each opportunity using these criteria:

    1. Strategic Fit (30%):
       How closely does it align with the company's business?

    2. Evidence Strength (30%):
       How strongly is it supported by the available research?

    3. Potential Business Value (25%):
       How meaningful could its business impact be?

    4. Implementation Feasibility (15%):
       How practical would it be to implement?

    For each criterion, assign a score from 1 to 5.

    Calculate the weighted overall score out of 100.

    Formula:
    Overall Score =
    (Strategic Fit / 5 * 30) +
    (Evidence Strength / 5 * 30) +
    (Business Value / 5 * 25) +
    (Feasibility / 5 * 15)

    Output for each opportunity:
    - Opportunity name
    - Four individual scores
    - Overall score out of 100
    - Brief reasoning
    - Priority: High, Medium, or Low

    Rank opportunities from highest to lowest score.

    IMPORTANT:
    - These are preliminary heuristic scores, not verified
      business assessments.
    - Do not invent company requirements or internal problems.
    - Do not invent financial figures or guaranteed ROI.
    - Give lower evidence scores when an opportunity relies
      mainly on assumptions.
    """

    response = llm.invoke(prompt)

    print("\n[DEBUG] Scoring node executed")
    print("[DEBUG] Scoring report length:", len(response.content))

    return {
        "qualification_report": response.content
    }

    
# Build workflow
builder = StateGraph(ResearchState)

builder.add_node("research", research_node)
builder.add_node("analysis", analysis_node)
builder.add_node("verification", verification_node)
builder.add_node("opportunity", opportunity_node)
builder.add_node("scoring", scoring_node)


builder.add_edge(START, "research")
builder.add_edge("research", "analysis")
builder.add_edge("analysis", "verification")
builder.add_edge("verification", "opportunity")
builder.add_edge("opportunity", "scoring")
builder.add_edge("scoring", END)

graph = builder.compile()
