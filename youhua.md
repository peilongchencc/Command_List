将`QA_Similarity`类转为常规方法后，你可以将这些方法放在一个普通的类中，而不是使用静态方法。以下是如何转换为常规方法的示例：

```python
from typing import List, Tuple, Any, Union

class SimilarityCalculator:
    def __init__(self, input_words: List[str], qa_arguments: Tuple[str], q=None):
        self.input_words = input_words
        self.qa_arguments = qa_arguments
        self.q = q

    def get_words_similarity_score(self) -> List[Union[int, float]]:
        if not self.qa_arguments and not self.q:
            return [0, 0, []]
        tmp_q_score = 1 if self.q in self.input_words else 0
        tmp_total_q_score = 1 if self.q else 0
        tmp_hit_keyword_score, tmp_hit_keyword_list = self._get_score_by_a_list(self.input_words, self.qa_arguments)

        # 关键词占比, 意图对应的没有a的情况直接取1
        tmp_total_score = len(self.qa_arguments) + tmp_total_q_score
        tmp_score = tmp_hit_keyword_score + tmp_q_score
        tmp_keyword_proportion = int(tmp_score) / tmp_total_score if 0 < tmp_total_score else 1
        # 数量优先，其次占比
        return [tmp_score, tmp_keyword_proportion, tmp_hit_keyword_list]

    # 依照评分给list排序
    def sort_by_mult_scores(self, to_be_sorted_list: List[Tuple[Any, List[Union[int, float]]]]) -> None:
        to_be_sorted_list.sort(key=lambda x: (-x[1][0], -x[1][1], -x[1][-1]))

    def _get_score_by_a_list(self, input_words, a_list):
        tmp_hit_keyword_score = 0  # 命中的必要关键词数量
        tmp_hit_keyword_list = []
        for a in a_list:
            if a not in input_words:
                continue
            tmp_index = input_words.index(a)
            tmp_hit_keyword_score += 1
            input_words.pop(tmp_index)
            tmp_hit_keyword_list.append(a)
        return tmp_hit_keyword_score, tmp_hit_keyword_list
```

现在，你可以创建一个`SimilarityCalculator`的实例并调用其方法来计算相似性分数，例如：

```python
input_words = ["apple", "banana", "cherry"]
qa_arguments = ("apple", "banana")
q = "cherry"

calculator = SimilarityCalculator(input_words, qa_arguments, q)
similarity_score = calculator.get_words_similarity_score()
print(similarity_score)
```