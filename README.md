# testing

## RUN
python .\main.py


## ARGUMENT
usage: main.py [-h] [--service SERVICE] [--method METHOD] [--user USER]

optional arguments:
  -h, --help         show this help message and exit
  --service SERVICE  E.G products, accounts or orders, Default: products
  --method METHOD    E.G GET Default: get
  --user USER        Default: 100

## MONITOR SCALLING

kubectl get pod <your pod name> -w
