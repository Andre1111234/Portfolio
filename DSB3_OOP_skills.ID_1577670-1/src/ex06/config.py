num_of_steps = 3
report_template = """We made {total_observations} observations by tossing a coin: {tails} of them were tails and {heads} of them were heads. The probabilities are {tail_prob:.2f}% and {head_prob:.2f}%, respectively. Our forecast is that the next {num_steps} observations will be: {tail_forecast} tail and {head_forecast} heads."""

# Для Telegram (замени на реальные значения)
telegram_webhook_url = "https://api.telegram.org/bot8221806505:AAFXL3H9RaqxSN66kowEpaX12LVUXy2okHE/sendMessage"
telegram_chat_id = "483983133"