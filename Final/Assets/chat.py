from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


chatbot = ChatBot(
                "GUI Bot",
                storage_adapter="chatterbot.storage.SQLStorageAdapter",
                logic_adapters=[
                    "chatterbot.logic.BestMatch",
                    'chatterbot.logic.MathematicalEvaluation',
                ],
                database_uri="sqlite:///database.sqlite3"
            )

    #return str(chatbot.get_response(mes).text)

f = open('final.txt', 'r')

train_data=[]
for line in f:
    train_data.append(line)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.english")

trainer = ListTrainer(chatbot)

trainer.train(train_data)