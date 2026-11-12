import streamlit as st
from workflow.graph import graph


st.set_page_config(
    page_title="PotentialScout AI",
    layout="wide"
)

st.title("PotentialScout AI")

st.subheader("Company Research & Opportunity Intelligence")

st.write(
    "Research companies, discover potential AI/software opportunities, "
    "and prioritize them using AI-powered analysis."
)

company_name = st.text_input(
    "Enter company name",
    placeholder="e.g. Careem, Uber, Amazon"
)




if st.button("Analyze Company", type="primary"):

    if not company_name.strip():
        st.warning("Please enter a company name.")

    else:
        initial_state = {
            "company_name": company_name.strip(),
            "search_results": [],
            "draft_report": "",
            "report": "",
            "opportunity_report": "",
            "qualification_report": ""
        }

        with st.spinner(
            f"Researching and analyzing {company_name}..."
        ):
            try:
                result = graph.invoke(initial_state)

                st.success("Company analysis completed!")

                tab1, tab2, tab3, tab4 = st.tabs([
                    "Research",
                    "Verified Report",
                    "Opportunities",
                    "Opportunity Scores"
                ])

                with tab1:
                    st.markdown(result.get("draft_report", ""))

                with tab2:
                    st.markdown(result.get("report", ""))

                with tab3:
                    st.markdown(result.get("opportunity_report", ""))

                with tab4:
                    st.markdown(result.get("qualification_report", ""))

            except Exception as e:
                st.error(f"An error occurred: {e}")