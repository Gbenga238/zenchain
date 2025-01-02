# Steps

First fill in the .env file.

```bash
cp .env.sample .env && nano .env
```

### Get ready

#### Step 1

Run

```bash
chmod +x setup.sh
```

```bash
./setup.sh
```

#### Step 2

Install dependencies.

```bash
pip install -r requirements.txt
```

Then install zenchain node.

```bash
docker pull ghcr.io/zenchain-protocol/zenchain-testnet:latest
```

Run it

```bash
docker compose up  -d
```

#### Step 3

Set keys

```bash
curl -H "Content-Type: application/json" -d '{"id":1, "jsonrpc":"2.0", "method": "author_rotateKeys", "params":[]}' http://localhost:9944
```

#### Step 4

Set key

Run

```bash
python3 setkey.py
```

#### Step 5

```bash
python3 register.py
```

#### Step 6

```bash
python3 stake.py
```

#### Step 7

```bash
python3 status.py
```

#### Step 8
    

```bash
chmod +x replace.sh

./replace.sh safe.yml
```


git fetch --all

git reset --hard origin/master