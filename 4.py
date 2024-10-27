# 添加智普langchain支持:
from langchain_community.chat_models import ChatZhipuAI


messages = [
    ("system", "你是一名专业的翻译家，可以将用户的中文翻译为英文。"),
    ("human", "我喜欢编程。"),
]
zhipuai_chat=ChatZhipuAI(model="glm-4-Flash",temperature= 0.99,
                    max_tokens=999999,api_key="9eb77fe2543c68240713c55742979c85.X54mEVPMMJk7WJGw")

a=zhipuai_chat.invoke(messages)
print(a.content)









from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from urllib.parse import quote  
from sqlalchemy import create_engine, select, Table, MetaData, Column, String
# from dotenv import load_dotenv
import os


# username = '1'
# passwd = '1'
# hostname = '1'
# port = '1'
db = SQLDatabase.from_uri("sqlite:///Test.db")


db_chain = SQLDatabaseChain(llm=zhipuai_chat, database=db, verbose=True)



b=db_chain.run("返回最大id号")

print("==============")
print(b)




