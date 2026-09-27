from model.initialization import agent

def invoke_agent(prompt, thread_id):
    config = {
        "configurable":{
            "thread_id": thread_id
        }
    }

    response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    },
    config=config
    )
    return  response["messages"][-1].content