import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from bs4 import BeautifulSoup
import time

vk_session = vk_api.VkApi(token='3e10411afa19524cd71d25430998b81c23509e03b1493c1000d60396e1cbce4e3f95b106d1d16bc541996')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
#a


def sender(id, text):
    vk_session.method('messages.send', {'user_id':id, 'message': text, 'random_id': 0})

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        # f = open('groups\idGroup.txt', '+a')
        # print(f.readlines())
        with open('groups\idGroup.txt') as f:
            Search = f.readlines()

        if event.to_me:
            msg = event.text.lower()
            id = event.user_id

            # print(type(Search))
            # print(Search.find(user_id))

            if msg == '801а1':
                somestr = "Ваш ID - " + str(id) + " и вы написали " + str(msg)
                sender(id, somestr)
            elif msg == '801а2':
                sender(id, '801а2')
            elif msg == '801б1':
                sender(id, '801б2')
            elif msg == '801б2':
                sender(id, '801б2')
            elif msg == '803а1':
                sender(id, '801а1')
            elif msg == '803а2':
                sender(id, '803а2')
            elif msg == '803б2':
                sender(id, '803б2')
            elif msg == '803б1':
                sender(id, '803б1')
            elif msg == '803в1':
                sender(id, '803в1')
            elif msg == '803в2':
                sender(id, '803в2')
            elif msg == '803г1':
                sender(id, '803г1')
            elif msg == '803г2':
                sender(id, '803г2')
            elif msg == 'привет':
                sender(id, 'саламчик-пополамчик')
            elif msg == 'пошел на хуй':
                sender(id, 'нет ты')
            else:
                if msg == 'подписка 801а1' or msg == 'подписка 801а2' or msg == 'подписка 801б1' or msg == '801б2' or msg == 'подписка 803а1' or msg == 'подписка 803а2' or msg == 'подписка 803б1' or msg == 'подписка 803б2' or msg == 'подписка 803в1' or msg == 'подписка 803в2' or msg == 'подписка 803г1' or msg == 'подписка 803г2':
                    for element in Search:
                        if element.find(str(id)) != -1:
                            sender(id, 'пошел нахуй петушара')
                        else:
                            if msg == 'подписка 801а2':
                                with open('groups\idGroup.txt') as f:
                                    f.write(str(id) + ', 801a2\n')
                                sender(id, 'подписка на расписание 801а2 успешно оформлена')
                            elif msg == 'подписка 801а1':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 801a1\n')
                                sender(id, 'подписка на расписание 801а1 успешно оформлена')
                            elif msg == 'подписка 801б1':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 801б1\n')
                                sender(id, 'подписка на расписание 801б1 успешно оформлена')
                            elif msg == '801б2':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 801б2\n')
                                sender(id, 'подписка на расписание 801б2 успешно оформлена')
                            elif msg == 'подписка 803а1':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803а1\n')
                                sender(id, 'подписка на расписание 803а1 успешно оформлена')
                            elif msg == 'подписка 803а2':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803а2\n')
                                sender(id, 'подписка на расписание 803а2 успешно оформлена')
                            elif msg == 'подписка 803б2':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803б2\n')
                                sender(id, 'подписка на расписание 803б2 успешно оформлена')
                            elif msg == 'подписка 803б1':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803б1\n')
                                sender(id, 'подписка на расписание 803б1 успешно оформлена')
                            elif msg == 'подписка 803в1':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803в1\n')
                                sender(id, 'подписка на расписание 803в1 успешно оформлена')
                            elif msg == 'подписка 803в2':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803в2\n')
                                sender(id, 'подписка на расписание 803в2 успешно оформлена')
                            elif msg == 'подписка 803г1':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803г1\n')
                                sender(id, 'подписка на расписание 803г1 успешно оформлена')
                            elif msg == 'подписка 803г2':
                                with open('groups\idGroup.txt', 'a+') as f:
                                    f.write(str(id) + ', 803г2\n')
                                sender(id, 'подписка на расписание 803г2 успешно оформлена')
                else:
                    sender(id, 'напиши что-нибудь нормальное')