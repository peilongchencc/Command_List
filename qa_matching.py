class SynonymReplacing():
    def __init__(self):
        self._std_id_word_group_map = {}
    #end of init
    def add_word_group(self, std_id, synonym_word_group):
        text_word_group_map = {}
        list_word_group_map = {}
        self._std_id_word_group_map[std_id] = {
            'text': text_word_group_map,
            'list': list_word_group_map,
        }
        for item in synonym_word_group:
            for word in item:
                if isinstance(word, list):
                    tmp_map = list_word_group_map
                else:
                    tmp_map = text_word_group_map
                tmp_list = tmp_map.get(item[0], [])
                tmp_list.append(word)
                tmp_map[item[0]] = tmp_list
        #end of for 近义词群
    #end of add_word_group
    def word_synonym_replacing(self, word, std_id):
        tmp_word_group = self._std_id_word_group_map[std_id]['text']
        return SynonymReplacing._get_synonym_word(word, tmp_word_group)
    #end of text_synonym_replacing
    def word_list_replacing(self, word_list, std_id):
        tmp_list = []
        tmp_word_group = self._std_id_word_group_map[std_id]['text']
        for word in word_list:
            tmp_list.append(SynonymReplacing._get_synonym_word(word, tmp_word_group))
        return tmp_list
    @staticmethod
    def _get_synonym_word(word_name, word_group):
        for key in word_group:
            if word_name not in word_group[key]:
                continue
            return key
        return word_name
    #end of _get_synonym_word

class AnswerStem:
    def __init__(self, intent_id: str, intent_name: str, intent_tag: str, std_id: str, std_question: str, timestamp: float):
        self.id = intent_id
        self.intent = intent_name
        self.intent_tag = intent_tag
        self.std_id = std_id
        self.std_question = std_question
        self.timestamp = timestamp

    def __str__(self):
        return (
            f"\t{{\n"
            f"\t\tid: {self.id}\n"
            f"\t\tintent: {self.intent}\n"
            f"\t\tstd_question: {self.std_question}\n"
            f"\t}}"
        )


class KeyRule():
    def __init__(self,interro_pron:str, predicates: List[str], arguments:List[str], word_group:List[List[str]],cnw_flag, matcher):
        self._interro_pron = interro_pron
        self._predicates = predicates
        self._arguments = arguments
        # self._vague_arguments = [interro_pron, predicate] + list(arguments)
        self._word_group = word_group
        self._pa = predicates + arguments
        self._cnw_flag = cnw_flag
        self._matcher = matcher
    #end of __init__

    #start of getters
    def get_interro_pron(self):
        return self._interro_pron
    #end of get_interro_prons
    def get_predicates(self):
        return self._predicates
    #end of get_predicates
    def get_arguments(self):
        return self._arguments
    #end of get_arguments_list
    # def get_vague_arguments(self) -> List[str]:
    #     return self._vague_arguments
    #end of get_vague_arguments
    def get_word_group(self):
        return self._word_group
    #end of get_word_group
    def get_pa(self) -> List[str]:
        return self._pa
    #end of get_pa
    def get_cnw_flag(self):
        return self._cnw_flag
    #end of get_cnw_flag
    def get_souldims(self):
        return self._matcher.get_souldims()
    #end of getters
    def match(self, souldims, verbs):
        return self._matcher.match(souldims, verbs)

class QuestionAnswer():
    def __init__(self, stem: AnswerStem, group: int, key_rule:KeyRule=None):
        self._stem = stem
        self._group = group
        self._key_rule = key_rule
    # end of __init__

    # start of getters
    def get_group(self):
        return self._group
    def get_key_rule(self):
        return self._key_rule
    def get_stem(self):
        return self._stem


