from sanic import Sanic
from sanic.response import json
import jieba

app = Sanic("jieba-segment")


@app.route("/seg_ment", methods=["POST"])
async def seg_ment(request):
    """分词API"""
    text = request.form.get("user_input")    # postman 测试时字段的名称需要对应，此处写"user_input"，postman写"input"就会报错。
    if not text:
        return json({"error": "缺少 \"user_input\" parameter"}, status=400) # \ 用于转义
    # 进行jieba分词处理
    text_segment = jieba.lcut(text)
    return json({"用户输入的分词结果为：": text_segment})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)