import argparse
import math

parser = argparse.ArgumentParser(description="This loan calculator able to work with different "
                                             "types of payment and accept command-line arguments")
parser.add_argument("--type")
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--periods", type=int, help="the number of months needed to repay the loan")
args = parser.parse_args()

v = vars(args)
n_args = sum([ 1 for a in v.values( ) if a])

err_msg = "Incorrect parameters"


def diff_payment(principal, periods, interest):  # OK
    i = interest / 12 / 100
    m = 1
    rest_periods = periods
    sum_payments = 0
    while rest_periods > 0:
        payment = principal / periods + i * (principal - (principal * (m - 1))/periods)
        payment = math.ceil(payment)
        print(f"Month {m}: payment is {payment}")
        m += 1
        sum_payments += payment
        rest_periods -= 1
    overpayment = math.ceil(sum_payments - principal)
    print(f"Overpayment = {overpayment}")
    # python creditcalc.py --type=diff --principal=1000000 --periods=10 --interest=10


def annuity_payment(principal, periods, interest, payment):  # OK
    if not principal:  # OK
        i = interest / 12 / 100
        principal = payment / ((i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1))
        print(f'Your loan principal = {math.floor(principal)}!')
        overpayment = math.ceil(payment * periods - principal)
        print(f"Overpayment = {overpayment}")
    elif not periods:  # OK
        i = interest / 12 / 100
        n = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
        overpayment = math.ceil(payment * n - principal)
        if n < 12:
            print(f'It will {n} months to repay this loan!')
        elif n == 12:
            print('It will 1 year to repay this loan!')
        else:
            n = divmod(n, 12)
            if n[1] > 0:
                print(f'It will take {n[0]} years and {n[1]} months to repay this loan!')
            else:
                print(f'It will take {n[0]} years to repay this loan!')
        print(f"Overpayment = {overpayment}")
    elif not payment:  # OK
        i = interest / 12 / 100
        payment = principal * ((i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1))
        payment = math.ceil(payment)
        print(f'Your monthly payment = {payment}!')
        overpayment = math.ceil(payment * periods - principal)
        print(f"Overpayment = {overpayment}")


if not args.interest \
        or n_args < 4 \
        or (args.principal and args.principal < 0) \
        or (args.periods and args.periods < 0) \
        or (args.interest and args.interest< 0):
    print(err_msg)
elif args.type == "diff":
    if args.payment:
        print(err_msg + " - payment in diff")
    else:
        diff_payment(args.principal, args.periods, args.interest)
elif args.type == "annuity":
    annuity_payment(args.principal, args.periods, args.interest, args.payment)
else:
    print(err_msg + " wrong type")

