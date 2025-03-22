def cust_map(input_params):
    churn_rate = input_params["churn_rate"]
    profit_generated = input_params["profit_generated"]
    risk_appetite = input_params["risk_appetite"]
    financial_acumen = input_params["financial_acumen"]

    risk_customer = 10 - (0.7 * risk_appetite + 0.3 * financial_acumen)
    value_customer = 0.5 * profit_generated + 0.5 * financial_acumen
    profit_margin = 0.7 * profit_generated + 0.3 * financial_acumen
    risk_bank = (
        0.5 * churn_rate + 0.3 * (10 - profit_generated) + 0.2 * (10 - financial_acumen)
    )
    retention_value = 0.6 * (10 - churn_rate) + 0.4 * profit_generated

    output = {
        "risk_customer": max(0, min(10, risk_customer)),
        "value_customer": max(0, min(10, value_customer)),
        "profit_margin": max(0, min(10, profit_margin)),
        "risk_bank": max(0, min(10, risk_bank)),
        "retention_value": max(0, min(10, retention_value)),
    }
    return output


if __name__ == "__main__":
    input_params = {
        "churn_rate": 5,  # 0-10
        "profit_generated": 8,
        "risk_appetite": 1,
        "financial_acumen": 10,
    }
    output = cust_map(input_params)
    print(f"Mapped {input_params} to {output}")
