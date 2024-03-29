from handlers.calc_fuel.s_odometer import register_handlers_cf_s_odo
from handlers.calc_fuel.f_odometer import register_handlers_cf_f_odo
from handlers.calc_fuel.fuel import register_handlers_cf_fuel
from handlers.calc_fuel.refuel import register_handlers_cf_refuel
from handlers.calc_fuel.sel_auto import register_handlers_cf_sel_auto
from handlers.calc_fuel.confirm import register_handlers_cf_confirm
from handlers.add_time.ch_date import register_handlers_at_ch_date
from handlers.add_time.confirm import register_handlers_at_confirm
from handlers.add_time.day_status import register_handlers_at_day_status
from handlers.add_time.f_time import register_handlers_at_f_time
from handlers.add_time.s_time import register_handlers_at_s_time
from handlers.commands.cmds import register_handlers_commands
from handlers.commands.menu import register_handlers_menu
from handlers.contacts.show import register_handlers_contacts_show
from handlers.contacts.search import register_handlers_contacts_search
from handlers.turnover.add import register_handlers_turnover_add
from handlers.turnover.confirm import register_handlers_turnover_confirm
from handlers.settings.set_delete import register_handlers_settings_delete
from handlers.settings.set_mode import register_handlers_settings_mode
from handlers.settings.set_name import register_handlers_settings_name
from handlers.settings.set_place import register_handlers_settings_place
from handlers.settings.set_wd import register_handlers_settings_wd
from handlers.settings.sets_menu import register_handlers_settings_menu
from handlers.registration.reg_wd import register_handlers_registration_wd
from handlers.registration.reg_instruct import register_handlers_registration_instruct
from handlers.registration.reg_base import register_handlers_registration_base
from handlers.registration.reg_city import register_handlers_registration_city
from handlers.registration.reg_schedule import register_handlers_registration_schedule
from handlers.reports.rep_menu import register_handlers_reports_menu
from handlers.reports.time_reported import register_handlers_reports_time
from handlers.reports.time_select import register_handlers_reports_time_select
from handlers.reports.time_delete import register_handlers_reports_time_delete
from handlers.reports.fuel_reported import register_handlers_reports_fuel
from handlers.reports.fuel_select import register_handlers_reports_fuel_select
from handlers.reports.fuel_delete import register_handlers_reports_fuel_delete
from handlers.reports.to_reported import register_handlers_reports_to
from handlers.reports.to_select import register_handlers_reports_to_select
from handlers.reports.to_delete import register_handlers_reports_to_delete
from handlers.issuereport.send import register_handlers_reportissue
