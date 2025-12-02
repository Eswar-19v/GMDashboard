from jira_client import search_jql
from collections import defaultdict

# Base JQLs (you can modify the sprint name dynamically)
Sprint_JQL = 'sprint = "{}"'
QA_SPRINT_LABEL_JQL = 'labels="{}" AND labels not in ("Production_Escalation","Production_Request")'
PROD_ESC_JQL = 'labels = "{}" AND labels = "Production_Escalation"'


lastfive_sprintQA=[]
currentSprint="GM-QA-Sprint79"
currentSprintdev="GM Sprint 79"
lastfive_sprintQA.append(currentSprint)
for i in range(1,5):
    curr_sprnum=int(currentSprint.split("Sprint")[-1].strip())
    lastfive_sprintQA.append(f"GM-QA-Sprint{curr_sprnum - i}")

def fetch_sprint_tasks():
    """All tasks for Sprint GM Sprint 79"""
    lastfive_sprinttasks=[]
    lastfive_sprints=[]
    lastfive_sprints.append(currentSprintdev)
    for i in range(1,5):
        curr_sprnum=int(currentSprintdev.split("Sprint")[-1].strip())
        lastfive_sprints.append(f"GM Sprint {curr_sprnum - i}")
    for i in lastfive_sprints:
        s_jql=Sprint_JQL.format(i)
        print(s_jql)
        tasks=search_jql(s_jql)
        lastfive_sprinttasks.append({i: len(tasks)})
    return lastfive_sprinttasks


def fetch_qa_tasks():
    """QA sprint tasks (GM-QA-Sprint79)"""        
    lastfive_tasks=[]
    for i in lastfive_sprintQA:
        qa_sprint_jql = QA_SPRINT_LABEL_JQL.format(i)
        qa_tasks=search_jql(qa_sprint_jql)
        dict_users=fetch_users(qa_tasks)

        lastfive_tasks.append({i: [dict_users,len(qa_tasks)]})
    return lastfive_tasks



def fetch_prod_escalations():
    """Production escalation issues based on labels"""
    lastfive_ProdEsc=[]
    for i in lastfive_sprintQA:
        prod_esc_jql = PROD_ESC_JQL.format(i)
        prod_tasks=search_jql(prod_esc_jql)
        lastfive_ProdEsc.append({i: len(prod_tasks)})
        
    return lastfive_ProdEsc


def fetch_all_data(sprint_num: int):
    """Fetch all data for a given sprint name"""
    Sprint_Data =[]
    sprint_name = f"GM Sprint {sprint_num}"
    sprint_tasks=search_jql(Sprint_JQL.format(sprint_name))
    Sprint_Data.append({sprint_name: len(sprint_tasks)})
    qalabel=f"GM-QA-Sprint{sprint_num}"
    qa_sprint_jql = QA_SPRINT_LABEL_JQL.format(qalabel)
    qa_tasks=search_jql(qa_sprint_jql)
    dict_users = fetch_users(qa_tasks)

    Sprint_Data.append({qalabel: [dict_users,len(qa_tasks)]})
    prod_esc_jql = PROD_ESC_JQL.format(qalabel)
    prod_tasks=search_jql(prod_esc_jql)
    Sprint_Data.append({"Production Escalations": len(prod_tasks)})
    return Sprint_Data



def fetch_users(qa_tasks):
    """Fetch users from qa tasks"""
    dict_users=defaultdict(dict)    
    #users , status 
    for task in qa_tasks:
        reporter=task.get("reporter","Unknown")
        status=task.get("status","Unknown")
        if status == "Resolved":
            dict_users[reporter]["Resolved"] = dict_users[reporter].get("Resolved", 0) + 1
        elif status == "Verified":
            dict_users[reporter]["Verified"] = dict_users[reporter].get("Verified", 0) + 1
        elif status == "Open":
            dict_users[reporter]["Open"] = dict_users[reporter].get("Open", 0) + 1
        elif status == "Deployed":
             dict_users[reporter]["Deployed"] = dict_users[reporter].get("Deployed", 0) + 1
        dict_users[reporter]["total"] = dict_users[reporter].get("total", 0) + 1
    return dict_users