class Matcher():
    def __init__(self, souldims, verbs, verb_groups, only):
        self._verb_groups = verb_groups
        self._verbs = self._replace_verbs(verbs)
        self._souldims_weight = 100 * len(souldims)
        self._verb_weight = 10 * len(verbs)
        self._only = only
        self._souldims = souldims
        if 0 == len(self._souldims) == len(self._verbs):
            self._only = False
    #end of init
    def get_souldims(self):
        return self._souldims
    # end of get_souldims
    def match(self, souldims, verbs):
        if self._only:
            return 0, self._is_all_match(souldims, verbs)
        tmp_score = 0
        tmp_score += self._get_score(souldims, self._souldims, self._souldims_weight)
        if 0 >= tmp_score:#业务实体没对上直接跳过
            return 0, False
        # 暂时关闭谓语维度评分
        # tmp_verbs = self._replace_verbs(verbs)
        # tmp_score += self._get_score(tmp_verbs, self._verbs, self._verb_weight)
        # tmp_score += self._get_score(ask_methods, self._ask_methods, self._ask_method_weight)
        return tmp_score, False
    #end of match

    @staticmethod
    def _get_score(inputs, data, weight):
        # data = [[a,b],[c,d]]
        # inputs = [a, b, c,d]
        if not data or not inputs:
            return 0
        for dimension_group in data:
            tmp_flag = True
            for dimension in inputs:
                if dimension in dimension_group:
                    tmp_flag = False
                    break
            #end of for business_entities
            if tmp_flag:
                return 0
        return weight
    #end of _check_business_entities
    def _replace_verbs(self, verbs):
        tmp_verb_list = []
        for verb in verbs:
            tmp_flag = True
            for verb_group in self._verb_groups:
                if verb not in verb_group:
                    continue
                tmp_flag = False
                tmp_verb_list.append(verb_group[0])
            #end of for self._verb_groups
            if tmp_flag:
                tmp_verb_list.append(verb)
        return tmp_verb_list
    #end of _replace_verbs

    def _is_all_match(self, souldims, verbs):
        for i in self._verbs:
            if i not in verbs:
                return False
        tmp_souldims_list = []
        tmp_count = 0
        for i in self._souldims:
            for j in souldims:
                if j not in tmp_souldims_list and j in i:
                    tmp_count += 1
                    tmp_souldims_list.append(j)
                    break
        if tmp_count == len(self._souldims):
            return True
        return False

