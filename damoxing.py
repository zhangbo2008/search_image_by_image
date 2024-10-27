print('免费的大模型调用api')

import requests,json

if 1:
            data=[    {
                    "role": "system",
                    "content": "请回答下面问题"
                },

                {
                    "role": "user",
                    "content": "2+2等于多少"

                }

            ]      
                        
            if 1:
                print('传入的参数',data)
                # yiyao=aaa['med']
                # yonghu=aaa['user']
                # 保存json
                from zhipuai import ZhipuAI

                client = ZhipuAI(api_key="9eb77fe2543c68240713c55742979c85.X54mEVPMMJk7WJGw")


                import time
                aaaaa=time.time()
                response = client.chat.completions.create(
                model="glm-4-Flash",
                    messages=data,
                    top_p= 1,
                    temperature= 0.99,
                    max_tokens=999999,
                    tools = [{"type":"web_search","web_search":{"search_result":False}}],
                    stream=False,
                )
                import json
                dict()
                a=response.choices[0].message.content
                print('大模型结果',a)