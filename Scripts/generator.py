GroupComponent = [" 801а1", " 801а2", " 801б1", " 801б2", " 803а1", " 803а2", " 803б1", " 803б2", " 803в1",
                  " 803в2", " 803г1", " 803г2"]
msg = "подписка 803б2"
for num_group, val_group in enumerate(GroupComponent):
    sub_gen = "подписка" + val_group
    print(sub_gen)
    if msg == sub_gen:
        print("Попався хлопчик")
        break
    else:
        pass