from typing import List
from answer.matching.qa_matching.qa_similarity import QA_Similarity
from answer.eneities.entities import QA_Result
from nazhi_nlp_server_lib.interro_analysing.entities import InterroPron
from nazhi_nlp_server_lib.utils.stock_intent_checking import FundJudge
class QA_Matching():
    def __init__(self, qa_list, qa_dict, replacing):
        self._qa_list = qa_list
        self._qa_dict = qa_dict
        self._replacing = replacing
    #end of init

    #start of public methods
    def get_replacing(self):
        return self._replacing
    #end of get_replacing
    def match(self, intent_tags, text, q, p_list, keyword_list, wordnet_dict, dimension_list) -> List[QA_Result]:
        tmp_cn = FundJudge.get_cn_fund(text,wordnet_dict)#todo 场内场外基金
        tmp_cw = FundJudge.get_cw_fund(text,wordnet_dict)

        tmp_vague_list = [q] + keyword_list
        #用intent_tag过滤
        tmp_qa_list = self._intent_tag_filter(self._qa_list, intent_tags)
        #用matcher做维度过滤
        tmp_result, tmp_is_only = self._qa_match(tmp_qa_list, p_list, self._replacing, dimension_list)
        if tmp_is_only:
            return [QA_Result(tmp_result.get_stem(), [], False, tmp_result.get_key_rule())]
        #按结果优先级分别排序
        tmp_qa_result_list = []
        for score, qa_list in tmp_result:
            tmp_qa_result_list += self._search_answer_list(qa_list, self._qa_dict, q, p_list,
                                                                         keyword_list, tmp_vague_list,
                                                                         self._replacing, tmp_cn, tmp_cw, score)
        tmp_qa_result_list = self._qa_result_filter(tmp_qa_result_list)
        tmp_qa_result_list = tmp_qa_result_list[:min(10, len(tmp_qa_result_list))]  # 取前10个，维度匹配的优先，精确匹配结果优先
        print('-'*50)
        return tmp_qa_result_list
    #end of match
    #end of public methods

    #start of private methods

    @classmethod
    def _search_answer_list(cls, qa_list, qa_dict, q, p_list, keyword_list, vague_list, replacing, fund_cn,fund_cw, score):
        """
        qa_dict = {
            0: {
                'intent1_1': [<qa.question_answer.QuestionAnswer 1>, <qa.question_answer.QuestionAnswer 2>],
                'intent1_2': [<qa.question_answer.QuestionAnswer 3>]
                },
            1: {
                'intent2': [<qa.question_answer.QuestionAnswer 4>]
                }
            }
        """
        #关键词匹配结果
        tmp_keyword_qa_result_list = cls._filter_by_keyword(keyword_list, qa_list, replacing)
        #关键词匹配结果按评分排序
        QA_Similarity.sort_by_mult_scores(tmp_keyword_qa_result_list)
        if 1 == len(keyword_list) or q == InterroPron.UNK:
            #只输入一个词或者问句形式为unk时返回去重后的关键词匹配结果
            return cls._vag_result_filter(tmp_keyword_qa_result_list,
                                                              intent_id_list=[],
                                                              fund_cn=fund_cn,
                                                              fund_cw=fund_cw,
                                                              score=score)
        #按qpa筛选出精确和模糊结果
        tmp_keyword_qa_result_list = tmp_keyword_qa_result_list[:100]
        tmp_accurate_qa_score_list, tmp_vague_qa_score_list = cls._filter_by_qpa(tmp_keyword_qa_result_list,
                                                                                     q, p_list, keyword_list, vague_list, replacing)
        #精确结果按评分顺序排序
        QA_Similarity.sort_by_mult_scores(tmp_accurate_qa_score_list)
        #模糊结果按评分顺序排序
        QA_Similarity.sort_by_mult_scores(tmp_vague_qa_score_list)
        tmp_intent_id_list = []
        #精确结果过滤, 去重, 并找出意图相关结果
        tmp_accurate_result_list, tmp_relevant_result_list = cls._acc_result_filter_and_get_relevant(tmp_accurate_qa_score_list,
                                                                                                                         tmp_vague_qa_score_list,
                                                                                                                         tmp_intent_id_list,
                                                                                                                         qa_dict,fund_cn,fund_cw,
                                                                                                                         score=score)
        #模糊结果过滤, 去重
        tmp_vague_result_list = cls._vag_result_filter(tmp_vague_qa_score_list,
                                                                           tmp_intent_id_list,
                                                                           fund_cn,fund_cw,
                                                                           score=score)
        return cls._concat_result(tmp_accurate_result_list,
                                                      tmp_relevant_result_list,
                                                      tmp_vague_result_list)
    #end of _get_qa_stem_list
    @staticmethod
    def _intent_tag_filter(qa_list, intent_tags):
        if not intent_tags:
            return qa_list
        tmp_list = []
        for qa in qa_list:
            tmp_intent_tag = qa.get_stem().intent_tag
            if tmp_intent_tag not in intent_tags:
                continue
            tmp_list.append(qa)
        return tmp_list
    #end of _intent_tag_filter
    @staticmethod
    def _qa_match(qa_list, p_list, replacing, dimension_list):
        tmp_qa_score_dict = {}
        for qa in qa_list:
            tmp_std_id = qa.get_stem().std_id
            tmp_p_list = replacing.word_list_replacing(p_list, tmp_std_id)
            tmp_key_rule = qa.get_key_rule()
            tmp_score, tmp_is_only = tmp_key_rule.match(dimension_list,
                                            tmp_p_list)
            tmp_score = str(tmp_score)
            if tmp_is_only:
                return qa, True

            tmp_qa_list = tmp_qa_score_dict.get(tmp_score)
            if not tmp_qa_list:
                tmp_qa_list = []
                tmp_qa_score_dict[tmp_score] = tmp_qa_list
            tmp_qa_list.append(qa)
        return sorted(tmp_qa_score_dict.items(), key=lambda d: d[0], reverse=True), False
    #end of _qa_match
    @staticmethod
    def _filter_by_keyword(word_list, qa_list, replacing):
        tmp_keyword_qa_result_list = []
        for qa in qa_list:
            tmp_std_id = qa.get_stem().std_id
            tmp_key_rule = qa.get_key_rule()
            tmp_word_list = replacing.word_list_replacing(word_list, tmp_std_id)
            tmp_score_list = QA_Similarity.get_words_similarity_score(tmp_word_list, tmp_key_rule.get_pa())
            tmp_score_list.append(qa.get_stem().timestamp)
            tmp_keyword_qa_result_list.append((qa, tmp_score_list))
        return tmp_keyword_qa_result_list
    #end of _filter_by_keyword
    @staticmethod
    def _filter_by_qpa(keyword_qa_result_list, q, p_list, keyword_list, vague_list, replacing):
        tmp_accurate_qa_score_list = []
        tmp_vague_qa_score_list = []
        for qa, score_list in keyword_qa_result_list:
            tmp_std_id = qa.get_stem().std_id
            tmp_key_rule = qa.get_key_rule()
            tmp_keyword_list = replacing.word_list_replacing(keyword_list, tmp_std_id)
            tmp_vague_list = replacing.word_list_replacing(vague_list, tmp_std_id)
            tmp_p_list_replace = replacing.word_list_replacing(p_list, tmp_std_id)
            tmp_flag = True
            for predicate in tmp_key_rule.get_predicates():
                if predicate not in tmp_p_list_replace:
                    tmp_flag = False
                    break
            #end of for 检查谓语是否都出现
            if tmp_flag and q == tmp_key_rule.get_interro_pron():
                tmp_score_list = QA_Similarity.get_words_similarity_score(tmp_keyword_list, tmp_key_rule.get_pa())
                tmp_score_list.append(qa.get_stem().timestamp)
                if sum(tmp_score_list[:2]) >= (len(tmp_key_rule.get_pa()) + 1.0):
                    tmp_accurate_qa_score_list.append((qa, tmp_score_list))
            tmp_score_list = QA_Similarity.get_words_similarity_score(tmp_vague_list, tmp_key_rule.get_pa(),
                                                                      q=tmp_key_rule.get_interro_pron())
            tmp_score_list.append(qa.get_stem().timestamp)
            tmp_vague_qa_score_list.append((qa, tmp_score_list))
        return tmp_accurate_qa_score_list, tmp_vague_qa_score_list
    #end of _match_by_qpa
    @staticmethod
    def _is_too_short_acc_result(acc_score_list, vague_result_list):
        if 0 >= len(vague_result_list):
            return False
        if int(sum(acc_score_list[:2])) > 2:
            return False
        #一个以下论元匹配+100%占比
        vague_result = vague_result_list[0]
        if 4 >= int(vague_result[1][0]):
            return False
        return True
    #end of _is_too_short_acc_result
    @staticmethod
    def _qa_result_filter(qa_result_list):
        tmp_list = []
        tmp_intent_id_list = []
        for qa_result in qa_result_list:
            tmp_intent_id = qa_result.get_answer_stem().id
            if tmp_intent_id in tmp_intent_id_list:
                continue
            tmp_intent_id_list.append(tmp_intent_id)
            tmp_list.append(qa_result)
        return tmp_list
    @staticmethod
    def _vag_result_filter(vag_qa_score_list, intent_id_list,fund_cn,fund_cw,score):
        #同意图去重, 把评分全部为0的过滤掉
        tmp_list = []
        for qa, score_list in vag_qa_score_list:
            if 0 >= score_list[0]:
                continue
            print(qa.get_stem().std_question, score_list, 'vag', f'score: {score}')
            if qa.get_stem().id in intent_id_list:
                continue
            if fund_cn and not fund_cw and qa.get_key_rule().get_cnw_flag() == fund_cw:
                continue
            if fund_cw and not fund_cn and qa.get_key_rule().get_cnw_flag() == fund_cn:
                continue
            intent_id_list.append(qa.get_stem().id)
            tmp_list.append(QA_Result(qa.get_stem(), score_list, False, qa.get_key_rule()))
        return tmp_list
    #end of _vag_result_filter
    @classmethod
    def _acc_result_filter_and_get_relevant(cls, accurate_qa_score_list, vague_qa_score_list, intent_id_list, qa_dict,fund_cn,fund_cw, score):
        #精确匹配的结果去重, 过滤, 追加其他分支答案
        tmp_acc_result_list = []
        tmp_relevant_result_list = []
        for qa, score_list in accurate_qa_score_list:
            if 0 >= score_list[0]:
                continue
            print(qa.get_stem().std_question, score_list, 'acc', f'score: {score}')
            if qa.get_stem().id in intent_id_list:
                continue
            if fund_cn and not fund_cw and qa.get_key_rule().get_cnw_flag()==fund_cw:
                continue
            if fund_cw and not fund_cn and qa.get_key_rule().get_cnw_flag()==fund_cn:
                continue
            #精确匹配到过短句子时，多进行一次分析
            if cls._is_too_short_acc_result(score_list, vague_qa_score_list):
                continue
            intent_id_list.append(qa.get_stem().id)
            tmp_acc_result_list.append(QA_Result(qa.get_stem(), score_list, True, qa.get_key_rule()))
            tmp_group = qa.get_group()
            if 1 == len(qa_dict[tmp_group].keys()):
                continue
            for intent_id in qa_dict[tmp_group].keys():
                if intent_id == qa.get_stem().id:
                    continue
                tmp_qa = qa_dict[tmp_group][intent_id][0]
                tmp_stem = tmp_qa.get_stem()
                if tmp_stem.id in intent_id_list:
                    continue
                intent_id_list.append(tmp_stem.id)
                tmp_relevant_result_list.append(QA_Result(tmp_qa.get_stem(), [0, 0, 0], False, tmp_qa.get_key_rule()))
        return tmp_acc_result_list, tmp_relevant_result_list
    #end of _acc_result_filter_and_get_relevant
    @staticmethod
    def _concat_result(accurate_result_list, relevant_result_list, vague_result_list):
        tmp_end_index = 0
        for qa_result in vague_result_list:
            if 4 > qa_result.get_score_list()[0]:
                break
            tmp_end_index += 1
        return accurate_result_list + vague_result_list[:tmp_end_index] + relevant_result_list + vague_result_list[tmp_end_index:]
    #end of private methods
