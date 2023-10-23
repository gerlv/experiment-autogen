import autogen

config_list = autogen.config_list_from_models(model_list=["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"], exclude="aoai")

llm_config = {
    "functions": [
        {
            "name": "query_db",
            "description": "Query a database and return the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {
                        "type": "string",
                        "description": "age range to query",
                    },
                    "job_title": {
                        "type": "string",
                        "description": "job title to query",
                        "enum": ["engineer", "doctor", "lawyer", "teacher"],
                    },
                },
            },
        },
        {
            "name": "render_report",
            "description": "render the report to the user based on the query result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_result": {
                        "type": "array",
                        "description": "List of query result",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "name of the person",
                                },
                                "age": {
                                    "type": "integer",
                                    "description": "age of the person",
                                },
                                "job_title": {
                                    "type": "string",
                                    "description": "job title of the person",
                                },
                                "gender": {
                                    "type": "string",
                                    "description": "Gender of the person",
                                    "enum": ["male", "female", "other", "unknown"],
                                },
                            },
                        },
                    }
                },
                "required": ["query_result"],
            },
        },
    ],
    "config_list": config_list,
    "request_timeout": 120,
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="Your task is to help the user to query the database and render the report. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
)


def query_db(**kwargs):
    print("query_db called with params:", kwargs)
    return [
        {
            "name": "John",
            "age": 30,
            "job_title": "engineer",
            "gender": "male"
        },
        {
            "name": "Mary",
            "age": 25,
            "job_title": "engineer",
            "gender": "female",
        }
    ]


def render_report(query_result):
    print("render_report called with params:", query_result)
    return "Here is the report..."


user_proxy.register_function(
    function_map={
        "query_db": query_db,
        "render_report": render_report,
    }
)

user_proxy.initiate_chat(
    chatbot,
    message="Fetch me a report of all engineers.",
)
