""" source: https://python-sonarqube-api.readthedocs.io/en"""

from sonarqube import SonarQubeClient
from pprint import pprint

GOAUTH_TOKEN = "6219cfc300bb234f10957072917f72cde8c6ba8b"

client = SonarQubeClient(
    sonarqube_url="http://localhost:9000",
    username="admin",
    password="HarshalC7!"
)

# Get all projects
def get_all_projects():
    projects = list(client.projects.search_projects())
  
    """response:
    [{'key': 'pymongo',
    'lastAnalysisDate': '2022-02-23T19:51:32+0530',
    'name': 'pymongo',
    'qualifier': 'TRK',
    'visibility': 'public'}]
    """
    return projects

# Create new project
def create_project(project, name, visibility="private"):
    """Creates new project

    Args:
        project (string): project key
        name (string): name of the project
        visibility (str, optional): Wether to keep private or public. Defaults to "private".

    Returns:
        error: Returns None if creation successful, else error
    """
    try:
        response = client.projects.create_project(project, name, visibility)
        print(response)
        return None
    except Exception as e:
        print(e)
        return f"Error while creating project {project}: {e}"
        

# Get issues
def get_issues_by_project_key(project_key):
    issues = list(client.issues.search_issues(componentKeys=project_key))
    return issues


# Get source code
def get_code(key, from_line, to_line):
    """Returns source code from the file

    Args:
        key (string): location of the file within the project
        from_line (int): line from which we want to get the code
        to_line (int): line till which we want to get the code

    Returns:
        string: code block
    """
    scm = client.sources.get_source_code(key=key, from_line=from_line, to_line=to_line)
    
    """get_code("pymongo:crud.py", from_line=1, to_line=5)
    response:
    {'sources': [[1,
                 '<span class="k">from</span> py_crud <span '
                 'class="k">import</span> <span class="sym-1 sym">mongo</span>'],
                [2,
                 '<span class="k">from</span> app <span class="k">import</span> '
                 '<span class="sym-2 sym">app</span>'],
                [3,
                 '<span class="k"><span class="sym-3 sym">from</span> '
                 'py_crud.models.project <span class="k">import</span> *</span>'],
                [4, ''],
                [5,
                 '<span class="k">if</span> __name__ == <span '
                 'class="s">"__main__"</span>:']]}
    """
    
    return scm

# Get Quality gate status of a project
def get_quality_status(project_key, branch="master"):
    """Get quality status

    Args:
        project_key (string): key of the project
        branch (str, optional): branch of the project. Defaults to "master".

    Returns:
        object: status of the branch of that project
    """
    qualitygates_status = client.qualitygates.get_project_qualitygates_status(projectKey=project_key, branch=branch)
    """response
    {'projectStatus': {'conditions': [],
                       'ignoredConditions': False,
                       'periods': [],
                       'status': 'OK'}}
    """
    return qualitygates_status


# Get component
def get_component(project_key):
    component = client.components.get_project_component_and_ancestors(project_key)
    
    """response: 
    {'ancestors': [],
     'component': {'analysisDate': '2022-02-23T19:51:32+0530',
                   'key': 'pymongo',
                   'name': 'pymongo',
                   'needIssueSync': False,
                   'qualifier': 'TRK',
                   'tags': [],
                   'version': '1.0',
                   'visibility': 'public'}}
    """
    return component

# Get measures of a project component
def get_measures(project_key, branch="master", metric_keys="code_smells,bugs,vulnerabilities"):
    components = list(client.measures.get_component_tree_with_specified_measures(
        component=project_key, 
        branch=branch,
        metricKeys=metric_keys
    ))
    """response:
        {'key': 'pymongo:py_crud/__init__.py',
         'language': 'py',
         'measures': [{'bestValue': True, 'metric': 'code_smells', 'value': '0'},
                      {'bestValue': True, 'metric': 'bugs', 'value': '0'},
                      {'bestValue': True, 'metric': 'vulnerabilities', 'value': '0'}],
         'name': '__init__.py',
         'path': 'py_crud/__init__.py',
         'qualifier': 'FIL'},
    """
    return components

if __name__ == "__main__":
    pprint(get_code(key="pymongo:crud.py", from_line=3, to_line=3))