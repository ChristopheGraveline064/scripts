# testing

## RUN
python .\scale_test.py


## ARGUMENT
```
Enter arguments in lowercase

optional arguments:
  -h, --help            show this help message and exit
  --service SERVICE     E.G products, accounts or orders, Default: products
  --method METHOD [METHOD ...]
                        E.G get, post, delete, get all or delete all Default: ['post']
  --user USER           Enter the number of user to simulate Default: 1000
  --threads THREADS     Enter the number of threads Default: 15
```

## MONITOR SCALLING

kubectl get pod <your pod name> -w
kubectl get hpa
