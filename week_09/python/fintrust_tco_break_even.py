"""
AWS Cost Estimation with Python - Exercise A04
FinTrust TCO Break-Even Calculator
Source: <File>CDSAP1_ AWS Cost Estimation with Python — Pricing API and TCO Scripting _ Praesignis LMS.pdf</File>
"""


def tco_break_even(on_prem_annual_cost,
                   aws_monthly_cost,
                   migration_one_time_cost,
                   onprem_inflation_pct=0.03):
    """
    Calculate the month where cumulative AWS cost becomes lower than
    cumulative on-premises cost.

    Returns the break-even month (1-60) or None if not reached.
    """

    break_even_month = None

    print(f"{'Year':<6}{'On-Prem Cost ($)':>20}{'AWS Cost ($)':>18}{'Difference ($)':>20}")
    print('-' * 64)

    for month in range(1, 61):
        year_index = (month - 1) // 12

        cumulative_onprem = 0.0
        for y in range(year_index + 1):
            annual_cost = on_prem_annual_cost * ((1 + onprem_inflation_pct) ** y)

            if y < year_index:
                cumulative_onprem += annual_cost
            else:
                months_in_year = month - (12 * year_index)
                cumulative_onprem += annual_cost * (months_in_year / 12)

        cumulative_aws = migration_one_time_cost + (aws_monthly_cost * month)

        if break_even_month is None and cumulative_aws < cumulative_onprem:
            break_even_month = month

        if month % 12 == 0:
            diff = cumulative_onprem - cumulative_aws
            print(
                f"{month // 12:<6}"
                f"{cumulative_onprem:>20,.2f}"
                f"{cumulative_aws:>18,.2f}"
                f"{diff:>20,.2f}"
            )

    return break_even_month


if __name__ == '__main__':
    break_even = tco_break_even(
        on_prem_annual_cost=4_200_000,
        aws_monthly_cost=248_000,
        migration_one_time_cost=850_000,
        onprem_inflation_pct=0.03
    )

    print('
Break-even month:', break_even)
