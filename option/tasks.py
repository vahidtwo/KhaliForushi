import jdatetime
from celery import shared_task

from clients.ravi import RaviClient
from clients.telegram import Telegram
from option.models import CoverdCallDynamicConfig, CoverdCallOptions


@shared_task(name="get-ravi-option")
def get_ravi_option():
    telegram_client = Telegram
    config = CoverdCallDynamicConfig.objects.first()
    client = RaviClient(token=config.token)
    response = client.get_covert_call(
        delta=config.delta, minimum_profit=config.minimum_profit
    )
    options_data = client.parse_covert_call_option_data(response)
    coverd_call_options_list = []
    for item in options_data:
        coverd_call_options_list.append(
            CoverdCallOptions(
                final_price_diff_percent_by_final_price=item.final_price_diff_percent_by_final_price,
                cover_call_final_price_diff_percent_by_base_price=item.cover_call_final_price_diff_percent_by_base_price,
                symbol=item.symbol,
                original_symbol=item.original_symbol,
                end_date=item.end_date,
                delta=item.delta,
                highest_bid_price=item.highest_bid_price,
                lowest_ask_price=item.lowest_ask_price,
                highest_bid_value=item.highest_bid_value,
                strick_price=item.strick_price,
                cover_call_final_price=item.cover_call_final_price,
                cover_call_volume=item.cover_call_volume,
                cover_call=item.cover_call,
                cover_call_profit=item.cover_call_profit,
                cover_call_in_end_date=item.cover_call_in_end_date,
                guarantee=item.guarantee,
                original_symbol_lowest_ask_price=item.original_symbol_lowest_ask_price,
            )
        )
    new_items = []
    for item in coverd_call_options_list:
        try:
            item.save()
            new_items.append(item)
        except Exception as e:
            print(str(e))

    now = jdatetime.date.today()
    for obj in new_items:
        date = jdatetime.date.fromgregorian(date=obj.end_date)
        telegram_client.send_message_to_channel(
            f"{obj.symbol} ({obj.original_symbol}) \n"
            f"annual profit {obj.cover_call:.3f}\n"
            f"delta {obj.delta}\n"
            f"due date: {date.strftime('%Y-%m-%d')} [{(date - now).days} day]\n"
            f"cover-call in due date: {obj.cover_call_in_end_date:.2f}"
        )
