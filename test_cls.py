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
#end of class Matcher

tmp_matcher = Matcher(tmp_souldims, tmp_predicates, tmp_word_group, tmp_only)

tmp_matcher = Matcher([], [], [], False)

