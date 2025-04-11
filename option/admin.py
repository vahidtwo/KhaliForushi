from django.contrib import admin

from option.models import CoverdCallOptions, CoverdCallDynamicConfig


# Register your models here.
@admin.register(CoverdCallOptions)
class CoverdCallOptionsAdmin(admin.ModelAdmin):
    list_display = (
        "final_price_diff_percent_by_final_price",
        "cover_call_final_price_diff_percent_by_base_price",
        "symbol",
        "original_symbol",
        "end_date",
        "delta",
        "highest_bid_price",
        "lowest_ask_price",
        "highest_bid_value",
        "guarantee",
        "original_symbol_lowest_ask_price",
        "cover_call_final_price",
        "cover_call_volume",
        "cover_call",
        "cover_call_profit",
        "cover_call_in_end_date",
        "strick_price",
        "created_at",
        "created_date_at",
    )


@admin.register(CoverdCallDynamicConfig)
class CoverdCallDynamicConfigAdmin(admin.ModelAdmin):
    list_display = ("delta", "minimum_profit", "token")
