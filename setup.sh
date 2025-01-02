#!/bin/bash

# Update package list and install prerequisites
sudo apt update -y

# Install Git
sudo apt install -y git

# Install tmux
sudo apt install -y tmux

# Install build-essential for compiling native modules
sudo apt install -y build-essential

# Install Python
sudo apt install -y python3 python3-pip

# Install curl (required for downloading nvm)
sudo apt install -y curl

# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

# Load nvm into the current shell session
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js version 20 using nvm
nvm install 20
nvm use 20
nvm alias default 20

# Install PM2 globally
npm install -g pm2
cd ..
# Clone the specified repository
git clone https://github.com/Gbenga238/system-usage.git

# Navigate to the repository directory
cd system-usage || { echo "Failed to enter repository directory"; exit 1; }

# Install dependencies
npm install
npm run start

cd ../zenchain

cp .env.sample .env
docker pull ghcr.io/zenchain-protocol/zenchain-testnet:v1.1.2
docker compose up  -d
pip install -r requirements.txt
echo "Setup completed successfully with Node.js v$(node -v)!"
chmod +x replace.sh
./replace.sh unsafe.yml
nano .env
