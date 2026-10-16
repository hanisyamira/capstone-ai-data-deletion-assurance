import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title='AI Data Deletion Assurance Engine',page_icon='🛡️',layout='wide')
ROOT=Path(__file__).resolve().parent
DATA_ROOT=ROOT
if not (ROOT/'data_lineage.json').exists() and (ROOT.parent/'data_lineage.json').exists():
    DATA_ROOT=ROOT.parent

def load_json(name):
    p=DATA_ROOT/name
    if not p.exists(): return [],f'{name} not found in {DATA_ROOT}'
    try:
        obj=json.loads(p.read_text(encoding='utf-8-sig'))
        if not isinstance(obj,list): return [],f'{name} must contain a JSON list'
        return obj,None
    except Exception as e: return [],f'Could not load {name}: {e}'

lineage,lineage_error=load_json('data_lineage.json')
audit,audit_error=load_json('audit_log.json')

st.markdown('''<style>
.stApp {background: #f6f8fc; color:#18243a;}
.block-container {padding-top:1.6rem; max-width:1450px;}
.hero {background:linear-gradient(115deg,#172b53,#3b45a5);padding:26px 30px;border-radius:18px;color:white;margin-bottom:18px;}
.hero h1 {color:white;margin:0;font-size:2rem;}
.hero p {color:#dce4ff;margin:7px 0 0;}
.kpi {background:white;border:1px solid #e3e8f1;border-radius:14px;padding:18px;min-height:100px;}
.kpi .number {font-size:1.9rem;font-weight:800;color:#22366b;}
.kpi .label {color:#66728a;font-size:.9rem;}
.step {padding:13px;border-radius:12px;background:white;border:1px solid #e2e8f1;text-align:center;font-weight:650;min-height:74px;}
.small {color:#69758b;font-size:.85rem;}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><div style="font-size:.78rem;letter-spacing:.12em">AI GOVERNANCE INTELLIGENCE DECK · CAPSTONE DEMONSTRATION</div><h1>AI Data Deletion Assurance Engine</h1><p>Discover · Classify · Trace · Delete · Verify · Evidence</p></div>',unsafe_allow_html=True)

for err in (lineage_error,audit_error):
    if err: st.warning(err+' — dashboard remains usable with empty data.')

active=sum(str(x.get('status','')).upper()=='ACTIVE' for x in lineage)
deleted=sum(str(x.get('status','')).upper()=='DELETED' for x in lineage)
checks=[x for x in audit if x.get('event_type')=='DELETION_VERIFICATION']
def evidence_quality(event):
    if not event.get('data_id') or str(event.get('data_id')).lower() in ('none','null',''):
        return 'INCOMPLETE'
    fields=('source_check','vector_check','lineage_check')
    if any(event.get(k) is not True and event.get(k) is not False for k in fields):
        return 'INCOMPLETE'
    if str(event.get('status','')).upper()=='PASS' and all(event.get(k) is True for k in fields):
        return 'VERIFIED PASS (RECORDED)'
    if str(event.get('status','')).upper()=='FAIL' or any(event.get(k) is False for k in fields):
        return 'FAIL / REVIEW'
    return 'INCOMPLETE'

passed=sum(evidence_quality(x)=='VERIFIED PASS (RECORDED)' for x in checks)
failed=sum(evidence_quality(x)=='FAIL / REVIEW' for x in checks)
incomplete=sum(evidence_quality(x)=='INCOMPLETE' for x in checks)
latest=sorted(checks,key=lambda x:str(x.get('timestamp','')))[-1] if checks else None

pages=['Overview','Deletion Assurance Workflow','AI Data Inventory','Lineage & Impact','Deletion Verification','Audit Evidence','Cost Effectiveness','Governance Framework']
with st.sidebar:
    st.title('🛡️ Governance Console')
    page=st.radio('Explore modules',pages)
    st.divider()
    st.caption('CAPSTONE DEMONSTRATION')
    st.success('Dashboard running')
    st.info('Purview integration: proposed, not connected')
    st.caption('Read-only: no deletion is executed from this interface.')

if page=='Overview':
    st.subheader('Why this project matters')
    st.write(
        'Organisations increasingly use AI assistants to retrieve information from internal documents. '
        'When personal or confidential information must be deleted, removing the original file may not '
        'remove its derived embeddings, vector records, cached copies, or retained logs. '
        'The governance challenge is not only to perform deletion, but to establish its scope, '
        'verify supported outcomes, and retain evidence for review.'
    )
    st.info(
        '**Project objective:** Design an AI Data Deletion Assurance Governance Framework that '
        'connects data discovery, classification, lineage, authorisation, deletion, verification, '
        'and audit evidence across AI data lifecycles.'
    )

    cols=st.columns(4)
    for c,v,label in zip(cols,[len(lineage),active,deleted,f'{passed}/{len(checks)}'],['Tracked data records','Active records','Marked deleted','Complete recorded PASS / all events']):
        c.markdown(f'<div class="kpi"><div class="number">{v}</div><div class="label">{label}</div></div>',unsafe_allow_html=True)

    st.subheader('Real-world inspired scenario: employee data in a healthcare AI assistant')
    scenario,challenge=st.columns([1.2,1])
    with scenario:
        st.markdown('**The situation**')
        st.write(
            'A healthcare organisation uses an internal Retrieval-Augmented Generation (RAG) '
            'assistant to answer staff questions using HR and policy documents. An employee requests '
            'deletion of personal information that was previously ingested into the assistant.'
        )
        st.markdown('**The question**')
        st.write('How can the organisation demonstrate what was deleted, what was checked, and what remains unresolved?')
    with challenge:
        st.markdown('**Where information may persist**')
        st.markdown(
            '- Original source documents\n'
            '- Embeddings and vector database entries\n'
            '- Application logs and caches\n'
            '- Backups or other retained copies\n'
            '- Model weights, if data was used for fine-tuning'
        )
        st.caption('Illustrative scenario using synthetic/example data; not a claim about a real organisation or deletion request.')

    st.subheader('Data deletion assurance lifecycle')
    names=['🔎 Discover','🛡️ Classify','🔗 Trace','🗑️ Delete','✅ Verify','📄 Evidence']
    for col,name in zip(st.columns(6),names):
        col.markdown(f'<div class="step">{name}</div>',unsafe_allow_html=True)
    st.caption('Conceptual governance workflow. The dashboard reads historical JSON evidence; it does not run a live scan or deletion.')

    st.subheader('Proof of concept and recorded evidence')
    a,b=st.columns([1.3,1])
    with a:
        st.write(
            'The local proof of concept tracks source documents, embedding models, a ChromaDB '
            'vector collection, and a local Ollama-based RAG workflow. Historical JSON records '
            'capture lineage metadata and deletion-verification checks.'
        )
        st.info('Microsoft Purview is a proposed enterprise discovery/classification integration. It is not connected to this dashboard.')
        st.caption('Recorded checks do not establish removal from backups, caches, logs, or fine-tuned model weights.')
    with b:
        st.markdown('**Evidence summary**')
        if latest:
            st.metric('Latest recorded verification',str(latest.get('status','Unknown')))
            st.caption(f"Data ID: {latest.get('data_id','—')} · {latest.get('timestamp','—')}")
        else:
            st.warning('No verification events available')
        st.caption('Historical status reported by audit log, not independently rechecked by this dashboard.')

    st.subheader('Cost-effectiveness and organisational value')
    value_cols=st.columns(3)
    with value_cols[0]:
        st.markdown('**⏱️ Reduced manual effort**')
        st.write('A consistent inventory and evidence workflow could reduce repeated manual searches and documentation.')
    with value_cols[1]:
        st.markdown('**💻 Practical prototype cost**')
        st.write('Local Python, ChromaDB, Ollama, and Streamlit enable a proof of concept without a production AI platform.')
    with value_cols[2]:
        st.markdown('**🛡️ Governance value**')
        st.write('Structured evidence may make reviews more consistent and help identify unresolved deletion risks.')

    st.info('Explore the **Cost Effectiveness** module in the sidebar to compare adjustable annual scenarios.')


    with st.expander('How cost-effectiveness can be evaluated'):
        st.write(
            'Compare a manual baseline with the proposed workflow using the same test cases. '
            'Record time to locate relevant data, time to prepare verification evidence, '
            'number of missed dependencies, and infrastructure or service charges.'
        )
        st.markdown('**Illustrative calculation (not measured results):**')
        st.code('Labour cost per request = staff hours × hourly rate\n'
                'Estimated saving per request = manual labour cost − workflow labour cost − incremental service cost',language='text')
        st.caption('No measured cost savings or production return on investment are claimed. Azure/Purview usage may incur charges.')

elif page=='Cost Effectiveness':
    st.subheader('Cost Effectiveness & Feasibility')
    st.caption('Interactive scenario modelling · AUD · Illustrative inputs only, not Lifeblood costs or measured project savings.')
    st.write(
        'Compare the staff effort required for a manual deletion-assurance process with an '
        'assisted workflow. This is a planning tool, not a validated business case: '
        'time savings must be measured using comparable deletion cases.'
    )

    st.markdown('#### Adjust the assumptions')
    a,b=st.columns(2)
    with a:
        requests=st.number_input('Deletion requests per year',min_value=0,max_value=100000,value=50,step=10)
        manual_hours=st.number_input('Manual staff hours per request',min_value=0.0,max_value=1000.0,value=3.0,step=0.5)
        hourly_rate=st.number_input('Fully loaded staff cost (A$/hour)',min_value=0.0,max_value=10000.0,value=60.0,step=5.0)
    with b:
        assisted_hours=st.number_input('Assisted staff hours per request',min_value=0.0,max_value=1000.0,value=1.0,step=0.5)
        annual_operating=st.number_input('Annual infrastructure, licences & maintenance (A$)',min_value=0.0,max_value=10000000.0,value=2000.0,step=500.0)
        initial_setup=st.number_input('One-time setup and training cost (A$)',min_value=0.0,max_value=10000000.0,value=4000.0,step=500.0)
    years=st.slider('Spread setup cost over (years)',min_value=1,max_value=5,value=2)

    manual_annual=requests*manual_hours*hourly_rate
    assisted_annual=requests*assisted_hours*hourly_rate+annual_operating+initial_setup/years
    gross_saving=requests*(manual_hours-assisted_hours)*hourly_rate
    net_saving=manual_annual-assisted_annual
    k1,k2,k3=st.columns(3)
    k1.metric('Manual annual cost',f'A${manual_annual:,.0f}')
    k2.metric('Assisted annual cost',f'A${assisted_annual:,.0f}')
    k3.metric('Estimated net annual benefit',f'A${net_saving:,.0f}')
    st.caption('Annualised assisted cost = assisted labour + annual operating costs + setup cost / amortisation years. '
               'Negative benefit indicates the assisted scenario costs more under these assumptions.')

    st.markdown('#### Annual cost comparison')
    comparison=pd.DataFrame({'Annual cost (A$)':{'Manual process':manual_annual,'Assisted process':assisted_annual}})
    st.bar_chart(comparison)
    labour_saving_per_request=(manual_hours-assisted_hours)*hourly_rate
    overhead=annual_operating+initial_setup/years
    if labour_saving_per_request>0:
        import math
        breakeven=math.ceil(overhead/labour_saving_per_request)
        st.info(f'**Illustrative break-even volume:** about {breakeven:,} requests/year to offset annualised setup and operating costs, assuming the selected time savings are achieved.')
    else:
        st.warning('There is no positive per-request labour saving with these assumptions; a break-even request volume cannot be calculated.')

    st.markdown('#### Open-source prototype vs enterprise deployment')
    st.dataframe(pd.DataFrame([
        {'Area':'Software','Local proof of concept':'Python, ChromaDB, Ollama, Streamlit (no licence fee for this local setup)','Enterprise scenario':'Commercial tools may add licence or consumption charges'},
        {'Area':'Infrastructure','Local proof of concept':'Local machine, electricity and storage','Enterprise scenario':'Cloud/servers, backups, monitoring and security'},
        {'Area':'People','Local proof of concept':'Development, testing and upkeep still required','Enterprise scenario':'Integration, governance, privacy and operations staffing'},
        {'Area':'Discovery','Local proof of concept':'Locally maintained inventory and classification metadata','Enterprise scenario':'Purview or comparable platform, subject to access and pricing'},
        {'Area':'Evidence','Local proof of concept':'Local JSON audit trail (not tamper-evident)','Enterprise scenario':'Controlled retention, access, integrity and audit processes'},
    ]),use_container_width=True,hide_index=True)
    st.warning('All default numbers are hypothetical examples. No productivity improvement, compliance saving, or ROI has been measured. '
               'The current dashboard is a read-only evidence viewer; it does not automate the full governance process. '
               'Microsoft Purview is proposed, not integrated or priced here.')
    with st.expander('Methodology and what to measure next'):
        st.markdown("""
- Run the **same synthetic deletion cases** manually and with the implemented workflow.
- Measure staff time for discovery, lineage review, deletion, verification, evidence preparation and approval.
- Record completeness, missed dependencies, rework and unresolved risks alongside elapsed time.
- Include deployment, cloud, licensing, security, training and maintenance costs in a real assessment.
- Compare equivalent assurance scope; faster checks are not a saving if required controls are omitted.
""")

elif page=='Deletion Assurance Workflow':
    st.subheader('Interactive Deletion Assurance Workflow')
    st.caption('Select a tracked record and explore the decision gates. This is a read-only walkthrough, not an operational deletion request.')
    if not lineage:
        st.info('Add data_lineage.json to explore a record.')
    else:
        options={f"{r.get('source_file','Unknown')} · {r.get('data_id','?')}":r for r in lineage}
        chosen=st.selectbox('Choose an employee data record',list(options),key='workflow_record')
        record=options[chosen]
        rid=record.get('data_id')
        relevant=[e for e in checks if e.get('data_id')==rid]
        relevant.sort(key=lambda e:str(e.get('timestamp','')),reverse=True)
        verification=relevant[0] if relevant else None
        stages=['Request & scope','Discover & classify','Lineage & impact','Approval & execution','Verify & evidence','Governance closure']
        stage=st.radio('Explore governance stage',stages,horizontal=True,key='workflow_stage')
        st.progress((stages.index(stage)+1)/len(stages))
        left,right=st.columns([1.55,1])
        with left:
            if stage=='Request & scope':
                st.markdown('#### 1 · Receive and scope the request')
                st.write('Identify the data subject and the requested deletion scope. Verify identity and authority before acting.')
                st.info('The dataset is a historical PoC record. No real request, identity verification, or authorisation is evidenced by the JSON.')
            elif stage=='Discover & classify':
                st.markdown('#### 2 · Discover and classify')
                st.write('Locate the source asset, assess sensitivity, determine ownership, and check retention obligations.')
                st.write('**Recorded classification:**',record.get('classification','Not recorded'))
                st.write('**Data owner:**',record.get('owner','Not recorded'))
                st.write('**Data steward:**',record.get('data_steward','Not recorded'))
                st.caption('Classification is recorded local metadata, not a Purview classification scan.')
            elif stage=='Lineage & impact':
                st.markdown('#### 3 · Trace downstream dependencies')
                st.write('Review the recorded RAG path and assess where copies or derived data might persist.')
                flow = (f"Source: {record.get('source_file','—')}\n"
                        f"  ↓ Embedding: {record.get('embedding_model','—')}\n"
                        f"  ↓ Vector collection: {record.get('vector_collection','—')}\n"
                        f"  ↳ Retrieved context → LLM: {record.get('llm','—')}")
                st.code(flow,language='text')
                st.warning('Logs, backups, caches, and fine-tuned weights are not covered by this metadata.')
            elif stage=='Approval & execution':
                st.markdown('#### 4 · Authorise and execute deletion')
                st.write('A production workflow would check legal holds, obtain appropriate approval, then invoke deletion in each approved target.')
                st.write('**Recorded lineage status:**',record.get('status','Unknown'))
                st.write('**Recorded deletion time:**',record.get('deleted_at') or 'Not recorded')
                st.warning('This prototype does not prove approval and cannot execute deletion. A DELETED label is historical metadata.')
            elif stage=='Verify & evidence':
                st.markdown('#### 5 · Verify and retain evidence')
                if verification:
                    for key,label in [('source_check','Source file'),('vector_check','Vector records'),('lineage_check','Lineage metadata')]:
                        val=verification.get(key)
                        st.write(('✅' if val is True else '❌' if val is False else '⚪')+' **'+label+':** '+('Recorded PASS' if val is True else 'Recorded FAIL' if val is False else 'Not recorded'))
                    st.write('**Assessment:**',evidence_quality(verification))
                    st.caption('Historical event: '+str(verification.get('timestamp','Unknown')))
                else: st.warning('No linked verification event found for this data ID.')
            else:
                st.markdown('#### 6 · Review residual risk and close')
                st.write('A data steward or authorised reviewer should confirm evidence completeness, assess unresolved locations, document exceptions, and decide whether to close the request.')
                st.warning('No sign-off, backup purge, legal-hold review, or closure approval is evidenced in the available JSON.')
        with right:
            st.markdown('#### Record summary')
            st.metric('Data ID',str(rid))
            st.write('**Source:**',record.get('source_file','—'))
            st.write('**Recorded status:**',record.get('status','—'))
            if verification:
                quality=evidence_quality(verification)
                if quality.startswith('VERIFIED'): st.success(quality)
                elif quality.startswith('FAIL'): st.error(quality)
                else: st.warning(quality)
            else: st.warning('No linked verification')
            st.caption('Evidence refers to past PoC activity, not a new live test.')
        with st.expander('View underlying metadata and latest verification event'):
            st.json({'lineage':record,'latest_verification':verification})

elif page=='AI Data Inventory':
    st.subheader('AI Data Inventory')
    st.caption('Read from data_lineage.json. Classifications below are recorded metadata, not automatic Purview detections.')
    if lineage:
        show=['data_id','source_file','classification','owner','data_steward','vector_collection','status','deleted_at']
        st.dataframe(pd.DataFrame([{k:x.get(k) for k in show} for x in lineage]),use_container_width=True,hide_index=True)
        classes=pd.DataFrame(lineage)['classification'].fillna('Unspecified').value_counts()
        st.bar_chart(classes)
    else: st.info('Add your data_lineage.json file to populate this module.')

elif page=='Lineage & Impact':
    st.subheader('Data Lineage & AI Impact')
    st.caption('Logical relationships reconstructed from recorded metadata; this is not a live dependency scan.')
    options={f"{x.get('source_file','Unknown')} ({x.get('data_id','?')})":x for x in lineage}
    if options:
        selected=st.selectbox('Choose a tracked dataset',list(options))
        x=options[selected]
        labels=[f"📄 Source\n{x.get('source_file','—')}",f"🧬 Embedding\n{x.get('embedding_model','—')}",f"🗃️ Vector collection\n{x.get('vector_collection','—')}",f"🤖 LLM\n{x.get('llm','—')}"]
        for col,label in zip(st.columns(4),labels): col.info(label)
        st.write('**Governance metadata**')
        st.json({k:x.get(k) for k in ['data_id','source_hash','owner','data_steward','classification','purpose','retention_rule','ingested_at','status','deleted_at']})
        st.warning('A model-level impact assessment is still required for fine-tuned models. Removing RAG vectors does not establish machine unlearning.')
    else: st.info('No lineage records available.')

elif page=='Deletion Verification':
    st.subheader('Deletion & Verification Evidence')
    st.warning('Read-only review. No delete button is provided. A recorded PASS is not proof that backups, caches, logs, or model weights were erased.')
    if checks:
        keys=['timestamp','data_id','source_check','vector_check','lineage_check','status']
        a,b,c=st.columns(3)
        a.metric('Complete recorded PASS',passed)
        b.metric('FAIL / review',failed)
        c.metric('Incomplete / unlinked',incomplete)
        st.caption('Complete PASS requires a linked data ID, all three check fields set to true, and a PASS status. This is a historical evidence-quality screen, not independent verification.')
        st.dataframe(pd.DataFrame([{**{k:x.get(k) for k in keys},'evidence_quality':evidence_quality(x)} for x in sorted(checks,key=lambda z:str(z.get('timestamp','')),reverse=True)]),use_container_width=True,hide_index=True)
        ids=sorted(set(str(x.get('data_id')) for x in checks if x.get('data_id')))
        selected=st.selectbox('Inspect verification record for data ID',ids) if ids else None
        for x in reversed(checks):
            if str(x.get('data_id'))==selected:
                st.json(x);break
    else: st.info('No verification events in audit_log.json.')

elif page=='Audit Evidence':
    st.subheader('Audit Trail')
    st.caption('Historical event records from audit_log.json; not a tamper-evident evidence store.')
    if audit:
        events=sorted(audit,key=lambda x:str(x.get('timestamp','')),reverse=True)
        st.dataframe(pd.DataFrame(events),use_container_width=True,hide_index=True)
        st.download_button('Download audit JSON snapshot',json.dumps(audit,indent=2),file_name='audit_snapshot.json',mime='application/json')
    else: st.info('No audit records available.')

else:
    st.subheader('Governance Framework & Responsibilities')
    st.write('A practical governance model combining enterprise controls with a local deletion assurance proof of concept.')
    rows=[
        ('Discover & inventory','AI system owner / IT','Inventory data sources and AI dependencies','Purview proposed; local metadata demonstrated'),
        ('Classify & assess risk','Data steward / Privacy','Determine sensitivity, obligations and retention','Metadata-based prototype'),
        ('Trace impact','AI engineer / Data steward','Map source → embeddings → vector store → model','Local lineage JSON'),
        ('Approve deletion','Data owner / Privacy','Validate scope, legal holds and authorization','Governance design only'),
        ('Execute deletion','AI engineer / IT','Remove approved source and derived vector entries','Existing local PoC; not invoked here'),
        ('Verify & evidence','Security / Auditor','Validate checks and preserve reviewable records','Historical audit JSON'),
    ]
    st.dataframe(pd.DataFrame(rows,columns=['Control stage','Responsible role','Expected control','Prototype coverage']),use_container_width=True,hide_index=True)
    st.info('Limitations: no live Purview integration, no backup deletion proof, no fine-tuned model unlearning, and no independent integrity verification of JSON evidence.')

st.divider()
st.caption('Capstone meeting prototype · Synthetic/example data only · Read-only evidence viewer')
