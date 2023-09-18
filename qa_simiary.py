from typing import List, Tuple, Any, Union

class QA_Similarity():
    @staticmethod
    def get_words_similarity_score(input_words: List[str], qa_arguments: Tuple[str], q=None) -> List[Union[int,float]]:
        if not qa_arguments and not q:
            return [0, 0, []]
        tmp_q_score = 1 if q in input_words else 0
        tmp_total_q_score = 1 if q else 0
        tmp_hit_keyword_score, tmp_hit_keyword_list = QA_Similarity._get_score_by_a_list(input_words, qa_arguments)

        #关键词占比, 意图对应的没有a的情况直接取1
        tmp_total_score = len(qa_arguments) + tmp_total_q_score
        tmp_score = tmp_hit_keyword_score + tmp_q_score
        tmp_keyword_proportion = int(tmp_score) / tmp_total_score if 0 < tmp_total_score else 1
        #数量优先，其次占比
        return [tmp_score, tmp_keyword_proportion, tmp_hit_keyword_list]

    #依照评分给list排序
    @staticmethod
    def sort_by_mult_scores(to_be_sorted_list: List[Tuple[Any,List[
                                                                Union[int,float]
                                                                ]]]) -> None:
        to_be_sorted_list.sort(key=lambda x: (-x[1][0], -x[1][1], -x[1][-1]))

    @staticmethod
    def _get_score_by_a_list(input_words, a_list):
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