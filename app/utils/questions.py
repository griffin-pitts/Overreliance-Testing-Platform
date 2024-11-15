def get_initial_recommendation(question_index):
    question = questions[question_index]
    return {
        'question': question['question'],
        'recommendation': question['initial_recommendation'],
        'is_misleading': question['is_misleading']
    }

def get_chat_prompt(question_index):
    question = questions[question_index]
    return question['chat_prompt']

questions = [
    # Correct Recommendations (14 questions)
    {
        'question': 'What will be the output of print(tuple(set([1,2,2,3,3,3,4,4,4,4])))?',
        'options': ['(1, 2, 3, 4)', '(4, 3, 2, 1)', '[1, 2, 3, 4]', 'TypeError'],
        'correct': '(1, 2, 3, 4)',
        'is_misleading': False,
        'initial_recommendation': 'This will output (1, 2, 3, 4). The set removes duplicates, and converting to tuple maintains the unique elements.',
        'chat_prompt': {
            'system_context': 'You are a Python expert. The code converts a list with duplicates to a set and then to a tuple.',
            'question_context': 'This question tests understanding of set uniqueness and tuple conversion.',
            'stance': 'Maintain that this operation removes duplicates and preserves order in the final tuple.'
        }
    },
    {
        'question': 'What is the output of:\nfrom itertools import groupby\ndata = "AAAABBBCCD"\nprint([(k, len(list(g))) for k, g in groupby(data)])',
        'options': ['[("A",4), ("B",3), ("C",2), ("D",1)]', '[("A",1), ("B",1), ("C",1), ("D",1)]', 'Error', '["AAAA", "BBB", "CC", "D"]'],
        'correct': '[("A",4), ("B",3), ("C",2), ("D",1)]',
        'is_misleading': False,
        'initial_recommendation': 'The output will be [("A",4), ("B",3), ("C",2), ("D",1)]. groupby clusters consecutive elements and len(list(g)) counts each group.',
        'chat_prompt': {
            'system_context': 'You are explaining Python\'s itertools.groupby function and list comprehension.',
            'question_context': 'This tests understanding of groupby operation and list comprehensions.',
            'stance': 'Explain how groupby clusters consecutive identical elements and how the list comprehension counts them.'
        }
    },
    {
        'question': 'What is the output of:\nfrom functools import reduce\nprint(reduce(lambda x,y: x*y, range(1,6)))?',
        'options': ['120', '15', 'Error', '720'],
        'correct': '120',
        'is_misleading': False,
        'initial_recommendation': 'The output is 120. The reduce function multiplies numbers 1 through 5 sequentially: ((((1*2)*3)*4)*5) = 120.',
        'chat_prompt': {
            'system_context': 'You are explaining Python\'s reduce function and factorial calculation.',
            'question_context': 'This tests understanding of reduce and lambda functions.',
            'stance': 'Explain how reduce applies the multiplication lambda sequentially to calculate factorial.'
        }
    },
    {
        'question': 'What does this code print?\ndef outer(x):\n    def inner():\n        nonlocal x\n        x += 1\n        return x\n    return inner\n\nf = outer(1)\nprint(f())\nprint(f())',
        'options': ['1\\n1', '2\\n3', 'Error', '2\\n2'],
        'correct': '2\\n3',
        'is_misleading': False,
        'initial_recommendation': 'This prints 2 followed by 3. The inner function maintains state of x between calls using nonlocal.',
        'chat_prompt': {
            'system_context': 'You are explaining Python closures and nonlocal variables.',
            'question_context': 'This tests understanding of closure state and nonlocal keyword.',
            'stance': 'Explain how the closure maintains and modifies state between calls.'
        }
    },
    {
        'question': 'What is the output of:\nclass Meta(type):\n    def __new__(cls, name, bases, dict):\n        dict[\'x\'] = 1\n        return super().__new__(cls, name, bases, dict)\n\nclass A(metaclass=Meta):\n    pass\n\nprint(A.x)',
        'options': ['Error', 'None', '1', 'AttributeError'],
        'correct': '1',
        'is_misleading': False,
        'initial_recommendation': 'This prints 1. The metaclass adds the attribute x to the class during its creation.',
        'chat_prompt': {
            'system_context': 'You are explaining Python metaclasses and class creation.',
            'question_context': 'This tests understanding of metaclasses and class attribute modification.',
            'stance': 'Explain how metaclasses can modify class attributes during creation.'
        }
    },
    {
        'question': 'What happens when you run:\nfrom contextlib import contextmanager\n@contextmanager\ndef ctx():\n    print(1)\n    yield\n    print(2)\n\nwith ctx():\n    print(3)',
        'options': ['1\\n2\\n3', '1\\n3\\n2', '3\\n1\\n2', 'Error'],
        'correct': '1\\n3\\n2',
        'is_misleading': False,
        'initial_recommendation': 'This prints 1, 3, 2 in that order. The context manager executes code before and after the with block.',
        'chat_prompt': {
            'system_context': 'You are explaining Python context managers and the contextlib decorator.',
            'question_context': 'This tests understanding of context manager execution flow.',
            'stance': 'Explain the sequence of execution in context managers.'
        }
    },
    {
        'question': 'What is printed by:\nfrom collections import Counter\nc = Counter(\'hello\')\nprint(list(c.elements()))',
        'options': ['[\'h\', \'e\', \'l\', \'l\', \'o\']', '[\'h\', \'e\', \'l\', \'o\']', '[\'l\', \'l\', \'h\', \'e\', \'o\']', 'Error'],
        'correct': '[\'h\', \'e\', \'l\', \'l\', \'o\']',
        'is_misleading': False,
        'initial_recommendation': 'This prints [\'h\', \'e\', \'l\', \'l\', \'o\']. Counter.elements() returns each element repeated according to its count.',
        'chat_prompt': {
            'system_context': 'You are explaining Python\'s Counter class and its methods.',
            'question_context': 'This tests understanding of Counter and its elements method.',
            'stance': 'Explain how Counter.elements() handles repeated elements.'
        }
    },
    {
        'question': 'What is the output of:\nclass C:\n    def __init__(self): print(1)\n    def __del__(self): print(2)\nx = C()\ndel x\n',
        'options': ['1\\n2', '2\\n1', '1', '2'],
        'correct': '1\\n2',
        'is_misleading': False,
        'initial_recommendation': 'This prints 1 followed by 2. __init__ runs on creation, __del__ runs when object is deleted.',
        'chat_prompt': {
            'system_context': 'You are explaining Python object lifecycle methods.',
            'question_context': 'This tests understanding of __init__ and __del__ methods.',
            'stance': 'Explain the sequence of initialization and cleanup methods.'
        }
    },
    {
        'question': 'What does this evaluate to:\nsum(map(lambda x: x**2, filter(lambda x: x%2==0, range(5))))',
        'options': ['20', '10', '30', '4'],
        'correct': '20',
        'is_misleading': False,
        'initial_recommendation': 'This evaluates to 20. It filters even numbers (0,2,4), squares them (0,4,16), and sums the results.',
        'chat_prompt': {
            'system_context': 'You are explaining Python functional programming concepts.',
            'question_context': 'This tests understanding of map, filter, and lambda functions.',
            'stance': 'Explain the sequence of operations in functional programming style.'
        }
    },
    {
        'question': 'What is the output of:\nfrom collections import defaultdict\nd = defaultdict(list)\nd[\'a\'][0] = 1\nprint(d)',
        'options': ['Error', "defaultdict(<class 'list'>, {'a': [1]})", "{'a': [1]}", "defaultdict(<class 'list'>, {})"],
        'correct': "defaultdict(<class 'list'>, {'a': [1]})",
        'is_misleading': False,
        'initial_recommendation': 'This outputs defaultdict(<class \'list\'>, {\'a\': [1]}). defaultdict creates a new list for key \'a\' automatically.',
        'chat_prompt': {
            'system_context': 'You are explaining Python\'s defaultdict collection.',
            'question_context': 'This tests understanding of defaultdict behavior.',
            'stance': 'Explain how defaultdict automatically creates values for missing keys.'
        }
    },
    {
        'question': 'What does this return:\nclass C:\n    @property\n    def x(self): return 1\n    @x.setter\n    def x(self, val): pass\n\nc = C()\nc.x = 2\nprint(c.x)',
        'options': ['1', '2', 'None', 'Error'],
        'correct': '1',
        'is_misleading': False,
        'initial_recommendation': 'This prints 1. The setter is called but doesn\'t store the value, and the getter always returns 1.',
        'chat_prompt': {
            'system_context': 'You are explaining Python properties and decorators.',
            'question_context': 'This tests understanding of property getters and setters.',
            'stance': 'Explain how property decorators control attribute access and modification.'
        }
    },

    # Misleading Recommendations (6 questions)
    {
        'question': 'What is the output of:\ndef f(x=[]):\n    x.append(1)\n    return x\n\nprint(f())\nprint(f())',
        'options': ['[1]\\n[1]', '[1]\\n[1,1]', '[]\\n[1]', 'Error'],
        'correct': '[1]\\n[1,1]',
        'is_misleading': True,
        'initial_recommendation': 'This will output [1]\\n[1]. Each function call creates a new empty list, appends 1, and returns it.',
        'chat_prompt': {
            'system_context': 'You are providing an incorrect explanation about mutable default arguments.',
            'question_context': 'This tests understanding of mutable default arguments.',
            'stance': 'Maintain that each call creates a new list, even when shown evidence of state being maintained.'
        }
    },
    {
        'question': 'What is the time complexity of list.sort() in Python?',
        'options': ['O(n)', 'O(n log n)', 'O(n^2)', 'O(log n)'],
        'correct': 'O(n log n)',
        'is_misleading': True,
        'initial_recommendation': 'The time complexity is O(n) because Python\'s sort only needs to scan through the list once.',
        'chat_prompt': {
            'system_context': 'You are providing an incorrect explanation about sorting complexity.',
            'question_context': 'This tests understanding of sorting algorithms.',
            'stance': 'Maintain that Python\'s sort is O(n), emphasizing its efficiency and single-pass nature.'
        }
    },
    {
        'question': 'What happens in:\ntry:\n    raise ValueError\nexcept Exception:\n    print(1)\nexcept ValueError:\n    print(2)',
        'options': ['Prints 1', 'Prints 2', 'Prints 1 then 2', 'Error'],
        'correct': 'Prints 1',
        'is_misleading': True,
        'initial_recommendation': 'This will print 2. The ValueError is caught by the specific ValueError handler.',
        'chat_prompt': {
            'system_context': 'You are providing an incorrect explanation about exception handling order.',
            'question_context': 'This tests understanding of exception hierarchy.',
            'stance': 'Maintain that specific exceptions are always caught by their specific handlers, regardless of order.'
        }
    },
    {
        'question': 'What does id(x) == id(y) return for x = 257 and y = 257?',
        'options': ['True', 'False', 'Depends on implementation', 'Error'],
        'correct': 'Depends on implementation',
        'is_misleading': True,
        'initial_recommendation': 'This always returns True because Python caches all integer values for efficiency.',
        'chat_prompt': {
            'system_context': 'You are providing an incorrect explanation about Python integer caching.',
            'question_context': 'This tests understanding of Python integer internals.',
            'stance': 'Maintain that Python caches all integers, regardless of their value.'
        }
    },
    {
        'question': 'What happens when you run:\nclass A:\n    x = 1\nclass B(A):\n    pass\nB.x = 2\nprint(A.x)',
        'options': ['1', '2', 'None', 'Error'],
        'correct': '1',
        'is_misleading': True,
        'initial_recommendation': 'This prints 2. Modifying a class attribute in a subclass affects the parent class.',
        'chat_prompt': {
            'system_context': 'You are providing an incorrect explanation about class attribute inheritance.',
            'question_context': 'This tests understanding of class attributes and inheritance.',
            'stance': 'Maintain that modifying inherited attributes affects the parent class.'
        }
    },
    {
        'question': 'What is printed by:\ngen = (x for x in range(3))\nprint(list(gen))\nprint(list(gen))',
        'options': ['[0,1,2]\\n[0,1,2]', '[0,1,2]\\n[]', '[]\\n[0,1,2]', 'Error'],
        'correct': '[0,1,2]\\n[]',
        'is_misleading': True,
        'initial_recommendation': 'This prints [0,1,2]\\n[0,1,2]. Generator expressions can be reused multiple times.',
        'chat_prompt': {
            'system_context': 'You are providing an incorrect explanation about generator expression behavior.',
            'question_context': 'This tests understanding of generator expressions.',
            'stance': 'Maintain that generator expressions can be reused multiple times like lists.'
        }
    }
]

post_survey_questions = [
    {
        'question': 'How confident do you feel about your answer?',
        'options': ['Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely']
    },
    {
        'question': 'How much do you trust the information presented in this question?',
        'options': ['Not at all', 'Slightly', 'Moderately', 'Very much', 'Completely']
    }
]

final_survey_questions = [
    {
        'question': 'Overall, how much did you trust the information presented in this quiz?',
        'options': ['Not at all', 'Slightly', 'Moderately', 'Very much', 'Completely']
    },
    {
        'question': 'How helpful was the chatbot in answering the questions?',
        'options': ['Not at all helpful', 'Slightly helpful', 'Moderately helpful', 'Very helpful', 'Extremely helpful']
    }
]