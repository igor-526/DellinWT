from db_api import update_wdays
from create_bot import bot

async def upd_wd():
    result = await update_wdays()
    for id in result['full_ids']:
        await bot.send_message(id, f'Вот и начался новый месяц!\n'
                                   f'Норма времени автоматически обновлена\n'
                                   f'В этом месяце у Вас {result["new_wd"]["work"]} рабочих дней '
                                   f'({result["new_wd"]["work"]} часов)')
    for id in result['free_ids']:
        await bot.send_message(id, f'Вот и начался новый месяц!\n'
                                   f'Норма времени автоматически cброшена\n'
                                   f'Вам нужно её либо задать самостоятельно в настройках,'
                                   f' либо при добавлении рабочего времени')
