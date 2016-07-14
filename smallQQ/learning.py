#coding:utf8
import cPickle
import os
import re


class Learn:
    """
    Record the simple learning
    """
    def __init__(self):
        self.knowledge_file = 'kownledge.db'
        self.knowledge_cache = self.load()
        self.length = 10

    def load(self):
        """
        Load the knowledge_file to the knowledge_cache
        """
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file) as f:
                knowledge_cache = cPickle.load(
                    cPickle.load(f)
                )
        else:
            knowledge_cache = {}

        return knowledge_cache

    def save(self):
        """
        Saved the record to the knowledge_file
        """
        with open(self.knowledge_file, 'a+') as f:
            cPickle.dump(self.knowledge_cache, f)

    def learn_or_call(self, words):
        """
        Record Leran "key" "word"
        """

        if re.findall(r'#[^#]*#', words):
            result = words.split(' ')
            if result[0] == '#learn#':
                try:
                    self.knowledge_cache[result[1]] = ' '.join(result[2:])
                    if len(self.knowledge_cache) > self.length:
                        self.save()
                        self.length += 10
                    return 'Record successfully'
                except IndexError:
                    return 'No enought record'

            elif result[0] == '#use#':
                answer = self.knowledge_cache.get(
                    result[1],
                    'Sorry !! No Record!'
                )
                return answer
            else:
                return "[Function] only support #learn# and #use#"
        else:
            return None

