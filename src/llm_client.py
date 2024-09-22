import openai
from openai import OpenAI


class LLMClient:
    def __init__(self, api_key, model_type='openai'):
        self.api_key = api_key
        self.model_type = model_type
        self.max_length = 6000  # 设置最大输入长度

    def summarize_report(self, content):
        # 检查内容长度，并根据模型类型调用相应的方法
        if len(content) > self.max_length:
            parts = self._split_content(content)
            summaries = []

            for part in parts:
                if self.model_type == 'openai':
                    summaries.append(self._summarize_with_openai(part))
                elif self.model_type == 'chatGlm':
                    summaries.append(self._summarize_with_chat_glm(part))
                elif self.model_type == 'deepseek':
                    summaries.append(self._summarize_with_deepseek(part))
                elif self.model_type == 'tongyi':
                    summaries.append(self._summarize_with_tongyiqianwen(part))
                else:
                    raise ValueError("Unsupported model type.")

            return "\n\n".join(summaries)  # 合并所有部分的总结

        # 内容未超出长度限制，直接调用相应的总结方法
        if self.model_type == 'openai':
            return self._summarize_with_openai(content)
        elif self.model_type == 'chatGlm':
            return self._summarize_with_chat_glm(content)
        elif self.model_type == 'deepseek':
            return self._summarize_with_deepseek(content)
        elif self.model_type == 'tongyi':
            return self._summarize_with_tongyiqianwen(content)
        else:
            raise None

    def _split_content(self, content):
        """根据最大长度分割内容"""
        parts = []
        while len(content) > self.max_length:
            # 找到最后一个空格以避免在单词中间分割
            split_index = content.rfind(' ', 0, self.max_length)
            if split_index == -1:  # 如果没有找到空格，就硬切
                split_index = self.max_length

            parts.append(content[:split_index])
            content = content[split_index:].strip()  # 剩余内容去除前后空白

        # 添加最后一部分
        if content:
            parts.append(content)

        return parts

    def _summarize_with_openai(self, content):
        """使用 OpenAI GPT-4 API 生成总结"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个优秀的项目总结助手。"},
                {"role": "user", "content": f"请根据以下内容生成一个项目每日报告,用中文回复:\n\n{content}"}
            ]
        )

        summary = response['choices'][0]['message']['content']
        return summary

    def _summarize_with_chat_glm(self, content):
        """使用智谱清言 API 生成总结"""
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        completion = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "system", "content": "你是一个优秀的项目总结助手。"},
                {"role": "user", "content": f"请根据以下内容生成一个项目每日报告,用中文回复:\n\n{content}"}
            ],
            top_p=0.7,
            temperature=0.9
        )
        summary = completion.choices[0].message.content
        return summary

    def _summarize_with_deepseek(self, content):
        """使用 DeepSeek API 生成总结"""
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个优秀的项目总结助手。"},
                {"role": "user", "content": f"请根据以下内容生成一个项目每日报告,用中文回复:\n\n{content}"},
            ],
            stream=False
        )
        summary = response.choices[0].message.content
        return summary


    def _summarize_with_tongyiqianwen(self, content):
        """使用通义千问 API 生成总结"""
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {'role': 'system', 'content': '你是一个优秀的项目总结助手。'},
                {'role': 'user', 'content': f"请根据以下内容生成一个项目每日报告,用中文回复:\n\n{content}"}
            ]
        )

        summary = completion.choices[0].message.content
        return summary
