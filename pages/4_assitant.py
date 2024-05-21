import json
import streamlit as st
from openai import OpenAI
client = OpenAI()

# 检索您之前创建的Assistant
assistant_id = "asst_ej1UWKPK6jHIyqdMjhNDKwJQ"  # 你自己的助手ID
assistant = client.beta.assistants.retrieve(assistant_id)
print(assistant)
# 创建一个线程并同时创建消息
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "你好,我购买了一本书和一个电子产品,请帮我计算一下订单总价！",
        }
    ]
)
print(thread)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    # instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question."
)
# run
print(run)

# Run(id='run_KxD3WKkDL0pZtN3OdkOv1ZVO', assistant_id='asst_ej1UWKPK6jHIyqdMjhNDKwJQ', cancelled_at=None, completed_at=None, created_at=1716258884, expires_at=None, failed_at=1716258890, file_ids=[], instructions='test for geekbang', last_error=LastError(code='rate_limit_exceeded', message='You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.'), metadata={}, model='gpt-3.5-turbo-16k', object='thread.run', required_action=None, started_at=1716258884, status='failed', thread_id='thread_kq5lqZ31Tgpo1LIeF8vBxXjj', tools=[FunctionTool(
#     function=FunctionDefinition(name='calculate_order_total', description='根据多个商品类型和数量计算订单总价', parameters={'type': 'object', 'properties': {'items': {'type': 'array', 'items': {'type': 'object', 'properties': {'item_type': {'type': 'string', 'description': '商品类型,例如:书籍,文具,电子产品'}, 'quantity': {'type': 'integer', 'description': '商品数量'}}, 'required': ['item_type', 'quantity']}}}, 'required': ['items']}), type='function')], usage=Usage(completion_tokens=0, prompt_tokens=0, total_tokens=0), temperature=1.0, top_p=1.0, max_completion_tokens=None, max_prompt_tokens=None, truncation_strategy={'type': 'auto', 'last_messages': None}, incomplete_details=None, response_format='auto', tool_choice='auto')


# 读取function元数据信息
def get_function_details(run):
    function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
    arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    function_id = run.required_action.submit_tool_outputs.tool_calls[0].id
    return function_name, arguments, function_id


# 读取并打印元数据信息
function_name, arguments, function_id = get_function_details(run)
print("function_name:", function_name)
print("arguments:", arguments)
print("function_id:", function_id)

# 定义计算订单总价函数


def calculate_order_total(items):
    item_prices = {
        "书籍": 10,
        "文具": 5,
        "电子产品": 100
    }
    total_price = 0
    for item in items:
        price_per_item = item_prices.get(item['item_type'], 0)
        total_price += price_per_item * item['quantity']
    return total_price


# 根据Assistant返回的参数动态调用函数

arguments = '[{"item_type":"书籍","quantity":1},{"item_type":"电子产品","quantity":1}]'
# 将 JSON 字符串转换为字典
arguments_dict = {"items": json.loads(arguments)}

function_name = "calculate_order_total"
# 调用函数
order_total = globals()[function_name](**arguments_dict)

# 打印结果以进行验证
print(f"订单总价为: {order_total} 元")
