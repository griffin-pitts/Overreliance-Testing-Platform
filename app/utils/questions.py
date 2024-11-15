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