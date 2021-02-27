import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='3e10411afa19524cd71d25430998b81c23509e03b1493c1000d60396e1cbce4e3f95b106d1d16bc541996')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


global SubscribedBoolean


def isSubscribed(id):
    try:
        with open("groups/idGroup.txt") as subscribeListFile:
            SubscribedList = subscribeListFile.readlines()
            if len(SubscribedList) != 0:
                SubscribeElementCounter = 0
                for SubscribeElementCounter in range(0, len(SubscribedList)):
                    SubscribeElement = SubscribedList[SubscribeElementCounter]
                    if SubscribeElement.find(str(id)) != -1:
                        print("Найден повтор ")
                        SubscribedBoolean = True
                        break
                    elif SubscribeElement.find(str(id)) == -1:
                        print("Повтор не найден")
                        SubscribedBoolean = False
                    SubscribeElementCounter += 1
                return SubscribedBoolean
            elif len(SubscribedList) == 0:
                SubscribedBoolean = False
                return SubscribedBoolean
    except Exception as someException:
        print('Возникла ошибка: ' + str(someException))


def unsubscribing(user_unsub_id):
    with open("groups\idGroup.txt") as File2:
        UnSubList = File2.readlines()
    with open(r'groups\idGroup.txt', 'w+') as File:
        for UnSubElement in UnSubList:
            if UnSubElement.find(str(user_unsub_id)) != -1:
                UnSubList.remove(UnSubElement)
        File.writelines(UnSubList)


def subscribing(message_to_sub, user_sub_id):
    with open(r'groups\idGroup.txt', 'a+') as File:
        File.write(str(user_sub_id) + ', ' + message_to_sub[9:14] + '\n')


def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            user_id = event.user_id
            print(str(msg) + " от " + str(user_id))

            SomeBool = isSubscribed(user_id)
            if msg == 'подписка 803г2':
                if SomeBool:
                    sender(user_id, 'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы '
                                    'данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    subscribing(msg, user_id)
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803г2')

            elif msg == 'отписка':
                if SomeBool:
                    unsubscribing(user_id)
                    sender(user_id, 'Вы были успешно отписаны от ежедневной рассылки расписания')
                else:
                    sender(user_id, 'Мы не можем вас отписать так как вы не подписаны')
            else:
                sender(user_id, 'напиши что-нибудь нормальное')

