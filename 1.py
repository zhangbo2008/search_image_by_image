#========这个是项目的主程序

# 添加智普langchain支持:
from langchain_community.chat_models import ChatZhipuAI


messages = [
    ("system", "你是一名专业的翻译家，可以将用户的中文翻译为英文。"),
    ("human", "我喜欢编程。"),
]
zhipuai_chat=ChatZhipuAI(model="glm-4-Flash",temperature= 0.99,
                    max_tokens=999999,api_key="9eb77fe2543c68240713c55742979c85.X54mEVPMMJk7WJGw")

# a=zhipuai_chat.invoke(messages)
# print(a.content)









from langchain_community.utilities import SQLDatabase
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















input="返回药品数据的数量"














top_k=10
_sqlite_prompt = f"""You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""


_sqlite_prompt = """你是一位SQLite专家。对于给定的输入问题，首先创建一个语法正确的SQLite查询来运行。 除非用户在问题中指定了要获取的具体示例数量，否则使用LIMIT子句按照SQLite的要求查询最多10个结果。你可以对结果进行排序，以返回数据库中最信息丰富的数据。 永远不要查询表中的所有列。你必须只查询回答问题所需的列。将每个列名用双引号（"）括起来，以将它们标识为限定标识符。 注意只使用你在以下表格中可以看到的列名。小心不要查询不存在的列。同时注意哪个列在哪个表中。 注意，如果问题涉及到“今天”，使用date('now')函数来获取当前日期。"""


PROMPT_SUFFIX = f"""只使用下面的表:
{db.table_info}

"""

template=_sqlite_prompt + PROMPT_SUFFIX


# b=db_chain.run("返回最大id号")




messages = [
    ("system", template),
    ("human", f"问题是: {input}"),
]
print("==============")
print("提示词",messages)
a=zhipuai_chat.invoke(messages)
print('使用的sql:')
qqq=a.content.replace('```','').replace('sql','')

print(qqq)

qqq2=db._execute(qqq)
print('得到的结果:')
print(qqq2)