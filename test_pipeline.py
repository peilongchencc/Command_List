# hanlp.py
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 根据不同情况获取名称
        # 对于函数来说，使用 `func.__name__` 可以获得函数名称；但对于类的实例，需要使用 `func.__class__.__name__` 来获得实例对应的类的名称。
        func_name = getattr(func, "__name__", None) or func.__class__.__name__
        
        print(f"Function {func_name} took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper

import hanlp
HanLP = hanlp.pipeline() \
    .append(timing_decorator(hanlp.load('CTB9_TOK_ELECTRA_SMALL')), output_key='tok') \
    .append(timing_decorator(hanlp.load('CTB9_POS_ELECTRA_SMALL')), output_key='pos') \
    .append(timing_decorator(hanlp.load('MSRA_NER_ELECTRA_SMALL_ZH')), output_key='ner', input_key='tok') \
    .append(timing_decorator(hanlp.load('CTB9_DEP_ELECTRA_SMALL', conll=False)), output_key='dep', input_key='tok') \
    .append(timing_decorator(hanlp.load('CTB9_CON_ELECTRA_SMALL')), output_key='con', input_key='tok')

doc = HanLP(['急性肠胃炎要如何治疗？', '盛剑环境的股价太高了。'])
print(doc)
# 终端输出：
# Function TransformerTaggingTokenizer took 0.033004 seconds to execute.
# Function TransformerTagger took 0.030062 seconds to execute.
# Function TransformerNamedEntityRecognizer took 0.035365 seconds to execute.
# Function BiaffineDependencyParser took 0.035167 seconds to execute.
# Function CRFConstituencyParser took 0.064560 seconds to execute.