# SAMAD app with crud functionality using AES encryption

## List of commands you can use

### REGISTER STUDENT

```bash
    python3 main.py register -n <nationalID> -i <studentID> -m <major> -b <birth_date> -f <first_name> -l <last_name> -c <balance>

    eg.

    python3 main.py register -n 0926985114 -i 40131053 -m CE -b 1403/09/30 -f Ali -l Naserinia -c 0
```

### REMOVE STUDENT

```bash
    python3 main.py remove <ID>

    eg.

    python3 main.py remove 0926985114
```

### INCREASE CREDIT

```bash
    python3 main.py credit -i <studentID> -m <money>

    eg.

    python3 main.py credit -i 40131024 -m 10000
```

### ADD FOOD

```bash
    python3 main.py add -n <name> -d <date> -p <price> -i <inventory>

    eg.

    python3 main.py add -n baghali -d 1403-01-08 -p 10000 -i 100
```

### DELETE FOOD

```bash
    python3 main.py delete <IDs>

    eg.

    python3 main.py delete 4241
```

### RESERVE

```bash
    python3 main.py reserve -s <studentID> -f <foodID>

    eg.

    python3 main.py reserve -s 40131053 -f 1
```

### CHANGE RESERVE

```bash
    python3 main.py change -s <SRCreserveID> -d <DSTreserveID> -t <date>

    eg.

    python3 main.py change -s 1 -d null
```
