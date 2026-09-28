def calculate_selling_price(price: float, discount_percent: float):
    selling_price = round(price - (price * discount_percent / 100), 2)
    return selling_price