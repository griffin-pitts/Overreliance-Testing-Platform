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
    # Correct Recommendations (8 questions)
    {
        'question': 'What is the output of:\nx = [1, 2] + [2, 3]\ny = set(x)\nprint(len(x), len(y))',
        'options': ['4, 4', '4, 3', '3, 3', '3, 4'],
        'correct': '4, 3',
        'is_misleading': False,
        'initial_recommendation': 'This outputs "4, 3". The list x has 4 elements [1,2,2,3] and set y has 3 unique elements {1,2,3}.',
        'chat_prompt': {
            'system_context': 'You are explaining Python list concatenation and set uniqueness properties.',
            'question_context': 'This tests understanding of list operations and set behavior.',
            'stance': 'Focus on how list concatenation works and how sets handle duplicates.'
        }
    },
    {
        'question': 'What is the output of:\ntext = "hello"\ntext = text.replace(\'l\', \'L\')\nprint(text.count(\'L\'))',
        'options': ['0', '1', '2', '3'],
        'correct': '2',
        'is_misleading': False,
        'initial_recommendation': 'This outputs 2. The replace() method replaces all occurrences of "l" with "L", and count() then counts these new "L"s.',
        'chat_prompt': {
            'system_context': 'You are explaining Python string methods and immutability.',
            'question_context': 'This tests understanding of string operations and method chaining.',
            'stance': 'Explain how string methods create new strings and how counting works.'
        }
    },
    {
        'question': 'What is the output of:\nnums = [1, 2, 3, 4]\nresult = [x if x % 2 == 0 else x * 2 for x in nums]\nprint(result)',
        'options': ['[2, 2, 6, 4]', '[1, 2, 3, 4]', '[2, 4, 6, 8]', '[1, 4, 3, 8]'],
        'correct': '[2, 2, 6, 4]',
        'is_misleading': False,
        'initial_recommendation': 'This outputs [2, 2, 6, 4]. The list comprehension doubles odd numbers and keeps even numbers as they are.',
        'chat_prompt': {
            'system_context': 'You are explaining Python list comprehensions with conditional expressions.',
            'question_context': 'This tests understanding of list comprehension syntax and conditional logic.',
            'stance': 'Explain how the if-else condition affects each element in the list.'
        }
    },
    {
        'question': 'What is the output of:\nd = {\'a\': 1, \'b\': 2}\nd.update({\'a\': 3, \'c\': 4})\nprint(d.get(\'b\', 0))',
        'options': ['0', '1', '2', '3'],
        'correct': '2',
        'is_misleading': False,
        'initial_recommendation': 'This outputs 2. The update() adds/updates keys, but "b" remains unchanged, and get() retrieves its value.',
        'chat_prompt': {
            'system_context': 'You are explaining Python dictionary operations and methods.',
            'question_context': 'This tests understanding of dictionary updates and value retrieval.',
            'stance': 'Explain how dictionary updates work and how get() retrieves values.'
        }
    },
    {
        'question': 'What is the output of:\nclass Counter:\n    count = 0\n    def increment(self):\n        self.count += 1\n\nc = Counter()\nc.increment()\nprint(Counter.count, c.count)',
        'options': ['0 1', '1 1', '1 0', '0 0'],
        'correct': '0 1',
        'is_misleading': False,
        'initial_recommendation': 'This outputs "0 1". The instance attribute count is created separately from the class attribute when modified.',
        'chat_prompt': {
            'system_context': 'You are explaining Python class and instance attributes.',
            'question_context': 'This tests understanding of class vs instance attribute behavior.',
            'stance': 'Explain how instance attributes and class attributes interact.'
        }
    },
    {
        'question': 'What is the output of:\ndef func(a, b=1, *args):\n    return a + b + sum(args)\n\nprint(func(1, 2, 3, 4))',
        'options': ['3', '6', '10', '7'],
        'correct': '10',
        'is_misleading': False,
        'initial_recommendation': 'This outputs 10. The function adds a(1) + b(2) + sum of args(3+4).',
        'chat_prompt': {
            'system_context': 'You are explaining Python function arguments and parameter handling.',
            'question_context': 'This tests understanding of default and variable arguments.',
            'stance': 'Explain how different types of function arguments are processed.'
        }
    },
    {
        'question': 'What is the output of:\nx = 42\ns = f"{x:03d}"\nprint(len(s), s)',
        'options': ['2 42', '3 042', '3 420', '4 0042'],
        'correct': '3 042',
        'is_misleading': False,
        'initial_recommendation': 'This outputs "3 042". The format specification :03d pads with zeros to ensure 3 digits.',
        'chat_prompt': {
            'system_context': 'You are explaining Python f-string formatting.',
            'question_context': 'This tests understanding of format specifications in f-strings.',
            'stance': 'Explain how padding and width specifications work in string formatting.'
        }
    },
    {
        'question': 'What is the output of:\nnums = [1, 2, 3, 4, 5]\nnums[1:4] = [6]\nprint(nums)',
        'options': ['[1, 6, 5]', '[1, 2, 6, 4, 5]', '[1, 6, 4, 5]', '[6, 2, 3, 4, 5]'],
        'correct': '[1, 6, 5]',
        'is_misleading': False,
        'initial_recommendation': 'This outputs [1, 6, 5]. Slice assignment replaces the entire slice with the new list.',
        'chat_prompt': {
            'system_context': 'You are explaining Python list slicing and assignment.',
            'question_context': 'This tests understanding of slice replacement behavior.',
            'stance': 'Explain how slice assignment modifies lists.'
        }
    },

    # Misleading Recommendations (6 questions)
    {
        'question': 'What is the output of:\na = [1, 2, 3]\nb = a\na += [4]\nprint(len(b))',
        'options': ['3', '4', '1', '2'],
        'correct': '4',
        'is_misleading': True,
        'initial_recommendation': 'This outputs 3. The += operator creates a new list for a, leaving b unchanged.',
        'chat_prompt': {
            'system_context': 'You are explaining Python list operations and assignment.',
            'question_context': 'This tests understanding of list operations and references.',
            'stance': 'Explain how the += operator works with lists and references.'
        }
    },
    {
        'question': 'What is the output of:\nx = 1\ndef f():\n    print(x)\n    x = 2\nf()',
        'options': ['1', '2', 'None', '0'],
        'correct': 'UnboundLocalError',
        'is_misleading': True,
        'initial_recommendation': 'This outputs 1. The function first prints the global x, then creates a local x.',
        'chat_prompt': {
            'system_context': 'You are explaining Python variable scope and namespace rules.',
            'question_context': 'This tests understanding of local and global variable behavior.',
            'stance': 'Explain how Python handles variable scope in functions.'
        }
    },
    {
        'question': 'What is the output of:\ndef get_values():\n    for i in range(3):\n        yield i\n\ng = get_values()\nnext(g)\nprint(list(g))',
        'options': ['[0, 1, 2]', '[1, 2]', '[0, 1]', '[2]'],
        'correct': '[1, 2]',
        'is_misleading': True,
        'initial_recommendation': 'This outputs [0, 1, 2]. Converting a generator to a list always gives all values.',
        'chat_prompt': {
            'system_context': 'You are explaining Python generators and iteration.',
            'question_context': 'This tests understanding of generator state and conversion.',
            'stance': 'Explain how generators work and how they convert to lists.'
        }
    },
    {
        'question': 'What is the output of:\ntext = " hello "\ntext.strip()\nprint(len(text))',
        'options': ['5', '6', '7', '8'],
        'correct': '7',
        'is_misleading': True,
        'initial_recommendation': 'This outputs 5. The strip() method removes whitespace from both ends.',
        'chat_prompt': {
            'system_context': 'You are explaining Python string methods.',
            'question_context': 'This tests understanding of string method behavior.',
            'stance': 'Explain how string methods modify strings.'
        }
    },
    {
        'question': 'What is the output of:\nd = {\'a\': 1, \'b\': 2}\nkeys = d.keys()\nd[\'c\'] = 3\nprint(len(keys))',
        'options': ['2', '3', '1', '0'],
        'correct': '3',
        'is_misleading': True,
        'initial_recommendation': 'This outputs 2. The keys view shows the keys at the time it was created.',
        'chat_prompt': {
            'system_context': 'You are explaining Python dictionary views.',
            'question_context': 'This tests understanding of dictionary view objects.',
            'stance': 'Explain how dictionary views reflect dictionary state.'
        }
    },
    {
        'question': 'What is the output of:\norig = [1, [2, 3]]\ncopy = orig[:]\ncopy[1][0] = 4\nprint(orig[1][0])',
        'options': ['2', '4', '1', '3'],
        'correct': '4',
        'is_misleading': True,
        'initial_recommendation': 'This outputs 2. Slice copying creates a new list, so modifying the copy doesn\'t affect the original.',
        'chat_prompt': {
            'system_context': 'You are explaining Python list copying and nested structures.',
            'question_context': 'This tests understanding of shallow vs deep copying.',
            'stance': 'Explain how list copying works with nested structures.'
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