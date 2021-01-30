
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

def countD(n, str1="Market Active till {} count down is ZERO."):
    countDown = n
    while (countDown >= 0):
        cc = []
        if countDown != 0:
            cc.append(countDown)
            print(str1.format(cc[0]),end='\r')
            sleep(1)
            cc.clear()
            countDown = countDown - 1
        else:
            break 


def countC(n):
    countDown = n

    while (countDown >= 0):
        cc = []
        channeled_timer(countDown)
        sleep(1)
        if countDown != 0:
            cc.append(countDown)
            # sleep(1)
            cc.clear()
            countDown = countDown - 1
        else:
            break 

def spin_manager():
    print('MAKO POLLO')
    from .models import WheelSpin
    from .models import WheelSpin, OutCome
    # from core.models import BetSettingVar

    try:
        id = max([obj.id for obj in WheelSpin.objects.all()])
    except Exception as e:
        print(e)
        WheelSpin.objects.update_or_create(id=1) # happens once DB creation

    try:
        try:
            OutCome.objects.create(market_id=id)  #  process result of last ma
        except Exception as e:
            pass
        sleep(2)
        this_wheelspin = WheelSpin.objects.get(id=id )
            #  create on demand
        if not this_wheelspin.place_stake_is_active:
            print('NOTTTTT')
            WheelSpin.objects.create(id=id+1)

        # WheelSpin.objects.create(id=id+1) # create WheeSpin of id current +1  
        id = id + 1
    except Exception as e:
        print('CONTROL ERROR', e)
        return e


################ web Socket functions ##########

channel_layer = get_channel_layer()
def channeled_timer(secondvalu):
    # channel_layer = get_channel_layer()
    # print(f'VALL:SS{secondvalu}')
    async_to_sync(channel_layer.group_send)(
        "daru_spin",
        {
            "type": "second_value",
            "secondvalu": secondvalu,
        }
    )


def market_create():
    print('DATO ZOLLO')
    from .models import WheelSpin, OutCome
    # from core.models import BetSettingVar

    try:
        id = max([obj.id for obj in WheelSpin.objects.all()])
    except Exception as e:
        print(e)
        WheelSpin.objects.update_or_create(id=1) # happens once DB creation

    try:
        try:
            OutCome.objects.create(market_id=id)  #  process result of last ma
        except Exception as e:
            print(f'Outcometask:{e}')
            pass
  
    except Exception as e:
        print('CONTROL ERROR', e)
        return e
