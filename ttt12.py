import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='3e10411afa19524cd71d25430998b81c23509e03b1493c1000d60396e1cbce4e3f95b106d1d16bc541996')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


global SubscribedBoolean


def is_subscribed(id_to_check):
    try:
        with open("groups/idGroup.txt") as subscribeListFile:
            subscribed_list = subscribeListFile.readlines()
            if len(subscribed_list) != 0:
                for subscribe_element_counter in range(0, len(subscribed_list)):
                    subscribe_element = subscribed_list[subscribe_element_counter]
                    if subscribe_element.find(str(id_to_check)) != -1:
                        print("Найден повтор ")
                        subscribed_boolean = True
                        break
                    elif subscribe_element.find(str(id_to_check)) == -1:
                        print("Повтор не найден")
                        subscribed_boolean = False
                    subscribe_element_counter += 1
                return subscribed_boolean
            elif len(subscribed_list) == 0:
                subscribed_boolean = False
                return subscribed_boolean
    except Exception as someException:
        print('Возникла ошибка: ' + str(someException))


def unsubscribing(user_unsub_id):
    with open(r"groups\idGroup.txt") as File2:
        un_sub_list = File2.readlines()
    with open(r'groups\idGroup.txt', 'w+') as File:
        for UnSubElement in un_sub_list:
            if UnSubElement.find(str(user_unsub_id)) != -1:
                un_sub_list.remove(UnSubElement)
        File.writelines(un_sub_list)


def subscribing(message_to_sub, user_sub_id):
    with open(r'groups\idGroup.txt', 'a+') as File:
        File.write(str(user_sub_id) + ', ' + message_to_sub[9:14] + '\n')


def sender(id_to_send, text):
    vk_session.method('messages.send', {'user_id': id_to_send, 'message': text, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            user_id = event.user_id
            print(str(msg) + " от " + str(user_id))
            SomeBool = is_subscribed(user_id)
            GroupComponent = [" 801а1", " 801а2", " 801б1", " 801б2", " 803а1", " 803а2", " 803б1", " 803б2", " 803в1",
                              " 803в2", " 803г1", " 803г2"]
            for num_group, val_group in enumerate(GroupComponent):
                sub_gen = "подписка" + val_group
                if msg == sub_gen:
                    if SomeBool:
                        sender(user_id, 'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы '
                                        'данных? Тогда напишите "Отписка"')
                    elif not SomeBool:
                        subscribing(msg, user_id)
                        sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы' +
                               val_group)
                    break

                if msg == 'отписка':
                    if SomeBool:
                        unsubscribing(user_id)
                        sender(user_id, 'Вы были успешно отписаны от ежедневной рассылки расписания')
                    else:
                        sender(user_id, 'Мы не можем вас отписать так как вы не подписаны')
                    break
                elif not 'подписка' + val_group:
                    sender(user_id, 'напиши что-нибудь нормальное')
                    break
