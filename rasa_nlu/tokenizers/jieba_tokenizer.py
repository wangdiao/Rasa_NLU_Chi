from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import glob
import logging
from typing import Any
from typing import List
from typing import Text

import jieba

from rasa_nlu.components import Component
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.tokenizers import Tokenizer, Token
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData

logger = logging.getLogger(__name__)

# Add jieba userdict file
jieba_userdicts = glob.glob("./jieba_userdict/*")
for jieba_userdict in jieba_userdicts:
    jieba.load_userdict(jieba_userdict)
    logger.warning("load jieba_userdict success: %s", jieba_userdict)


class JiebaTokenizer(Tokenizer, Component):
    name = "tokenizer_jieba"

    provides = ["tokens"]

    def __init__(self):
        pass

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["jieba"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        if config['language'] != 'zh':
            raise Exception("tokenizer_jieba is only used for Chinese. Check your configure json file.")

        for example in training_data.training_examples:
            example.set("tokens", self.tokenize(example.text))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("tokens", self.tokenize(message.text))

    def tokenize(self, text):
        # type: (Text) -> List[Token]
        tokenized = jieba.tokenize(text)
        tokens = [Token(word, start) for (word, start, end) in tokenized]

        return tokens