#end of class FinancialAnswerMatching


class QA_MatchingBuilder():
    @staticmethod
    def build(question_metadata):
        tmp_replacing = SynonymReplacing()
        tmp_QA_list = []
        tmp_QA_dict = {}
        for group in range(len(question_metadata)):
            tmp_QA_dict[group] = {}
            for item in question_metadata[group]:
                tmp_intent_id = item['id']
                tmp_intent_name = item['intent']
                tmp_intent_tag = item['intent_tag']

                if tmp_QA_dict[group].get(tmp_intent_id) is None:
                    tmp_QA_dict[group][tmp_intent_id] = []
                for std_question_item in item['std_questions']:
                    tmp_std_question = std_question_item['std_question']
                    tmp_timetsamp = std_question_item['timestamp']
                    tmp_std_id = std_question_item['std_id']
                    tmp_key_rule_dict = std_question_item['key_rule']
                    tmp_interro_pron = tmp_key_rule_dict['interro_pron']
                    tmp_predicates = tmp_key_rule_dict['predicates']
                    tmp_arguments = tmp_key_rule_dict['arguments']
                    tmp_word_group = tmp_key_rule_dict['word_group']

                    if 'matcher' in std_question_item.keys():
                        tmp_souldims = std_question_item['matcher']['souldims']
                        tmp_only = std_question_item['matcher'].get('only', False)
                        tmp_matcher = Matcher(tmp_souldims, tmp_predicates, tmp_word_group, tmp_only)
                    else:
                        tmp_matcher = Matcher([], [], [], False)
                    tmp_cnw_flag = tmp_key_rule_dict['cnw_flag'] if 'cnw_flag' in tmp_key_rule_dict else None
                    tmp_replacing.add_word_group(tmp_std_id, tmp_word_group)
                    tmp_qa_stem = AnswerStem(tmp_intent_id, tmp_intent_name, tmp_intent_tag, tmp_std_id, tmp_std_question, float(tmp_timetsamp))
                    tmp_arguments = [tmp_replacing.word_synonym_replacing(argument, tmp_std_id) for argument in tmp_arguments]
                    tmp_predicates = [tmp_replacing.word_synonym_replacing(predicate, tmp_std_id) for predicate in tmp_predicates]
                    tmp_key_rule = KeyRule(tmp_interro_pron, tmp_predicates, tmp_arguments, tmp_word_group,tmp_cnw_flag, tmp_matcher)
                    tmp_question_answer = QuestionAnswer(tmp_qa_stem, group, tmp_key_rule)

                    tmp_QA_list.append(tmp_question_answer)
                    tmp_QA_dict[group][tmp_intent_id].append(tmp_question_answer)
        return QA_Matching(tmp_QA_list, tmp_QA_dict, tmp_replacing)