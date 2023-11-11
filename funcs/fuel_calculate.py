import db_api


async def calc_fuel(res):
    auto = res['auto']
    auto_info = await db_api.sel_auto(auto)
    s_odo = res['start_odo']
    f_odo = res['finish_odo']
    f = res['fuel']
    rf = res['refuel']
    result = {'odo': f_odo - s_odo,
              'fuel': f + rf - (
                      f_odo - s_odo) / 100 * auto_info['consumption'],
              'auto': auto,
              'consumption': auto_info['consumption'],
              'tank': auto_info['tank'],
              'auto_id': auto_info['id']}
    result['fuel_delta'] = result['odo']/100*auto_info['consumption']
    if result['fuel'] < 1:
        result['fuel'] = 1
    if result['fuel'] > result['tank']:
        result['fuel'] = result['tank']
    return result
