# Experiments with Autogen

This is a repository for experiments with [Autogen](https://github.com/autogen/autogen).

## Installation

Requires Python3.10 and Poetry 1.6.1+.

```bash
poetry install
```

## [Function calling](./experiments_autogen/function_calling.py)

```text
user_proxy (to chatbot):

Fetch me a report of all engineers.

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested function Call: query_db *****
Arguments:
{
  "job_title": "engineer"
}
*********************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION query_db...
query_db called with params: {'job_title': 'engineer'}
user_proxy (to chatbot):

***** Response from calling function "query_db" *****
[{'name': 'John', 'age': 30, 'job_title': 'engineer', 'gender': 'male'}, {'name': 'Mary', 'age': 25, 'job_title': 'engineer', 'gender': 'female'}]
*****************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested function Call: render_report *****
Arguments:
{
  "query_result": [
    { "name": "John", "age": 30, "job_title": "engineer", "gender": "male" },
    {"name": "Mary", "age": 25, "job_title": "engineer", "gender": "female"}
  ]
}
**************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION render_report...
render_report called with params: [{'name': 'John', 'age': 30, 'job_title': 'engineer', 'gender': 'male'}, {'name': 'Mary', 'age': 25, 'job_title': 'engineer', 'gender': 'female'}]
user_proxy (to chatbot):

***** Response from calling function "render_report" *****
Here is the report...
**********************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

TERMINATE
```
