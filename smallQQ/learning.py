#coding:utf8
import cPickle
import os
import re
import weather


class Learn:
    """
    Record the simple learning
    """
    def __init__(self):
        self.knowledge_file = 'kownledge.db'
        self.knowledge_cache = self.load()
        self.length = 10
        self.weather = weather.Weather()

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
                return answer.encode('utf8')
            elif result[0] in ['#weather#', '###']:
                answer = self.weather.get_weather_report(result[1])
                return answer

            else:
                return (
                    '[注意]: 请注意语法(空格)\n'
                    '[Function] only support:\n'
                    '1.#learn# 关键字 需要记录的内容\n'
                    '2.#use# 关键字\n'
                    '3.#weather# 中国市级城市名\n '
                )

        else:
            return None

